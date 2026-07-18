// Mirrors API_CONTRACT.md § Core types exactly. snake_case on purpose.

export type Station = "nurse" | "cardiology" | "imaging" | "doctor";
export type Role = "staff" | "patient";
export type Priority = "high" | "normal";
export type NodeStatus = "done" | "active" | "pending";

export interface Patient {
  id: number;
  name: string;
  dob: string;
  summary_text: string;
}

export interface Visit {
  id: number;
  patient_id: number;
  date: string;
  intent_text: string;
  plan_confirmed: boolean;
}

export interface JourneyNode {
  id: number;
  visit_id: number;
  station: Station;
  specialist_name: string;
  specialist_profile: string;
  goals: string[];
  status: NodeStatus;
  position: number;
}

export interface JourneyEdge {
  id: number;
  from_node_id: number;
  to_node_id: number;
}

export interface Journey {
  nodes: JourneyNode[];
  edges: JourneyEdge[];
}

export interface Guardrail {
  id: number;
  num: number;
  condition_text: string;
  action_text: string;
}

export interface NodeBrief {
  id: number;
  node_id: number;
  from_node_id: number;
  from_station: Station;
  summary_md: string;
  action_items: { text: string; priority: Priority }[];
  created_ts: string;
}

export interface Todo {
  id: number;
  visit_id: number;
  created_by_node_id: number;
  for_node_id: number;
  text: string;
  priority: Priority;
  status: "open" | "done";
}

export interface TranscriptTurn {
  id: number;
  session_id: number;
  speaker: Role;
  text: string;
  ts: string;
}

export interface Suggestion {
  id: number;
  session_id: number;
  kind: "question" | "action" | "observation";
  text: string;
  reason: string;
  priority: Priority;
  ts: string;
}

export interface GuardrailAlert {
  id: number;
  session_id: number;
  guardrail_id: number;
  guardrail_num: number;
  condition_text: string;
  triggered_by: string;
  action: string;
  ts: string;
}

export interface Contradiction {
  id: number;
  session_id: number;
  statement: string;
  conflicts_with: string;
  severity: "high" | "note";
  suggested_probe: string;
  ts: string;
}

export interface ChartEntry {
  id: number;
  visit_id: number;
  node_id: number;
  node_station: Station;
  category: "symptom" | "vital" | "finding" | "note" | "contradiction";
  text: string;
  ts: string;
}

export interface JourneyMutation {
  id: number;
  session_id: number;
  guardrail_id: number;
  description: string;
  insert_station: Station;
  before_node_id: number;
  status: "proposed" | "accepted" | "dismissed";
  ts: string;
}

// Patient Context Model (Phase 1) ------------------------------------------
export type SlotStatus = "known" | "uncertain" | "stale" | "contradicted" | "missing";

// One provenance ledger entry — the quality trail behind a belief.
export interface ContextLedgerEntry {
  id: number;
  slot_key: string;
  value: string;
  status: SlotStatus;
  confidence: number;
  source_kind: "seed" | "speech" | "typed" | "image" | "measurement" | "inferred";
  source_channel: string;
  actor_role: string;
  actor_id: string;
  actor_name: string;
  from_patient: boolean;
  extracted_from_speech: boolean;
  model: string;
  session_id: number | null;
  node_id: number | null;
  turn_id: number | null;
  raw_quote: string;
  ts: string;
}

export interface ContextSlot {
  id: number;
  visit_id: number;
  key: string;
  label: string;
  category: string;
  status: SlotStatus;
  value: string;
  confidence: number;
  required: boolean;
  why_required: string;
  updated_ts: string;
  provenance: ContextLedgerEntry | null;
}

export interface ContextCompleteness {
  total_required: number;
  counts: Record<SlotStatus, number>;
  open_gaps: number;
  percent: number;
}

export interface PatientContext {
  visit_id: number;
  slots: ContextSlot[];
  completeness: ContextCompleteness;
  ledger: ContextLedgerEntry[];
}

export interface Appointment {
  node_id: number;
  patient_id: number;
  patient_name: string;
  time: string;
  station: Station;
  status: NodeStatus;
}

export interface PatientPage {
  patient: Patient;
  visit: Visit;
  journey: Journey;
  guardrails: Guardrail[];
  briefs: NodeBrief[];
  todos: Todo[];
  chart: ChartEntry[];
  active_session_id: number | null;
}

export interface SessionInfo {
  id: number;
  node_id: number;
  started_ts: string;
  ended_ts: string | null;
}

export interface SessionState {
  session: SessionInfo;
  turns: TranscriptTurn[];
  suggestions: Suggestion[];
  alerts: GuardrailAlert[];
  contradictions: Contradiction[];
  chart_entries: ChartEntry[];
  todos: Todo[];
  pending_mutation: JourneyMutation | null;
  last_seq: number;
}

// WebSocket 2 — discriminated union per API_CONTRACT.md
export type ServerEvent =
  | { seq: number; ts: string; type: "transcript.partial"; data: { speaker: Role; text: string } }
  | { seq: number; ts: string; type: "transcript.turn"; data: TranscriptTurn }
  | { seq: number; ts: string; type: "tick.started"; data: { turn_id: number } }
  | { seq: number; ts: string; type: "suggestion"; data: Suggestion }
  | { seq: number; ts: string; type: "guardrail.alert"; data: GuardrailAlert }
  | { seq: number; ts: string; type: "contradiction"; data: Contradiction }
  | { seq: number; ts: string; type: "chart.entry"; data: ChartEntry }
  | { seq: number; ts: string; type: "context.slot_updated"; data: { slot: ContextSlot; completeness: ContextCompleteness } }
  | { seq: number; ts: string; type: "todo.update"; data: { op: "add" | "complete" | "edit"; todo: Todo } }
  | { seq: number; ts: string; type: "journey.mutation_proposed"; data: JourneyMutation }
  | { seq: number; ts: string; type: "journey.updated"; data: Journey }
  | { seq: number; ts: string; type: "session.compile.started"; data: Record<string, never> }
  | { seq: number; ts: string; type: "session.compile.done"; data: { briefs: NodeBrief[]; todos: Todo[] } }
  | { seq: number; ts: string; type: "session.ended"; data: Record<string, never> }
  | { seq: number; ts: string; type: "error"; data: { code: string; message: string } };
