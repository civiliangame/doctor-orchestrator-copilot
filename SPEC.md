# DOC Orchestration Spec

Locked decisions from design review (2026-07-18). Supersedes DESIGN.md where they differ.
`DEMO_SCRIPT.md` is the acceptance test — every mechanism here exists to make that script land.

## Decisions log

1. **Voice: direct Soniox WebSocket** (`stt-rt-v5`, diarization on). LiveKit is out of the
   stack entirely. The relay in `backend/main.py` is the transport; this spec adds
   role-mapping and turn detection on top of it.
2. **The patient journey is a DAG in the data model, linear in the demo.** Specialist screens
   render it as a straight timeline (past and future nodes). No graph UI.
3. **The journey graph is seeded, not generated.** Beat D's Claude call takes the doctor's
   plain-text intent and fills each node's goals and numbered guardrails; it never invents
   nodes or edges.
4. **Mid-session graph mutation is allowed, human-in-the-loop.** When a guardrail with a
   `proposed_insert` fires, the *backend* (not a model) creates a mutation proposal; the
   specialist clicks Accept; the timeline re-routes. Models never edit the graph directly.
5. **Navigation model:** appointments list → patient page (compiled brief + action items +
   journey timeline) → **Start Session** (live transcript + pop-up cards) → **End Session**.
   There is no separate "mailbox" — a node's inbound to-dos and briefs render on the patient
   page when its specialist opens it.
6. **Per-turn workers: five parallel Claude calls per patient turn**, sharing one cached
   prompt prefix (see § Turn pipeline).
7. **End-of-session compiler: Fable.** Produces a handoff brief per outgoing edge and
   reconciles the to-do list. Never rewrites `chart_entries` (append-only audit trail).
8. **Silence is a valid output.** Every worker may return empty arrays; suggestions are
   capped at 2 per turn; everything dedupes against what's already been shown.

## Per-turn workers

| Worker | Model | Output | Cancellation policy |
|---|---|---|---|
| contradictions | Sonnet | `contradictions[]` | latest-wins: new patient turn cancels in-flight call, re-fires with fuller transcript |
| suggestions | Sonnet | `suggestions[]` (≤2) | latest-wins |
| guardrails | Haiku | `guardrail_alerts[]` | latest-wins |
| chart | Haiku | `chart_updates[]` | **sequential accumulator**: never cancelled; each call covers all turns since the last completed call |
| todos | Haiku | `todo_updates[]` | sequential accumulator |
| *(end of session)* compiler | Fable | briefs + todo reconciliation | n/a — runs once on End Session |

**Output schemas:**

```json
{
  "contradictions":   [{ "statement": "verbatim quote from this turn",
                         "conflicts_with": "verbatim quote + source (seeded record | visit-N note | this session HH:MM)",
                         "severity": "high|note",
                         "suggested_probe": "..." }],
  "suggestions":      [{ "kind": "question|action|observation", "text": "...",
                         "reason": "...", "priority": "high|normal" }],
  "guardrail_alerts": [{ "guardrail_id": 1, "triggered_by": "patient: 'verbatim quote'",
                         "action": "..." }],
  "chart_updates":    [{ "category": "symptom|vital|finding|note|contradiction", "text": "..." }],
  "todo_updates":     [{ "op": "add|complete|edit", "id": "todo-7",
                         "for_node_id": 3, "text": "...", "priority": "high|normal" }]
}
```

**Prompt rules baked into every worker:** empty output is preferred over filler; never repeat
an already-shown item; quote trigger text verbatim. The contradiction worker explicitly
compares the new turn against (a) the seeded record, (b) last visit's notes/goals, (c) every
earlier statement in this session's transcript. The guardrail worker gets only the numbered
guardrail list and the transcript — a checklist match, nothing more.

## Turn pipeline

1. **Transcript events** from the Soniox relay, per session. Speaker-role mapping: the
   scripted greeting anchors *first speaker = staff*; thereafter turns **strictly alternate**
   staff/patient. Diarization labels confirm; on disagreement, alternation wins.
2. **Patient end-of-turn:** a final segment attributed to the patient followed by **900ms**
   with no further patient-attributed finals. (H9 fallback: operator hotkey emits the same
   internal event.)
3. **Tick:** assemble the prompt and fire all five workers in parallel.
4. Persist outputs to SQLite; broadcast over the session WebSocket; UI renders cards as each
   worker returns — urgent workers (guardrails, contradictions, suggestions) are not blocked
   by the accumulators.

**Prompt layout (identical cached prefix across all five workers):**

```
[CACHED PREFIX — static per session]
  system: worker role + station persona + output schema + rules
  patient record: hand-written summary, meds, history, prior visit notes (verbatim seed)
  visit goals & numbered guardrails
  this specialist's profile
  journey: node list with status (done/active/pending)

[DYNAMIC SUFFIX — grows per turn]
  chart entries so far (all stations, today)
  current to-do list (stable IDs)
  already-shown suggestions/alerts/contradictions (dedup)
  transcript: last 20 turns, ending with the turn that fired this tick
```

