# DOC Frontend ↔ Backend Contract

**This document is the commitment.** The frontend is built against these shapes; the backend
implements them exactly. Changes require editing this file first. Context: `SPEC.md` (system
design), `DEMO_SCRIPT.md` (what the UI must make land on stage).

## Conventions

- Base URL `http://localhost:8000`. All REST under `/api`. JSON bodies, `snake_case` keys
  everywhere — do **not** camelCase on the frontend.
- IDs are integers. Timestamps are ISO 8601 UTC strings (`"2026-07-18T21:04:11.312Z"`).
- Enums are string literals, typed below.
- Errors: appropriate HTTP status + `{ "error": { "code": string, "message": string } }`.
- WebSocket events carry a per-session monotonic `seq` and the row `id` of their entity —
  **dedupe by `(type, data.id)`** so reconnect + rehydrate can overlap safely.

## The five screens

| Screen | Who | Feeds from |
|---|---|---|
| 1. Planning (Beat D) | Dr. Zhang, end of visit N | `plan/generate`, `plan/confirm` |
| 2. Appointments | any station | `GET /api/appointments` |
| 3. Patient page | any station | `GET /api/patients/{id}` — briefs, action items, journey timeline, chart. **Start Session** lives here |
| 4. Live session | station running a session | `POST /api/sessions` + both WebSockets |
| 5. Payoff / handoff | Dr. Zhang at journey end | same as screen 3 — the patient page with full accumulated chart **is** the payoff view |

The journey renders as a **straight horizontal timeline** (nodes ordered by `position`;
`edges` exist in the payload but the demo journey is linear). Statuses: `done` (dimmed, check),
`active` (highlighted), `pending`. A mutation acceptance visibly inserts a node — animate it.

A synthetic-data disclaimer banner renders on every screen.

## Core types

```ts
type Station = "nurse" | "cardiology" | "imaging" | "doctor";
type Role = "staff" | "patient";
type Priority = "high" | "normal";

interface Patient {
  id: number;
  name: string;          // "Maria Alvarez"
  dob: string;           // "1968-03-12"
  summary_text: string;  // hand-written clinical summary, display as-is
}

interface Visit {
  id: number;
  patient_id: number;
  date: string;                    // "2026-07-25"
  intent_text: string;             // Dr. Zhang's Beat D free text
  plan_confirmed: boolean;
}

interface JourneyNode {
  id: number;
  visit_id: number;
  station: Station;
  specialist_name: string;         // "Nurse Kim"
  specialist_profile: string;      // one-liner for display
  goals: string[];
  status: "done" | "active" | "pending";
  position: number;                // render order, ascending
}

interface JourneyEdge { id: number; from_node_id: number; to_node_id: number; }

interface Journey { nodes: JourneyNode[]; edges: JourneyEdge[]; }

interface Guardrail {
  id: number;
  num: number;                     // display as "Guardrail #1"
  condition_text: string;
  action_text: string;
}

interface NodeBrief {              // compiled by Fable at the previous node's End Session
  id: number;
  node_id: number;                 // addressee
  from_node_id: number;
  from_station: Station;
  summary_md: string;              // markdown body
  action_items: { text: string; priority: Priority }[];  // render BIG on the patient page
  created_ts: string;
}

interface Todo {
  id: number;
  visit_id: number;
  created_by_node_id: number;
  for_node_id: number;
  text: string;
  priority: Priority;
  status: "open" | "done";
}

interface TranscriptTurn {
  id: number;
  session_id: number;
  speaker: Role;
  text: string;                    // full finalized turn text
  ts: string;
}

interface Suggestion {
  id: number;
  session_id: number;
  kind: "question" | "action" | "observation";
  text: string;
  reason: string;                  // e.g. "Guardrail: radiating pain" — show as subtitle
  priority: Priority;
  ts: string;
}

interface GuardrailAlert {         // RED, the demo climax — visually loudest element
  id: number;
  session_id: number;
  guardrail_id: number;
  guardrail_num: number;
  condition_text: string;          // denormalized for display
  triggered_by: string;            // "patient: 'spreading to my left arm'" — quote verbatim
  action: string;
  ts: string;
}

interface Contradiction {          // AMBER card, distinct from suggestions
  id: number;
  session_id: number;
  statement: string;               // verbatim quote from this turn
  conflicts_with: string;          // verbatim quote + source label
  severity: "high" | "note";
  suggested_probe: string;
  ts: string;
}

interface ChartEntry {             // append-only; never edited or removed
  id: number;
  visit_id: number;
  node_id: number;
  node_station: Station;           // denormalized — group chart by this
  category: "symptom" | "vital" | "finding" | "note" | "contradiction";
  text: string;
  ts: string;
}

interface JourneyMutation {        // banner with [Accept] [Dismiss]
  id: number;
  session_id: number;
  guardrail_id: number;
  description: string;             // "Insert Cardiology consult before Imaging"
  insert_station: Station;
  before_node_id: number;
  status: "proposed" | "accepted" | "dismissed";
  ts: string;
}
```

