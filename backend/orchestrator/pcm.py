"""Patient Context Model (Phase 1 of the agentic harness).

The PCM is the living, structured belief state the harness reasons over: a set of
typed *slots*, each carrying a status (known/uncertain/stale/contradicted/missing),
a confidence, and — crucially — full provenance. It is a VIEW layered on top of the
append-only chart, never a replacement for it (same discipline as node_briefs vs
chart_entries in SPEC.md).

Two design commitments enforced here:

1. Required slots are DERIVED, not hand-authored. `derive_required_slots` reads the
   visit's guardrails + node goals (+ a condition template) and materializes the
   slots that today's visit actually needs. Re-planning the visit re-derives them.

2. Every belief has a paper trail. `record_contribution` is the ONLY way a slot's
   value changes, and it always writes a `context_ledger` row first: which user,
   who they are, when, whether it came from the patient, whether it was pulled from
   live speech vs typed vs seeded, the verbatim quote, and the model (if inferred).
   The slot's `current_ledger_id` points at the row that justifies its present value.
"""

from db import ins, now_iso, one, q

VALID_STATUS = ("known", "uncertain", "stale", "contradicted", "missing")

# Weight each status contributes to the visit's "context completeness" score.
_STATUS_WEIGHT = {"known": 1.0, "uncertain": 0.4, "stale": 0.3, "contradicted": 0.2, "missing": 0.0}
# Statuses that still represent an OPEN information gap the harness should close.
_OPEN_STATUS = ("missing", "uncertain", "stale", "contradicted")

# ---------------------------------------------------------------- slot template
# The standard information a cardiac follow-up needs. `keywords` are used to attach
# each slot to the guardrail/goal that makes it required (its "why"), so the demo
# survives a re-plan and a fresh visit still derives sensible slots.
CARDIAC_SLOTS = [
    {"key": "chest_pain.progression", "label": "Chest pain progression since last week",
     "category": "symptom", "keywords": ["progress", "chest pain", "pain persist", "pain"]},
    {"key": "chest_pain.radiation", "label": "Pain radiating to arm, jaw, or back",
     "category": "symptom", "keywords": ["radiat", "arm", "jaw", "back"]},
    {"key": "chest_pain.associated", "label": "New numbness or shortness of breath",
     "category": "symptom", "keywords": ["numb", "shortness", "breath"]},
    {"key": "aspirin.adherence", "label": "Daily aspirin 81mg adherence",
     "category": "medication", "keywords": ["aspirin", "adherence", "tolerat"]},
    {"key": "aspirin.gi_tolerance", "label": "Aspirin GI / stomach tolerance",
     "category": "medication", "keywords": ["stomach", "gi", "side effect", "nsaid"]},
    {"key": "bp.current", "label": "Current blood pressure",
     "category": "vital", "keywords": ["bp", "blood pressure", "160/100", "recheck"]},
]

# What the hand-written summary + last visit note already establish. These become the
# initial ledger entries (source_kind='seed'). A value of None means "genuinely unknown
# today" — the slot stays a visible gap. `bp.current` is seeded STALE on purpose: last
# week's reading exists but today's visit needs a fresh one.
SEED_FACTS = {
    "chest_pain.radiation": (
        "Non-radiating at last visit (2026-07-11)", "known", 0.7,
        "mostly with exertion, NOT radiating at that visit"),
    "chest_pain.associated": (
        "No numbness or shortness of breath at last visit", "known", 0.7,
        "No shortness of breath, no diaphoresis, no numbness"),
    "aspirin.adherence": (
        "Aspirin 81mg started 2026-07-11; today's adherence not yet confirmed", "uncertain", 0.3,
        "STARTED ASPIRIN 81 MG DAILY at that visit"),
    "aspirin.gi_tolerance": (
        "History of stomach upset with NSAIDs; current tolerance not confirmed", "uncertain", 0.3,
        "History of stomach upset with NSAIDs (ibuprofen)"),
    "bp.current": (
        "138/86 at last visit (2026-07-11) — needs recheck today", "stale", 0.4,
        "BP 138/86, HR 78"),
    "chest_pain.progression": None,   # the reason for the visit — unknown until asked today
}

