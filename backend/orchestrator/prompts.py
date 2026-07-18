"""Prompt assembly for the per-turn workers, the compiler, and the planner.

Layout per SPEC.md § Turn pipeline:
- CACHED prefix: identical string across all five workers and all ticks of a
  session (built once, cached in _prefix_cache) -> prefix cache hit for the
  4 sibling calls of every tick.
- Per-worker second system block: role + output schema + rules (static text).
- Dynamic user message: journey, chart, todos, already-shown (dedup),
  transcript window with the analyzed turn(s) clearly marked.
"""

from config import TRANSCRIPT_CONTEXT_TURNS
from db import jloads, q

# ---------------------------------------------------------------- cached prefix

_prefix_cache: dict[int, str] = {}


def session_prefix(ctx: dict) -> str:
    """The shared cached system block. Byte-identical for a session's lifetime."""
    sid = ctx["session"]["id"]
    cached = _prefix_cache.get(sid)
    if cached is not None:
        return cached

    node, visit, patient = ctx["node"], ctx["visit"], ctx["patient"]
    guardrails = q(
        "SELECT * FROM guardrails WHERE visit_id=? ORDER BY num", (visit["id"],)
    )
    guardrail_lines = "\n".join(
        f"Guardrail #{g['num']}: IF {g['condition_text']} THEN {g['action_text']}"
        for g in guardrails
    ) or "(none defined)"
    goals = jloads(node["goals_json"], [])
    goal_lines = "\n".join(f"- {g}" for g in goals) or "- (no goals set)"

    text = f"""You are DOC (Doctor Orchestrator Copilot), an ambient clinical copilot. You listen to a live clinic conversation between a staff member and a patient. Several specialized workers analyze each patient turn; this shared context block is identical for all of them. Your worker role and output schema follow in the next system block.

GLOBAL RULES (every worker follows all of these):
1. SILENCE IS PREFERRED. Every output array may be empty. Emit an item ONLY when it is clearly warranted by the conversation. No filler, no speculation, no restating the obvious.
2. NEVER repeat an item that is already shown (see the ALREADY SHOWN section of the user message). If in doubt whether something is a duplicate, stay silent.
3. QUOTE TRIGGER TEXT VERBATIM. Wherever a field asks for a quote, copy the exact words from the transcript or record. Never paraphrase inside quotes.
4. You are a copilot, not a doctor. Never diagnose. Frame findings as items for the clinical team's review.
5. Reply with ONLY one JSON object matching your worker's schema. No prose, no markdown fences.

== PATIENT RECORD (hand-written clinical summary; includes the last visit's note) ==
{patient["summary_text"]}

== TODAY'S VISIT INTENT (written by the doctor when planning this visit) ==
{visit["intent_text"]}

== NUMBERED GUARDRAILS (the doctor's escalation checklist for today's visit) ==
{guardrail_lines}

== CURRENT STATION (where this live session is happening) ==
Station: {node["station"]} — {node["specialist_name"]} ({node["specialist_profile"]})
Session goals for this station:
{goal_lines}"""

    _prefix_cache[sid] = text
    return text


def clear_session_prefix(session_id: int) -> None:
    _prefix_cache.pop(session_id, None)


# ---------------------------------------------------------------- worker system blocks

