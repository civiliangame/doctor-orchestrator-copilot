"""Patient Context Model — the canonical, source-grounded belief state.

The PCM is the running summary of a patient's current status across ALL sources
of information: FHIR bundles, prior clinical notes, markdown chart files, live
scribe conversations, and (later phases) async agents. It is a set of typed
*slots*, each carrying a status (known/uncertain/stale/contradicted/missing), a
confidence, and — the point — full provenance. It is a VIEW layered on top of
the append-only sources, never a replacement for them (same discipline as
node_briefs vs chart_entries).

Scoping: slots belong to the PATIENT (`context_slots`, unique per patient+key) —
the running status survives across visits. What a specific visit still needs is
a separate layer (`visit_slot_requirements`), derived from that visit's
guardrails + node goals by `derive_required_slots` (and extended by whatever a
source declares worth tracking, e.g. the chart-file reader's `why_required`).

Design commitments enforced here:

1. One write path. `record_contribution` is the ONLY way a slot's value changes,
   and it always writes a `context_ledger` row first: which actor, their role,
   when, whether it came from the patient, speech vs typed vs record, the
   verbatim quote, the model (if inferred), and a typed `source_ref` naming the
   exact origin:

       fhir:<record_id>#<ResourceType>/<id>[,...]   exact FHIR resource(s)
       fhir:<record_id>#longitudinal                record-level summarized fact
       turn:<turn_id>                               conversation turn
       note:<date>:<author>                         clinical note
       file:<md_file>                               markdown chart file ingest
       agent:<name>[:<run>]                         async agent contribution

   The slot's `current_ledger_id` points at the row that justifies its present
   value; the full history is queryable, so the patient's context at any time is
   auditable (replay the ledger).

2. Slot vocabulary comes from ground truth, not the model. Deterministic sources
   (FHIR ingest, seeds, visit derivation) may create slots by passing `label=`;
   the per-turn LLM integrator can only fill slots that already exist — an
   unknown key still gets its audit ledger row, but no slot materializes. (The
   chart-file reader is the deliberate exception: it mints keys for what a
   hand-authored file establishes, via chart_md's own validation.)

3. Live beliefs mirror to the patient's chart file. Every LIVE contribution
   (speech/typed/image/measurement/inferred — not fhir/seed, which came FROM
   the record) is appended by chart_md.append_update to the patient's markdown
   file under its DOC-managed section, with provenance. The file stays a
   faithful, human-readable running ledger.
"""

from db import ins, now_iso, one, q

VALID_STATUS = ("known", "uncertain", "stale", "contradicted", "missing")

# Weight each status contributes to the visit's "context completeness" score.
_STATUS_WEIGHT = {"known": 1.0, "uncertain": 0.4, "stale": 0.3, "contradicted": 0.2, "missing": 0.0}
# Statuses that still represent an OPEN information gap the harness should close.
_OPEN_STATUS = ("missing", "uncertain", "stale", "contradicted")
# Contributions that happened LIVE (vs pulled from the record) — these mirror to
# the patient's markdown chart file.
_LIVE_KINDS = ("speech", "typed", "image", "measurement", "inferred")

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

# What the hand-written summary + last visit note already establish. These become
# the initial ledger entries — provenance-wise they are just another source (the
# prior clinical note), referenced by `note:<date>:<author>`. A value of None
# means "genuinely unknown today" — the slot stays a visible gap. `bp.current`
# is seeded STALE on purpose: last week's reading exists but today needs a fresh one.
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
    "source_kind": "seed", "source_ref": "note:2026-07-11:dr-zhang",
    "source_channel": "seed", "actor_role": "clinician",
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


def ensure_slot(patient_id: int, key: str, label: str, category: str) -> dict:
    """Get the patient's slot for `key`, creating an empty (missing) one if new.
    Only deterministic sources call this — the vocabulary comes from ground truth."""
    slot = one("SELECT * FROM context_slots WHERE patient_id=? AND key=?", (patient_id, key))
    if slot:
        return slot
    sid = ins("context_slots", patient_id=patient_id, key=key, label=label,
              category=category, status="missing", value="", confidence=0.0,
              updated_ts=now_iso())
    return one("SELECT * FROM context_slots WHERE id=?", (sid,))


def add_requirement(visit_id: int, slot_key: str, why_required: str) -> None:
    """Mark a slot as required by a visit (upsert; existing why wins unless empty)."""
    from db import ex
    req = one("SELECT * FROM visit_slot_requirements WHERE visit_id=? AND slot_key=?",
              (visit_id, slot_key))
    if req is None:
        ins("visit_slot_requirements", visit_id=visit_id, slot_key=slot_key,
            why_required=why_required)
    elif why_required and not req["why_required"]:
        ex("UPDATE visit_slot_requirements SET why_required=? WHERE id=?",
           (why_required, req["id"]))