_SEED_ACTOR = {
    "source_kind": "seed", "source_channel": "seed", "actor_role": "clinician",
    "actor_id": "dr_zhang_prior", "actor_name": "Dr. Zhang (prior visit note)",
    "from_patient": False, "extracted_from_speech": False,
}


# ---------------------------------------------------------------- derive + seed

def _why_required(keywords: list[str], guardrails: list[dict], goals: list[str]) -> str:
    """Attribute a slot to the guardrail or goal that makes it required today."""
    for g in guardrails:
        cond = g["condition_text"].lower()
        if any(k in cond for k in keywords):
            return f"Guardrail #{g['num']}: {g['condition_text']}"
    for goal in goals:
        if any(k in goal.lower() for k in keywords):
            return f"Goal: {goal}"
    return "Cardiac follow-up baseline"


def derive_required_slots(visit_id: int) -> None:
    """Materialize the slots today's visit needs, from guardrails + node goals +
    the condition template. Idempotent: upserts by (visit_id, key)."""
    guardrails = q("SELECT * FROM guardrails WHERE visit_id=? ORDER BY num", (visit_id,))
    goal_rows = q("SELECT goals_json FROM journey_nodes WHERE visit_id=?", (visit_id,))
    from db import jloads
    goals: list[str] = []
    for r in goal_rows:
        goals += jloads(r["goals_json"], [])

    for spec in CARDIAC_SLOTS:
        why = _why_required(spec["keywords"], guardrails, goals)
        existing = one("SELECT id FROM context_slots WHERE visit_id=? AND key=?",
                       (visit_id, spec["key"]))
        if existing:
            from db import ex
            ex("UPDATE context_slots SET label=?, category=?, why_required=? WHERE id=?",
               (spec["label"], spec["category"], why, existing["id"]))
        else:
            ins("context_slots", visit_id=visit_id, key=spec["key"], label=spec["label"],
                category=spec["category"], status="missing", value="", confidence=0.0,
                required=1, why_required=why, updated_ts=now_iso())


def seed_context(visit_id: int) -> None:
    """Fill slots with what the seeded record already establishes, each as a
    provenance-tagged ledger entry. Only runs when the ledger is empty for the visit."""
    if one("SELECT id FROM context_ledger WHERE visit_id=? LIMIT 1", (visit_id,)):
        return
    for key, fact in SEED_FACTS.items():
        if fact is None:
            continue
        value, status, confidence, quote = fact
        record_contribution(
            visit_id, key, value, status, confidence,
            raw_quote=quote, **_SEED_ACTOR,
        )


# ---------------------------------------------------------------- the write path

def record_contribution(
    visit_id: int, key: str, value: str, status: str, confidence: float, *,
    source_kind: str, source_channel: str = "", actor_role: str = "system",
    actor_id: str = "", actor_name: str = "", from_patient: bool = False,
    extracted_from_speech: bool = False, model: str = "",
    session_id: int | None = None, node_id: int | None = None,
    turn_id: int | None = None, raw_quote: str = "",
) -> dict | None:
    """The ONLY way a slot value changes. Always writes a context_ledger row for
    provenance, then points the slot's current_ledger_id at it. Returns the fresh
    slot row on change, or None if the update was a no-op (same value + status) or
    the key is not a known slot (the ledger row is still written for the audit trail).
    """
    value = (value or "").strip()
    status = status if status in VALID_STATUS else "uncertain"
    confidence = max(0.0, min(1.0, float(confidence or 0.0)))

    slot = one("SELECT * FROM context_slots WHERE visit_id=? AND key=?", (visit_id, key))
    # No-op guard: don't spam the ledger when the accumulator re-derives the same belief.
    if slot and slot["value"] == value and slot["status"] == status:
        return None

    ledger_id = ins(
        "context_ledger", visit_id=visit_id,
        slot_id=slot["id"] if slot else None, slot_key=key,
        value_written=value, status_written=status, confidence=confidence,
        source_kind=source_kind, source_channel=source_channel,
        actor_role=actor_role, actor_id=actor_id, actor_name=actor_name,
        from_patient=int(bool(from_patient)),
        extracted_from_speech=int(bool(extracted_from_speech)),
        model=model, session_id=session_id, node_id=node_id, turn_id=turn_id,
        raw_quote=raw_quote, ts=now_iso(),
    )
    if slot is None:
        return None  # unknown key — ledger keeps the record, no slot to update

    from db import ex
    ex("UPDATE context_slots SET value=?, status=?, confidence=?, current_ledger_id=?, updated_ts=? "
       "WHERE id=?", (value, status, confidence, ledger_id, now_iso(), slot["id"]))
    return one("SELECT * FROM context_slots WHERE id=?", (slot["id"],))


