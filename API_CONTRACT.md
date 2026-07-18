# DOC Frontend ↔ Backend Contract (v2 — context-rot pivot)

**This document is the commitment.** The frontend is built against these shapes; the backend
implements them exactly. Changes require editing this file first. Context: `SPEC.md` (system
design), `DEMO_SCRIPT.md` (what the UI must make land on stage).

## Conventions

- Base URL `http://localhost:5000` (ngrok exposes this same port for Telnyx webhooks).
  All UI-facing REST under `/api`. Telnyx-facing routes (`/webhook`, `/media-stream`)
  are NOT part of this contract — the frontend never touches them.
- JSON bodies, `snake_case` keys everywhere — do **not** camelCase on the frontend.
- IDs are integers. Timestamps are ISO 8601 UTC strings (`"2026-07-18T21:04:11.312Z"`).
- Enums are string literals, typed below.
- Errors: appropriate HTTP status + `{ "error": { "code": string, "message": string } }`.
- WebSocket events carry a per-run monotonic `seq` and the row `id` of their entity —
  **dedupe by `(type, data.id)`** so reconnect + rehydrate can overlap safely.

## The demo flow (screens)

| Screen | Feeds from |
|---|---|
| 1. Patient page — the messy record, latest intake if any, **Clean Up Context** button | `GET /api/patients/{id}`, `POST /api/patients/{id}/runs` |
| 2. Run view — one screen, four stages that light up in order: specialist panel findings → interview plan → live call → compiled intake | `GET /api/runs/{id}` + `/ws/runs/{id}/events` |
| 3. Payoff — patient page again: before (documents) / after (compiled intake) side by side | `GET /api/patients/{id}` |

The run is **fully automatic**: one click on Clean Up Context drives analysis → plan →
outbound call → compiled intake with no further input. The UI's job is to make each stage
visible as it happens. A synthetic-data disclaimer banner renders on every screen.

## Core types

```ts
type FindingKind = "contradiction" | "gap" | "ambiguity";
type Severity = "high" | "normal";
type RunStatus = "analyzing" | "planning" | "calling" | "compiling" | "done" | "failed";
type QuestionStatus = "pending" | "asking" | "answered" | "deferred";
type CallTransport = "sim" | "telnyx";
type CallStatus = "dialing" | "active" | "ended";
type CallSpeaker = "agent" | "patient";

interface Patient {
  id: number;
  name: string;              // "Maria Alvarez"
  dob: string;               // "1968-03-12"
  phone: string;             // E.164, the number Telnyx dials
}

interface Document {         // one messy source record — append-only, never rewritten
  id: number;
  patient_id: number;
  title: string;             // "ED Discharge Summary"
  doc_type: string;          // "summary" | "visit_note" | "med_list" | "triage_note" | "referral" | ...
  author: string;            // "Dr. R. Okafor, Emergency Medicine"
  date: string;              // "2026-07-02"
  content_md: string;        // render as markdown
}

interface Run {
  id: number;
  patient_id: number;
  status: RunStatus;
  transport: CallTransport;
  started_ts: string;
  ended_ts: string | null;
}

interface Specialist {       // chosen dynamically by the triage agent
  id: number;
  run_id: number;
  key: string;               // "cardiology", "neurology", "general_medicine", ...
  display_name: string;      // "Cardiology"
  rationale: string;         // one-liner: why triage spun this specialist up
  status: "running" | "done";
}

interface Finding {
  id: number;
  run_id: number;
  specialist_id: number | null;  // null when discovered live on the call
  kind: FindingKind;
  severity: Severity;
  title: string;                 // short card headline
  detail: string;                // one paragraph
  quotes: { doc_title: string; quote: string }[];  // verbatim evidence; doc_title "phone call" for live finds
  patient_answerable: boolean;   // false → becomes a SpecialistTask, not a question
}

interface InterviewQuestion {
  id: number;
  run_id: number;
  finding_ids: number[];         // findings this question resolves
  order: number;                 // ask order, ascending
  question: string;              // patient-facing phrasing
  sub_questions: string[];       // follow-up angles the voice agent works through
  completeness_criteria: string; // what a "detailed enough" answer must contain
  status: QuestionStatus;
}

interface SpecialistTask {       // things a patient can't answer — manual work for humans
  id: number;
  run_id: number;
  finding_id: number;
  for_specialist: string;        // Specialist.key
  instruction: string;           // "Check pupillary light reflex bilaterally"
  why: string;
}

interface Call {
  id: number;
  run_id: number;
  transport: CallTransport;
  status: CallStatus;
  started_ts: string;
  ended_ts: string | null;
}

interface CallTurn {
  id: number;
  call_id: number;
  speaker: CallSpeaker;
  text: string;
  ts: string;
}

interface Answer {               // written by the voice agent's record_answer tool
  id: number;
  question_id: number;
  summary_text: string;          // clinical restatement of what the patient reported
  complete: boolean;             // met the completeness criteria
  ts: string;
}

interface Intake {               // the compiled clean context — the payoff artifact
  id: number;
  run_id: number;
  chief_complaint: string;
  hpi_md: string;                // onset/location/duration/character/aggravating/relieving/radiation/timing/severity
  meds_reconciliation_md: string;
  resolved_contradictions_md: string;
  open_items_md: string;         // remaining manual tasks + anything unresolved
  created_ts: string;
}
```