CONTRADICTIONS_SYSTEM = """YOUR WORKER: CONTRADICTION DETECTOR (runs once per patient turn)

Compare THE TURN TO ANALYZE (marked at the end of the user message) against ALL THREE sources:
  (a) the seeded PATIENT RECORD block above (medications, history, plan),
  (b) the last visit's note inside that record (what was prescribed and observed last week),
  (c) EVERY earlier statement in this session's transcript.

Report a contradiction ONLY when the patient's new statement factually conflicts with one of those sources. New information, symptom progression, or elaboration is NOT a contradiction:
- Symptom changes since the last visit are EXPECTED (that is why this follow-up exists). Pain that was non-radiating last week but radiates now is progression — never a contradiction.
- Vague patient timelines ("maybe two weeks ago") that only roughly disagree with record dates are not contradictions.
- A patient truthfully disclosing non-adherence ("I stopped taking X") does NOT contradict the record showing X was prescribed or started — that is honest disclosure the chart worker records. Never flag "stopped X" against a "started/prescribed X" note, regardless of how the dates line up. The contradiction happens if they LATER claim adherence ("I've been taking X every day") after that disclosure — then quote both of the patient's statements.
- A contradiction is the patient asserting a fact that conflicts with a fact they or the record previously asserted.

Output schema (one JSON object, nothing else):
{"contradictions": [{
  "statement": "verbatim quote from THE TURN TO ANALYZE",
  "conflicts_with": "verbatim conflicting quote, then its source label in parentheses",
  "severity": "high|note",
  "suggested_probe": "one short question the staff member can ask to resolve the conflict"
}]}

Rules:
- "statement" and "conflicts_with" MUST contain the actual quoted words.
- Source labels: (this session, earlier turn) / (last visit note) / (patient record). Example conflicts_with value: "the aspirin was bothering my stomach, so I stopped it (this session, earlier turn)".
- severity "high" for medication adherence, cardiac symptoms, or any safety-relevant conflict; otherwise "note".
- suggested_probe: ONE short question, at most 15 words.
- Return {"contradictions": []} when there is no genuine direct conflict. Never re-report a contradiction listed in ALREADY SHOWN."""

SUGGESTIONS_SYSTEM = """YOUR WORKER: SUGGESTIONS (at most 2 per turn)

Suggest at most 2 things the current staff member should ask or do NEXT, driven by:
- the session goals for this station,
- the visit intent and numbered guardrails,
- what THE TURN TO ANALYZE just revealed.

Output schema (one JSON object, nothing else):
{"suggestions": [{
  "kind": "question|action|observation",
  "text": "short, speakable suggestion",
  "reason": "short pointer to the driving goal or guardrail",
  "priority": "high|normal"
}]}

Rules:
- 0, 1, or 2 items; prefer 0 or 1. An empty array is the right answer when the conversation is already on track.
- "reason" cites the source, e.g. "Dr. Zhang's goal #1" or "Guardrail #2: numbness / shortness of breath".
- Never suggest something the staff member just asked, something the patient already answered, or anything in ALREADY SHOWN — including the same action reworded.
- When a guardrail fires on this turn, do NOT suggest escalating — the red alert card already instructs that. Instead suggest the single next clinical question, e.g. screening the remaining escalation criteria ("Ask about numbness and shortness of breath now").
- Keep "text" under 20 words; keep "reason" under 10 words."""

GUARDRAILS_SYSTEM = """YOUR WORKER: GUARDRAIL CHECKLIST MATCHER

You are a strict checklist matcher. Use ONLY two inputs: the NUMBERED GUARDRAILS list above and the transcript in the user message. Ignore all other context. Do not editorialize, infer beyond the checklist, or invent conditions.

A guardrail fires ONLY if THE TURN TO ANALYZE explicitly satisfies its condition in the patient's own words. Example: pain "spreading to my left arm" satisfies a condition about pain radiating to the arm. A condition being merely discussed, asked about, or explicitly denied does NOT fire it.

Output schema (one JSON object, nothing else):
{"guardrail_alerts": [{
  "guardrail_id": <the guardrail NUMBER from the list, e.g. 1>,
  "triggered_by": "patient: 'verbatim quote from THE TURN TO ANALYZE'",
  "action": "the guardrail's action text, copied from the list"
}]}

Rules:
- Empty array unless a condition is explicitly met by THIS turn.
- At most one entry per guardrail number. Never fire a number already listed under ALREADY SHOWN alerts.
- "triggered_by" must contain the patient's exact words inside the quotes."""

CHART_SYSTEM = """YOUR WORKER: CHART SCRIBE (append-only)

Extract NEW clinical facts from the NEW TURNS (marked in the transcript) as terse chart entries. Style: clinical shorthand — e.g. "BP 142/88", "Chest pain now radiating to left arm, onset ~2 days", "Reports stopping aspirin ~2 wks ago due to GI upset".

Output schema (one JSON object, nothing else):
{"chart_updates": [{"category": "symptom|vital|finding|note|contradiction", "text": "..."}]}

Rules:
- Only facts actually stated in the NEW turns. 0-3 entries per pass; empty array when the new turns contain no new clinical facts (greetings, logistics, repeats).
- Never repeat or rephrase anything already in CHART SO FAR.
- Use category "contradiction" only when recording that the patient contradicted an earlier statement or the record (e.g. misreported adherence, later corrected)."""

