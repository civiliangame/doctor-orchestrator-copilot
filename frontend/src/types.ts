// Types mirror API_CONTRACT.md (v2 — context-rot pivot) exactly.
// snake_case keys, integer ids, ISO-8601 UTC timestamps.

export type FindingKind = "contradiction" | "gap" | "ambiguity";
export type Severity = "high" | "normal";
export type RunStatus = "analyzing" | "planning" | "calling" | "compiling" | "done" | "failed";
export type QuestionStatus = "pending" | "asking" | "answered" | "deferred";
export type CallTransport = "sim" | "telnyx";
export type CallStatus = "dialing" | "active" | "ended";
export type CallSpeaker = "agent" | "patient";

export interface Patient {
  id: number;
  name: string;
  dob: string;
  phone: string;
}

export interface Document {
  id: number;
  patient_id: number;
  title: string;
  doc_type: string;
  author: string;
  date: string;
  content_md: string;
}

export interface Run {
  id: number;
  patient_id: number;
  status: RunStatus;
  transport: CallTransport;
  started_ts: string;
  ended_ts: string | null;
}

export interface Specialist {
  id: number;
  run_id: number;
  key: string;
  display_name: string;
  rationale: string;
  status: "running" | "done";
}

export interface Finding {
  id: number;
  run_id: number;
  specialist_id: number | null; // null when discovered live on the call
  kind: FindingKind;
  severity: Severity;
  title: string;
  detail: string;
  quotes: { doc_title: string; quote: string }[];
  patient_answerable: boolean;
}

export interface InterviewQuestion {
  id: number;
  run_id: number;
  finding_ids: number[];
  order: number;
  question: string;
  sub_questions: string[];
  completeness_criteria: string;
  status: QuestionStatus;
}

export interface SpecialistTask {
  id: number;
  run_id: number;
  finding_id: number;
  for_specialist: string;
  instruction: string;
  why: string;
}

export interface Call {
  id: number;
  run_id: number;
  transport: CallTransport;
  status: CallStatus;
  started_ts: string;
  ended_ts: string | null;
}

export interface CallTurn {
  id: number;
  call_id: number;
  speaker: CallSpeaker;
  text: string;
  ts: string;
}

export interface Answer {
  id: number;
  question_id: number;
  summary_text: string;
  complete: boolean;
  ts: string;
}

export interface Intake {
  id: number;
  run_id: number;
  chief_complaint: string;
  hpi_md: string;
  meds_reconciliation_md: string;
  resolved_contradictions_md: string;
  open_items_md: string;
  created_ts: string;
}

// ---------- REST payloads ----------

export interface PatientPage {
  patient: Patient;
  documents: Document[];
  latest_run: Run | null;
  latest_intake: Intake | null;
  specialist_tasks: SpecialistTask[];
}

export interface RunState {
  run: Run;
  specialists: Specialist[];
  findings: Finding[];
  questions: InterviewQuestion[];
  specialist_tasks: SpecialistTask[];
  call: Call | null;
  call_turns: CallTurn[];
  answers: Answer[];
  intake: Intake | null;
  last_seq: number;
}

// ---------- WebSocket event union ----------

export interface PlanReady {
  id: number;
  question_count: number;
  task_count: number;
}

interface Ev<T extends string, D> {
  seq: number;
  ts: string;
  type: T;
  data: D;
}

export type RunEvent =
  | Ev<"run.status", Run>
  | Ev<"specialist.selected", Specialist>
  | Ev<"finding.created", Finding>
  | Ev<"specialist.done", Specialist>
  | Ev<"plan.question", InterviewQuestion>
  | Ev<"plan.task", SpecialistTask>
  | Ev<"plan.ready", PlanReady>
  | Ev<"call.status", Call>
  | Ev<"call.turn", CallTurn>
  | Ev<"question.status", InterviewQuestion>
  | Ev<"answer.recorded", Answer>
  | Ev<"intake.ready", Intake>;