## REST endpoints

### `GET /api/patients/{patient_id}`

The patient page (screens 1 and 3).

```ts
interface PatientPage {
  patient: Patient;
  documents: Document[];         // the messy record, chronological
  latest_run: Run | null;
  latest_intake: Intake | null;  // non-null → render before/after
  specialist_tasks: SpecialistTask[];  // from the latest run
}
```

### `POST /api/patients/{patient_id}/runs`

Starts a full cleanup run. Fire-and-forget: returns immediately, everything after arrives
over the WebSocket.

Request: `{ "transport": "sim" | "telnyx" }` — `telnyx` dials `patient.phone` for real;
`sim` runs the identical pipeline against the simulated-call seam.

Response `201`: `Run`.

Errors: `409 run_in_progress` if the patient already has an unfinished run.

### `GET /api/runs/{run_id}`

Rehydration for the run view (reconnects, refreshes). Returns everything so far:

```ts
interface RunState {
  run: Run;
  specialists: Specialist[];
  findings: Finding[];
  questions: InterviewQuestion[];
  specialist_tasks: SpecialistTask[];
  call: Call | null;
  call_turns: CallTurn[];
  answers: Answer[];
  intake: Intake | null;
  last_seq: number;              // events at or below this are reflected above
}
```

### Dev / demo controls (`/api/dev/*`)

- `POST /api/dev/reset` → reseed the DB to the demo state. `{ "ok": true }`.
- `POST /api/dev/sim-answer` — **the integration seam.** Body
  `{ "call_id": number, "text": string }`. Feeds one patient utterance into the interview
  loop exactly as the Telnyx STT path does; the loop replies with its next `call.turn`.
  Errors: `409 call_not_active`.
- `POST /api/dev/hangup` — Body `{ "call_id": number }`. Force-ends the call; the run
  proceeds to compile with whatever was answered.

## WebSocket: `/ws/runs/{run_id}/events`

Envelope: `{ "seq": number, "ts": string, "type": string, "data": ... }` — `seq` monotonic
per run, in-memory only; dedupe by `(type, data.id)`, rehydrate via `GET /api/runs/{id}`.

Event union (`data` types reference the core types above):

| type | data | when |
|---|---|---|
| `run.status` | `Run` | every status transition |
| `specialist.selected` | `Specialist` | triage picked a specialist (one event each) |
| `finding.created` | `Finding` | a specialist (or the live call) surfaced an issue |
| `specialist.done` | `Specialist` | that specialist's pass finished |
| `plan.question` | `InterviewQuestion` | orchestrator emitted a question (streamed as built) |
| `plan.task` | `SpecialistTask` | orchestrator routed a non-answerable item |
| `plan.ready` | `{ "id": number, "question_count": number, "task_count": number }` | plan complete, call about to fire |
| `call.status` | `Call` | dialing / active / ended |
| `call.turn` | `CallTurn` | every agent and patient utterance |
| `question.status` | `InterviewQuestion` | pending → asking → answered/deferred |
| `answer.recorded` | `Answer` | the agent's record_answer tool fired |
| `intake.ready` | `Intake` | compile finished — the payoff moment |

Ordering guarantee: within one run, `plan.ready` arrives after every `plan.question`;
`intake.ready` is always the final event before `run.status: done`.

## Sim-call loop (how the frontend demos without a phone)

1. `POST /api/patients/1/runs` with `{"transport": "sim"}`.
2. Watch the run view light up: specialists → findings → questions → `call.status: active`.
3. The agent's opening `call.turn` arrives. A human (or `scripts/replay-demo.mjs`) answers
   via `POST /api/dev/sim-answer`; the agent's follow-up arrives as the next `call.turn`.
4. Repeat until the agent ends the call itself → `intake.ready`.

The Telnyx path emits the **identical event stream** — the run view needs no
transport-specific code.