TODOS_SYSTEM = """YOUR WORKER: TO-DO COORDINATOR

Maintain the cross-station to-do list for today's visit. Use node ids from the JOURNEY section of the user message for "for_node_id".

Ops:
- "add": a new, concrete task for a LATER station that follows from the NEW turns (e.g. a finding the cardiologist must evaluate). Requires for_node_id, text, priority.
- "complete": an open todo in CURRENT TODOS was fully answered or handled during this session. Requires its id.
- "edit": an existing todo's text or priority must change based on new information. Requires id plus the changed fields.

Output schema (one JSON object, nothing else):
{"todo_updates": [{"op": "add|complete|edit", "id": "todo-<n>", "for_node_id": <node id>, "text": "...", "priority": "high|normal"}]}

Rules:
- An empty array is the norm. Add a todo only for a genuinely actionable, station-specific follow-up; never duplicate an existing todo (including near-duplicates).
- Keep todo text specific and clinical, e.g. "Evaluate radiating chest pain with finger paresthesia, onset ~2 days"."""

PCM_SYSTEM = """YOUR WORKER: CONTEXT INTEGRATOR (structured belief state)

Maintain the Patient Context Model — a FIXED set of information SLOTS today's visit needs (listed under CONTEXT SLOTS in the user message). For each slot the NEW TURNS give fresh information about, emit an update. Never invent slot keys; use only the keys listed.

Status for each update:
- "known": the new turns clearly establish the current value (a clear denial — "no numbness, no shortness of breath" — is a valid known value).
- "uncertain": partially addressed or hedged; more confirmation needed.
- "contradicted": the patient's new statement conflicts with the slot's CURRENT value or the record.
- Omit a slot entirely if the new turns add nothing about it.

Output schema (one JSON object, nothing else):
{"slot_updates": [{
  "key": "<one of the slot keys exactly>",
  "value": "concise current value in clinical shorthand",
  "status": "known|uncertain|contradicted",
  "confidence": 0.0-1.0,
  "quote": "verbatim patient words this is based on"
}]}

Rules:
- Only touch a slot the NEW TURNS actually speak to. An empty array is the norm for greetings/logistics.
- "quote" MUST be the patient's exact words from the transcript — it is the provenance citation stored with the update.
- Never emit an update whose value equals the slot's current value; prefer sharpening a value over restating it.
- Raise a slot to "known" only when the answer is unambiguous. Use "contradicted" when the patient reverses a prior statement (e.g. later claims aspirin adherence after admitting they stopped)."""

WORKER_SYSTEM = {
    "contradictions": CONTRADICTIONS_SYSTEM,
    "suggestions": SUGGESTIONS_SYSTEM,
    "guardrails": GUARDRAILS_SYSTEM,
    "chart": CHART_SYSTEM,
    "todos": TODOS_SYSTEM,
    "pcm": PCM_SYSTEM,
}

COMPILE_SYSTEM = """YOUR WORKER: END-OF-SESSION COMPILER

The session at the current station has ended. Produce:
1. Exactly one handoff brief per node listed under NEXT NODES in the user message — a concise markdown summary of what this session learned that THAT specific specialist needs, plus their big action items.
2. To-do reconciliation ops: close ("complete") todos that were answered during this session, dedupe, and re-prioritize where warranted. You may also "add" a missing follow-up.

Output schema (one JSON object, nothing else):
{"briefs": [{
   "node_id": <id from NEXT NODES>,
   "summary_md": "markdown, <=120 words, most important finding first",
   "action_items": [{"text": "imperative, specific", "priority": "high|normal"}]
 }],
 "todo_ops": [{"op": "complete|edit|add", "id": "todo-<n>", "for_node_id": <node id>, "text": "...", "priority": "high|normal"}]}

Rules:
- One brief per listed next node, tailored to that station's role. 2-4 action items each.
- Briefs MUST reflect fired guardrail alerts and contradictions — they are safety-critical handoff context. Quote vitals exactly.
- Do not invent findings; only compile what is in the transcript, chart, alerts, contradictions, and todos.
- The raw chart is preserved separately; the brief is a curated view, not a replacement."""