## REST endpoints

### Screen 1 — Planning (Beat D)

```
POST /api/visits/{visit_id}/plan/generate
  body     { intent_text: string }
  returns  { journey: Journey, guardrails: Guardrail[] }     // draft: nodes now carry goals
  latency  one Claude call, ~2–5s — show a generating state

POST /api/visits/{visit_id}/plan/confirm
  body     { nodes: { id: number, goals: string[] }[], guardrails: { id: number, condition_text: string, action_text: string }[] }
  returns  { journey: Journey, guardrails: Guardrail[] }     // as saved; sets plan_confirmed
```

The doctor edits the draft inline (goals and guardrail text are editable; nodes/edges are not)
then confirms once.

### Screens 2–3 — Appointments & patient page

```
GET /api/appointments?station={Station}
  returns  { appointments: { node_id: number, patient_id: number, patient_name: string,
                             time: string, station: Station, status: JourneyNode["status"] }[] }

GET /api/patients/{patient_id}?node_id={viewing_node_id}
  returns  {
    patient: Patient,
    visit: Visit,
    journey: Journey,
    guardrails: Guardrail[],
    briefs: NodeBrief[],          // addressed to node_id — render summary + BIG action items
    todos: Todo[],                // open items for node_id
    chart: ChartEntry[],          // entire visit chart, group by node_station
    active_session_id: number | null
  }
```

The station switcher (which specialist "am I") is a frontend-only dropdown; it just changes
the `station`/`node_id` query params. No auth.

### Screen 4 — Live session

```
POST /api/sessions
  body     { node_id: number }
  returns  { session_id: number,
             events_url: "ws://localhost:8000/ws/session/{id}/events",
             audio_url:  "ws://localhost:8000/ws/audio?session_id={id}" }

GET  /api/sessions/{id}
  returns  {                       // full rehydration after refresh/reconnect
    session: { id: number, node_id: number, started_ts: string, ended_ts: string | null },
    turns: TranscriptTurn[],
    suggestions: Suggestion[],
    alerts: GuardrailAlert[],
    contradictions: Contradiction[],
    chart_entries: ChartEntry[],   // this session's only
    todos: Todo[],                 // current list, all nodes
    pending_mutation: JourneyMutation | null,
    last_seq: number
  }

POST /api/sessions/{id}/end
  returns  202 { compiling: true } // then session.compile.* events on the events socket

POST /api/mutations/{id}/accept
POST /api/mutations/{id}/dismiss
  returns  { mutation: JourneyMutation, journey: Journey }   // journey.updated also broadcast
```

### Beat C — imaging upload

```
POST /api/nodes/{node_id}/images
  multipart file field "image" (jpeg/png)
  returns  { findings: ChartEntry[] }   // also broadcast as chart.entry events
  latency  one multimodal call, ~3–8s — show an analyzing state
```

### Dev / operator controls (no auth, used off-screen during the demo)

```
POST /api/dev/inject-turn        { session_id, speaker: Role, text }  // type a turn instead of speaking it
POST /api/dev/end-patient-turn   { session_id }                       // H9 fallback hotkey
POST /api/dev/nodes/{id}/complete                                     // demo time-skip ("cardiology cleared")
POST /api/dev/reset                                                   // wipe + reseed DB for rehearsals
```

## WebSocket 1 — audio uplink: `/ws/audio?session_id={id}`

**Upload-only.** Binary frames of mic audio (webm/opus chunks from `MediaRecorder`), text
frame `"stop"` to end. Server sends nothing on this socket except a fatal
`{ "error": { code, message } }` before closing. All transcript display comes from the
events socket.

## WebSocket 2 — events: `/ws/session/{id}/events`

Everything the session screen renders arrives here. Envelope + discriminated union:

```ts
type ServerEvent =
  // live transcript
  | { seq: number; ts: string; type: "transcript.partial";
      data: { speaker: Role; text: string } }                 // in-progress line; REPLACE the
                                                              // current partial for that speaker
  | { seq: number; ts: string; type: "transcript.turn";
      data: TranscriptTurn }                                  // finalized; append, clear partial

  // orchestrator lifecycle
  | { seq: number; ts: string; type: "tick.started";
      data: { turn_id: number } }                             // show a subtle "DOC is thinking"
                                                              // indicator; clear on first card
                                                              // or next tick.started

  // per-turn worker outputs (each may arrive at different times after a tick)
  | { seq: number; ts: string; type: "suggestion";        data: Suggestion }
  | { seq: number; ts: string; type: "guardrail.alert";   data: GuardrailAlert }
  | { seq: number; ts: string; type: "contradiction";     data: Contradiction }
  | { seq: number; ts: string; type: "chart.entry";       data: ChartEntry }

  // patient context model (Phase 1) — a slot's belief changed; re-render its row
  | { seq: number; ts: string; type: "context.slot_updated";
      data: { slot: ContextSlot; completeness: ContextCompleteness } }
  | { seq: number; ts: string; type: "todo.update";
      data: { op: "add" | "complete" | "edit"; todo: Todo } }

  // journey
  | { seq: number; ts: string; type: "journey.mutation_proposed"; data: JourneyMutation }
  | { seq: number; ts: string; type: "journey.updated";           data: Journey }

  // end of session
  | { seq: number; ts: string; type: "session.compile.started"; data: {} }
  | { seq: number; ts: string; type: "session.compile.done";
      data: { briefs: NodeBrief[]; todos: Todo[] } }          // reconciled list, all nodes
  | { seq: number; ts: string; type: "session.ended"; data: {} }

  | { seq: number; ts: string; type: "error";
      data: { code: string; message: string } };
```