def derive_required_slots(visit_id: int) -> None:
    """Materialize what today's visit needs: ensure the patient-level slots exist
    and record, per visit, WHY each is required (guardrails + node goals + the
    condition template). Idempotent: upserts by (visit_id, slot_key)."""
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    if visit is None:
        return
    guardrails = q("SELECT * FROM guardrails WHERE visit_id=? ORDER BY num", (visit_id,))
    goal_rows = q("SELECT goals_json FROM journey_nodes WHERE visit_id=?", (visit_id,))
    from db import ex, jloads
    goals: list[str] = []
    for r in goal_rows:
        goals += jloads(r["goals_json"], [])

    for spec in CARDIAC_SLOTS:
        why = _why_required(spec["keywords"], guardrails, goals)
        slot = ensure_slot(visit["patient_id"], spec["key"], spec["label"], spec["category"])
        ex("UPDATE context_slots SET label=?, category=? WHERE id=?",
           (spec["label"], spec["category"], slot["id"]))
        req = one("SELECT id FROM visit_slot_requirements WHERE visit_id=? AND slot_key=?",
                  (visit_id, spec["key"]))
        if req:
            ex("UPDATE visit_slot_requirements SET why_required=? WHERE id=?", (why, req["id"]))
        else:
            ins("visit_slot_requirements", visit_id=visit_id, slot_key=spec["key"],
                why_required=why)


def seed_context(visit_id: int) -> None:
    """Fill slots with what the prior visit note already establishes, each as a
    provenance-tagged ledger entry (source `note:...`). Only runs when the
    patient's ledger has no note-sourced entries yet."""
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    if visit is None:
        return
    pid = visit["patient_id"]
    if one("SELECT id FROM context_ledger WHERE patient_id=? AND source_kind='seed' LIMIT 1", (pid,)):
        return
    labels = {s["key"]: s for s in CARDIAC_SLOTS}
    for key, fact in SEED_FACTS.items():
        if fact is None:
            continue
        value, status, confidence, quote = fact
        spec = labels.get(key, {})
        record_contribution(
            pid, key, value, status, confidence,
            raw_quote=quote, visit_id=visit_id,
            label=spec.get("label"), category=spec.get("category", "clinical"),
            **_SEED_ACTOR,
        )


# ---------------------------------------------------------------- the write path