PLAN_SYSTEM = """You are DOC's visit planner. You are given a FIXED patient journey (you may NOT add, remove, or reorder nodes) and the doctor's free-text intent for the visit. Produce:
1. Per-node goals: 2-4 short imperative goals per node, derived from the intent and the patient record, checkable during that station's session.
2. Numbered guardrails: one per condition->action escalation the doctor states, numbered IN THE EXACT ORDER the conditions appear in the intent text. Guardrail #1 is the first condition the doctor mentions.

Output schema (one JSON object, nothing else):
{"nodes": [{"node_id": <id>, "goals": ["...", "..."]}],
 "guardrails": [{"num": 1, "condition_text": "concise clinical condition", "action_text": "the doctor's required action", "cardiology_escalation": true}]}

Rules:
- Cover every condition->action pair the doctor states; do not invent extra guardrails.
- SPLITTING: split at the level of the doctor's distinct condition CLAUSES, not individual words. "if the pain radiates to the arm, jaw, or back" is ONE clause -> ONE guardrail; "or she reports numbness or shortness of breath" is a SECOND clause -> ONE guardrail covering both symptoms together. Never split a single clause's alternatives ("arm, jaw, or back"; "numbness or shortness of breath") into separate guardrails.
- Monitoring instructions are guardrails too: "confirm she's tolerating drug X" implies a guardrail like "X non-adherence or side effects -> flag to the doctor".
- Only conditions requiring a DEVIATION or safety action (escalate, hold, flag, call) are guardrails. Routine plan steps ("chest CT if the pain persists") are node goals, NOT guardrails.
- WORKED EXAMPLE — the intent "If the pain radiates to the arm, jaw, or back, or she reports numbness or shortness of breath — escalate: I want a cardiology consult before any imaging. Confirm she's tolerating drug X; she's had side effects before. Recheck BP — if it's above 160/100, hold imaging and call me." yields exactly FOUR guardrails:
  #1 "Chest pain radiating to the arm, jaw, or back" -> "Escalate: cardiology consult before any imaging" (cardiology_escalation: true)
  #2 "New numbness or shortness of breath" -> "Escalate: cardiology consult before any imaging (same escalation as #1)" (cardiology_escalation: true)
  #3 "Drug X non-adherence or side effects" -> "Flag to the doctor before continuing the drug X plan" (cardiology_escalation: false)
  #4 "Blood pressure above 160/100" -> "Hold imaging; call the doctor" (cardiology_escalation: false)
- "cardiology_escalation" is true ONLY for guardrails whose action is escalating to a cardiology consult before imaging (e.g. pain radiating to arm/jaw/back; new numbness or shortness of breath). All other guardrails: false.
- condition_text and action_text must be short and display-ready (they render on cards).
- Include an entry in "nodes" for every journey node given."""


# ---------------------------------------------------------------- dynamic user message

def _transcript_rows(session_id: int, upto_turn_id: int, since_turn_id: int | None) -> list[dict]:
    rows = q(
        "SELECT * FROM transcript_turns WHERE session_id=? AND id<=? ORDER BY id DESC LIMIT ?",
        (session_id, upto_turn_id, TRANSCRIPT_CONTEXT_TURNS),
    )[::-1]
    if since_turn_id is not None and rows and rows[0]["id"] > since_turn_id + 1:
        extra = q(
            "SELECT * FROM transcript_turns WHERE session_id=? AND id>? AND id<? ORDER BY id",
            (session_id, since_turn_id, rows[0]["id"]),
        )
        rows = extra + rows
    return rows