**Latency budget:** end-of-turn → first card < 3s. First orchestrator task is measuring one
real tick (Soniox final → card render). If over: trim transcript to 10 turns, cap output
tokens, stream.

## End-of-session compile (Fable)

Input: full session transcript, this session's chart entries, current to-dos, fired
alerts/contradictions, the journey. Output:

- **One handoff brief per outgoing edge** of the completed node: summary of new findings +
  big action items for that specific next specialist. Stored in `node_briefs`; rendered at
  the top of that node's patient page.
- **To-do reconciliation ops:** close items answered during the session, dedupe, re-prioritize.
- Marks the node `done`, sets the next node `active`.

Raw `chart_entries` are untouched — the brief is a curated view, the entries are the record.

## Data model (SQLite)

```
patients        (id, name, dob, summary_text)           -- summary_text: hand-written, used verbatim in prompts
visits          (id, patient_id, date, intent_text)     -- intent_text: Beat D input
journey_nodes   (id, visit_id, station, specialist_name, specialist_profile,
                 goals_json, status: done|active|pending, position)
journey_edges   (id, visit_id, from_node_id, to_node_id)
guardrails      (id, visit_id, num, condition_text, action_text,
                 proposed_insert_json NULL)              -- e.g. {"station":"cardiology","before_node_id":3}
node_briefs     (id, node_id, from_node_id, content_md, created_ts)
sessions        (id, node_id, started_ts, ended_ts NULL)
transcript_turns(id, session_id, speaker: staff|patient, text, ts, source: soniox|inject)
suggestions     (id, session_id, kind, text, reason, priority, ts)
guardrail_alerts(id, session_id, guardrail_id, triggered_by, action, ts)
contradictions  (id, session_id, statement, conflicts_with, severity, probe, ts)
chart_entries   (id, visit_id, node_id, ts, category, text)   -- APPEND-ONLY
todos           (id, visit_id, created_by_node_id, for_node_id, text,
                 priority, status: open|done)
journey_mutations(id, session_id, guardrail_id, insert_json,
                 status: proposed|accepted|dismissed)
```

## API surface

**Authoritative contract: `API_CONTRACT.md`** — exact endpoints, request/response types, and
the WebSocket event union. Committed for the frontend handoff; changes go there first.

Summary: REST under `/api` (plan generate/confirm, appointments, patient page, sessions
start/end/rehydrate, mutation accept/dismiss, image upload, dev controls). Two WebSockets:
`/ws/audio?session_id=` (mic upload **only** — replaces the raw-relay down-channel in the
current `/ws/transcribe`) and `/ws/session/{id}/events` (everything the UI renders,
including transcript partials/turns after role-mapping and end-of-turn detection).

`POST /api/dev/inject-turn` is the integration seam: it feeds the same internal
turn-handler the voice pipeline feeds, so the orchestrator is fully buildable and
latency-testable before/without live audio. `POST /api/dev/reset` reseeds the DB between
rehearsals.

## Seed data

**Patient: Maria Alvarez, 58.**
History: hypertension (lisinopril 10mg daily), borderline-high LDL. No prior cardiac events.

**Visit N (last week, Dr. Zhang, primary care):** intermittent exertional chest pain ×2
weeks, non-radiating, no SOB. Started aspirin 81mg daily. Note mentions prior stomach
trouble with NSAIDs. BP 138/86.

**Hand-written summary** (verbatim prompt block, ~150 words): written during seeding, covers
the above plus Dr. Zhang's stated concerns.

**Visit N+1 journey (seeded):** Nurse Intake → Imaging (chest CT) → Dr. Zhang.
Mutation target: Cardiology consult (Dr. Osei) inserted before Imaging when guardrail #1 fires.

**Guardrails (numbered — DEMO_SCRIPT.md depends on these numbers):**

| # | Condition | Action | proposed_insert |
|---|---|---|---|
| 1 | Pain radiating to arm/jaw/back | Escalate: cardiology consult before imaging | cardiology before Imaging |
| 2 | New numbness or shortness of breath | Same escalation as #1 | (attaches to #1's node if already accepted) |
| 3 | Aspirin non-adherence or GI side effects | Flag to Dr. Zhang before continuing aspirin plan | — |
| 4 | BP > 160/100 | Hold imaging; call Dr. Zhang | — |

**Beat C assets:** 2–3 pre-selected images (CT slice, lab panel) with known findings, staged
under `backend/seed/images/`.

## Build order (updated from DESIGN.md Next Steps)

1. SQLite models + seed script (this file is the source of truth) + `/api/dev/inject-turn`.
2. Turn pipeline + five workers, tested entirely via inject-turn; **measure the 3s budget**.
3. Beat D (`/api/plan`) + planning view.
4. Station view (transcript, cards, mutation accept) wired to the existing Soniox relay
   via role-mapping + 900ms end-of-turn detection.
5. End-session Fable compile + patient-page briefs.
6. Beat C image upload.
7. Rehearse against DEMO_SCRIPT.md, tune prompts/seed until every marked trigger fires.