def turn_provenance(turn: dict, ctx: dict, model: str = "") -> dict:
    """Provenance kwargs for a contribution extracted from a transcript turn.
    Speaker → actor; turn.source → speech vs typed (honest: inject == typed)."""
    is_patient = turn["speaker"] == "patient"
    node, patient = ctx["node"], ctx["patient"]
    from_speech = turn.get("source") == "soniox"
    return {
        "source_kind": "speech" if from_speech else "typed",
        "source_channel": turn.get("source", "inject"),
        "actor_role": "patient" if is_patient else node["station"],
        "actor_id": "patient" if is_patient else node["specialist_name"],
        "actor_name": patient["name"] if is_patient else node["specialist_name"],
        "from_patient": is_patient,
        "extracted_from_speech": from_speech,
        "model": model,
        "session_id": ctx["session"]["id"],
        "node_id": node["id"],
        "turn_id": turn["id"],
    }


# ---------------------------------------------------------------- read + serialize

def ledger_shape(r: dict | None) -> dict | None:
    if r is None:
        return None
    return {
        "id": r["id"], "slot_key": r["slot_key"],
        "value": r["value_written"], "status": r["status_written"],
        "confidence": r["confidence"], "source_kind": r["source_kind"],
        "source_channel": r["source_channel"], "actor_role": r["actor_role"],
        "actor_id": r["actor_id"], "actor_name": r["actor_name"],
        "from_patient": bool(r["from_patient"]),
        "extracted_from_speech": bool(r["extracted_from_speech"]),
        "model": r["model"], "session_id": r["session_id"],
        "node_id": r["node_id"], "turn_id": r["turn_id"],
        "raw_quote": r["raw_quote"], "ts": r["ts"],
    }


def slot_shape(r: dict) -> dict:
    prov = None
    if r["current_ledger_id"]:
        prov = ledger_shape(one("SELECT * FROM context_ledger WHERE id=?", (r["current_ledger_id"],)))
    return {
        "id": r["id"], "visit_id": r["visit_id"], "key": r["key"], "label": r["label"],
        "category": r["category"], "status": r["status"], "value": r["value"],
        "confidence": r["confidence"], "required": bool(r["required"]),
        "why_required": r["why_required"], "updated_ts": r["updated_ts"],
        "provenance": prov,
    }


def completeness(visit_id: int) -> dict:
    slots = q("SELECT status FROM context_slots WHERE visit_id=? AND required=1", (visit_id,))
    counts = {s: 0 for s in VALID_STATUS}
    for r in slots:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    total = len(slots)
    score = sum(_STATUS_WEIGHT.get(r["status"], 0.0) for r in slots) / total if total else 0.0
    return {
        "total_required": total,
        "counts": counts,
        "open_gaps": sum(counts[s] for s in _OPEN_STATUS),
        "percent": round(score * 100),
    }


def get_pcm(visit_id: int, ledger_limit: int = 200) -> dict:
    slots = q("SELECT * FROM context_slots WHERE visit_id=? ORDER BY category, key", (visit_id,))
    ledger = q("SELECT * FROM context_ledger WHERE visit_id=? ORDER BY id DESC LIMIT ?",
               (visit_id, ledger_limit))
    return {
        "visit_id": visit_id,
        "slots": [slot_shape(s) for s in slots],
        "completeness": completeness(visit_id),
        "ledger": [ledger_shape(r) for r in ledger],
    }