def dynamic_message(
    ctx: dict, turn_id: int, mode: str, since_turn_id: int | None = None
) -> str:
    """The per-tick user message. mode: 'urgent' (analyze the final patient turn)
    or 'accumulator' (process all turns newer than since_turn_id)."""
    session, node, visit = ctx["session"], ctx["node"], ctx["visit"]
    sid, vid = session["id"], visit["id"]

    nodes = q("SELECT * FROM journey_nodes WHERE visit_id=? ORDER BY position", (vid,))
    journey_lines = "\n".join(
        f"node {n['id']} [{n['status']}]: {n['station']} — {n['specialist_name']}"
        for n in nodes
    )
    station_by_node = {n["id"]: n["station"] for n in nodes}

    chart = q("SELECT * FROM chart_entries WHERE visit_id=? ORDER BY id", (vid,))
    chart_lines = "\n".join(
        f"[{c['category']}] {c['text']} ({station_by_node.get(c['node_id'], '?')})"
        for c in chart
    ) or "(none yet)"

    todos = q("SELECT * FROM todos WHERE visit_id=? ORDER BY id", (vid,))
    todo_lines = "\n".join(
        f"todo-{t['id']} [{t['status']}, {t['priority']}] for node {t['for_node_id']}"
        f" ({station_by_node.get(t['for_node_id'], '?')}): {t['text']}"
        for t in todos
    ) or "(none)"

    # Context slots — only shown to the accumulator group (the context integrator
    # consumes them; chart/todos ignore them). Keeps the tuned urgent workers untouched.
    slots_section = ""
    if mode == "accumulator":
        slot_rows = q(
            "SELECT s.key, s.label, s.status, s.value FROM visit_slot_requirements r "
            "JOIN context_slots s ON s.patient_id=? AND s.key=r.slot_key "
            "WHERE r.visit_id=? ORDER BY s.category, s.key",
            (visit["patient_id"], vid),
        )
        slot_lines = "\n".join(
            f"- {s['key']} [{s['status']}] {s['label']}: {s['value'] or '(unknown)'}"
            for s in slot_rows
        ) or "(none)"
        slots_section = (
            f"\n== CONTEXT SLOTS (fixed keys; the context integrator fills these) ==\n{slot_lines}\n"
        )

    shown_sug = q("SELECT text FROM suggestions WHERE session_id=? ORDER BY id", (sid,))
    shown_alerts = q(
        "SELECT g.num, a.triggered_by FROM guardrail_alerts a"
        " JOIN guardrails g ON a.guardrail_id=g.id WHERE a.session_id=? ORDER BY a.id",
        (sid,),
    )
    shown_con = q("SELECT statement FROM contradictions WHERE session_id=? ORDER BY id", (sid,))
    shown_lines = []
    shown_lines.append("suggestions:")
    shown_lines += [f"- {s['text']}" for s in shown_sug] or ["- (none)"]
    shown_lines.append("guardrail alerts (these numbers must NOT fire again):")
    shown_lines += [f"- #{a['num']}: {a['triggered_by']}" for a in shown_alerts] or ["- (none)"]
    shown_lines.append("contradictions:")
    shown_lines += [f"- {c['statement']}" for c in shown_con] or ["- (none)"]

    turns = _transcript_rows(sid, turn_id, since_turn_id)
    t_lines = []
    for t in turns:
        if mode == "accumulator" and since_turn_id is not None and t["id"] == _first_new(turns, since_turn_id):
            t_lines.append("--- NEW TURNS SINCE THE LAST CHART/TODO PASS START HERE ---")
        t_lines.append(f"[{t['speaker']}] {t['text']}")
    transcript_block = "\n".join(t_lines) or "(no transcript yet)"

    if mode == "urgent":
        final = turns[-1] if turns else None
        marker = (
            f">>> THE TURN TO ANALYZE (turn {final['id']}, {final['speaker']}):\n"
            f"\"{final['text']}\""
            if final else ">>> (no turn found)"
        )
    else:
        marker = (
            ">>> Process every turn after the NEW-TURNS marker above. Earlier turns are "
            "context only — they were already processed in previous passes."
        )

    return f"""== JOURNEY (today's visit; use these node ids) ==
{journey_lines}

== CHART SO FAR (all stations, today's visit) ==
{chart_lines}

== CURRENT TODOS ==
{todo_lines}
{slots_section}
== ALREADY SHOWN (do not repeat any of these) ==
{chr(10).join(shown_lines)}

== TRANSCRIPT (this session, oldest first) ==
{transcript_block}

{marker}"""


def _first_new(turns: list[dict], since_turn_id: int) -> int | None:
    for t in turns:
        if t["id"] > since_turn_id:
            return t["id"]
    return None