### Rendering rules the demo depends on

- **Guardrail alerts are the loudest thing on screen** (red, large, persistent until session
  end). Contradictions are amber cards, visually distinct from the neutral suggestion cards.
  Both must quote their `triggered_by` / `conflicts_with` text verbatim — the citation *is*
  the demo.
- Cards from one tick arrive **staggered** (five parallel workers). Render each on arrival;
  never wait to batch a tick.
- Suggestions: keep the 2 most recent prominent; older ones collapse into a history list.
- `journey.mutation_proposed` renders as a banner with Accept/Dismiss on the journey
  timeline. On `journey.updated`, re-render the timeline — animate the inserted node.
- **Reconnect:** on socket drop, `GET /api/sessions/{id}`, replace local state, reconnect,
  dedupe overlapping events by `(type, data.id)`.
- Chart entries with `category: "contradiction"` also appear in the patient-page chart —
  they survive into the handoff on purpose.

## Patient Context Model (Phase 1 — agentic harness)

The PCM is the structured, provenance-tracked belief state the agentic harness reasons
over. It is a **view** on top of the append-only chart, never a replacement. Slots are
**derived** from the visit's guardrails + node goals (not hand-authored); every belief
carries a full provenance ledger entry so its quality is auditable — which user, who they
are, when, whether it came from the patient, and whether it was pulled from live speech vs
typed vs seeded from the record.

```ts
type SlotStatus = "known" | "uncertain" | "stale" | "contradicted" | "missing";

interface ContextLedgerEntry {      // one contribution to a belief — the quality trail
  id: number;
  slot_key: string;
  value: string;
  status: SlotStatus;
  confidence: number;               // 0..1
  source_kind: "seed" | "speech" | "typed" | "image" | "measurement" | "inferred";
  source_channel: string;           // "seed" | "soniox" | "inject" | "image_upload" | ...
  actor_role: string;               // "patient" | "nurse" | "doctor" | "clinician" | "system" | ...
  actor_id: string;                 // stable id of who: "patient", specialist name, agent
  actor_name: string;               // display name of who
  from_patient: boolean;            // did this originate from the patient?
  extracted_from_speech: boolean;   // pulled from live/transcribed speech (vs typed/seed)
  model: string;                    // model that asserted it, if inferred
  session_id: number | null;
  node_id: number | null;
  turn_id: number | null;           // transcript turn this came from
  raw_quote: string;                // verbatim supporting text (the citation)
  ts: string;
}

interface ContextSlot {
  id: number;
  visit_id: number;
  key: string;                      // stable, e.g. "chest_pain.radiation"
  label: string;
  category: string;                 // symptom | vital | medication | risk | history | logistics
  status: SlotStatus;
  value: string;                    // current best value ("" when missing)
  confidence: number;
  required: boolean;
  why_required: string;             // the goal / guardrail that made it required
  updated_ts: string;
  provenance: ContextLedgerEntry | null;   // the ledger row justifying the current value
}

interface ContextCompleteness {
  total_required: number;
  counts: Record<SlotStatus, number>;
  open_gaps: number;                // slots still missing/uncertain/stale/contradicted
  percent: number;                  // weighted 0..100 readiness score
}

interface PatientContext { visit_id: number; slots: ContextSlot[];
  completeness: ContextCompleteness; ledger: ContextLedgerEntry[]; }
```

```
GET /api/visits/{visit_id}/context
  returns  PatientContext            // belief state + completeness + full ledger (newest first)
```

Live updates arrive on the events socket as `context.slot_updated` (above): the backend's
context-integrator worker (a per-turn accumulator, like chart/todos) folds each patient
turn into the slots and broadcasts the changed slot plus the new completeness. The frontend
overlays these on a one-time `GET .../context` baseline.

## Migration note (backend, current code)

`backend/main.py`'s `/ws/transcribe` currently relays raw Soniox token JSON to the client.
Under this contract that socket becomes `/ws/audio` (upload-only) and the backend translates
Soniox tokens into `transcript.partial` / `transcript.turn` events on the events socket,
applying the role-mapping and 900ms end-of-turn rules from `SPEC.md § Turn pipeline`.
`frontend/src/useTranscriber.ts` should split accordingly: one hook owns mic capture + the
audio socket; a separate hook owns the events socket and all rendered state.