def record_contribution(
    patient_id: int, key: str, value: str, status: str, confidence: float, *,
    source_kind: str, source_ref: str = "", source_channel: str = "",
    actor_role: str = "system", actor_id: str = "", actor_name: str = "",
    from_patient: bool = False, extracted_from_speech: bool = False, model: str = "",
    visit_id: int | None = None, session_id: int | None = None,
    node_id: int | None = None, turn_id: int | None = None, raw_quote: str = "",
    label: str | None = None, category: str | None = None,
) -> dict | None:
    """The ONLY way a slot value changes. Always writes a context_ledger row for
    provenance, then points the slot's current_ledger_id at it.

    Passing `label` (deterministic sources: FHIR ingest, seeds, chart-file
    reader) creates the slot when it doesn't exist yet. Without `label` (the LLM
    integrator), an unknown key gets its audit ledger row but no slot — the
    model cannot invent vocabulary. Returns the fresh slot row on change, or
    None on a no-op (same value + status) or an unmatched key.

    Live contributions (speech/typed/image/measurement/inferred) are mirrored
    to the patient's markdown chart file via chart_md.append_update.
    """
    value = (value or "").strip()
    status = status if status in VALID_STATUS else "uncertain"
    confidence = max(0.0, min(1.0, float(confidence or 0.0)))

    slot = one("SELECT * FROM context_slots WHERE patient_id=? AND key=?", (patient_id, key))
    if slot is None and label:
        slot = ensure_slot(patient_id, key, label, category or "clinical")
    # No-op guard: don't spam the ledger when a source re-asserts the same belief.
    if slot and slot["value"] == value and slot["status"] == status:
        return None

    ledger_id = ins(
        "context_ledger", patient_id=patient_id, visit_id=visit_id,
        slot_id=slot["id"] if slot else None, slot_key=key,
        value_written=value, status_written=status, confidence=confidence,
        source_kind=source_kind, source_ref=source_ref, source_channel=source_channel,
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
    fresh = one("SELECT * FROM context_slots WHERE id=?", (slot["id"],))

    # Mirror every LIVE belief change into the patient's markdown chart file.
    # fhir/seed contributions are skipped: they came FROM the record/file.
    if visit_id is not None and source_kind in _LIVE_KINDS:
        from orchestrator import chart_md  # local import: chart_md imports pcm
        chart_md.append_update(
            visit_id, fresh, one("SELECT * FROM context_ledger WHERE id=?", (ledger_id,))
        )
    return fresh


def turn_provenance(turn: dict, ctx: dict, model: str = "") -> dict:
    """Provenance kwargs for a contribution extracted from a transcript turn.
    Speaker → actor; turn.source → speech vs typed (honest: inject == typed);
    source_ref pins the exact turn."""
    is_patient = turn["speaker"] == "patient"
    node, patient = ctx["node"], ctx["patient"]
    from_speech = turn.get("source") == "soniox"
    return {
        "source_kind": "speech" if from_speech else "typed",
        "source_ref": f"turn:{turn['id']}",
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

def requirements_for(visit_id: int) -> dict[str, str]:
    """slot_key -> why_required for a visit."""
    rows = q("SELECT slot_key, why_required FROM visit_slot_requirements WHERE visit_id=?",
             (visit_id,))
    return {r["slot_key"]: r["why_required"] for r in rows}


def ledger_shape(r: dict | None) -> dict | None:
    if r is None:
        return None
    return {
        "id": r["id"], "patient_id": r["patient_id"], "visit_id": r["visit_id"],
        "slot_key": r["slot_key"],
        "value": r["value_written"], "status": r["status_written"],
        "confidence": r["confidence"], "source_kind": r["source_kind"],
        "source_ref": r["source_ref"], "source_channel": r["source_channel"],
        "actor_role": r["actor_role"],
        "actor_id": r["actor_id"], "actor_name": r["actor_name"],
        "from_patient": bool(r["from_patient"]),
        "extracted_from_speech": bool(r["extracted_from_speech"]),
        "model": r["model"], "session_id": r["session_id"],
        "node_id": r["node_id"], "turn_id": r["turn_id"],
        "raw_quote": r["raw_quote"], "ts": r["ts"],
    }


def slot_shape(r: dict, req: dict[str, str] | None = None,
               visit_id: int | None = None) -> dict:
    prov = None
    if r["current_ledger_id"]:
        prov = ledger_shape(one("SELECT * FROM context_ledger WHERE id=?", (r["current_ledger_id"],)))
    req = req or {}
    return {
        "id": r["id"], "patient_id": r["patient_id"], "visit_id": visit_id,
        "key": r["key"], "label": r["label"],
        "category": r["category"], "status": r["status"], "value": r["value"],
        "confidence": r["confidence"], "required": r["key"] in req,
        "why_required": req.get(r["key"], ""), "updated_ts": r["updated_ts"],
        "provenance": prov,
    }


def slot_shape_for_visit(r: dict, visit_id: int) -> dict:
    return slot_shape(r, requirements_for(visit_id), visit_id)


def completeness(visit_id: int) -> dict:
    slots = q(
        "SELECT s.status FROM visit_slot_requirements r "
        "JOIN visits v ON v.id = r.visit_id "
        "JOIN context_slots s ON s.patient_id = v.patient_id AND s.key = r.slot_key "
        "WHERE r.visit_id=?", (visit_id,))
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
    """The visit view: every slot of the visit's patient, decorated with whether
    (and why) THIS visit requires it, plus the patient's full provenance ledger."""
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    pid = visit["patient_id"]
    req = requirements_for(visit_id)
    slots = q("SELECT * FROM context_slots WHERE patient_id=? ORDER BY category, key", (pid,))
    ledger = q("SELECT * FROM context_ledger WHERE patient_id=? ORDER BY id DESC LIMIT ?",
               (pid, ledger_limit))
    return {
        "visit_id": visit_id,
        "patient_id": pid,
        "slots": [slot_shape(s, req, visit_id) for s in slots],
        "completeness": completeness(visit_id),
        "ledger": [ledger_shape(r) for r in ledger],
    }


def get_patient_pcm(patient_id: int, ledger_limit: int = 1000) -> dict:
    """The patient view: the running status across all sources, in ingestion
    order (slot id), with the full ledger. No visit decoration."""
    slots = q("SELECT * FROM context_slots WHERE patient_id=? ORDER BY id", (patient_id,))
    ledger = q("SELECT * FROM context_ledger WHERE patient_id=? ORDER BY id DESC LIMIT ?",
               (patient_id, ledger_limit))
    return {
        "patient_id": patient_id,
        "slots": [slot_shape(s) for s in slots],
        "ledger": [ledger_shape(r) for r in ledger],
    }
