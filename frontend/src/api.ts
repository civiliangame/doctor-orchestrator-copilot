// REST client — API_CONTRACT.md. Base is the backend directly (CORS allows 5173).

import type {
  Appointment,
  ChartEntry,
  Guardrail,
  Journey,
  JourneyMutation,
  PatientPage,
  Role,
  SessionState,
  Station,
  TranscriptTurn,
} from "./types";

export const API_BASE = `http://${location.hostname}:8000`;

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(status: number, code: string, message: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

async function req<T>(method: string, path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers: body !== undefined ? { "content-type": "application/json" } : undefined,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    let code = "http_error";
    let message = `${method} ${path} failed (${res.status})`;
    try {
      const j = await res.json();
      if (j?.error) {
        code = j.error.code;
        message = j.error.message;
      }
    } catch {
      /* non-JSON error body */
    }
    throw new ApiError(res.status, code, message);
  }
  return res.json();
}

export const api = {
  appointments: (station: Station) =>
    req<{ appointments: Appointment[] }>("GET", `/api/appointments?station=${station}`),

  patient: (patientId: number, nodeId: number) =>
    req<PatientPage>("GET", `/api/patients/${patientId}?node_id=${nodeId}`),

  planGenerate: (visitId: number, intentText: string) =>
    req<{ journey: Journey; guardrails: Guardrail[] }>(
      "POST", `/api/visits/${visitId}/plan/generate`, { intent_text: intentText },
    ),

  planConfirm: (
    visitId: number,
    nodes: { id: number; goals: string[] }[],
    guardrails: { id: number; condition_text: string; action_text: string }[],
  ) =>
    req<{ journey: Journey; guardrails: Guardrail[] }>(
      "POST", `/api/visits/${visitId}/plan/confirm`, { nodes, guardrails },
    ),

  sessionCreate: (nodeId: number) =>
    req<{ session_id: number; events_url: string; audio_url: string }>(
      "POST", "/api/sessions", { node_id: nodeId },
    ),

  session: (sessionId: number) => req<SessionState>("GET", `/api/sessions/${sessionId}`),

  sessionEnd: (sessionId: number) =>
    req<{ compiling: boolean }>("POST", `/api/sessions/${sessionId}/end`),

  mutationAccept: (mutationId: number) =>
    req<{ mutation: JourneyMutation; journey: Journey }>(
      "POST", `/api/mutations/${mutationId}/accept`,
    ),

  mutationDismiss: (mutationId: number) =>
    req<{ mutation: JourneyMutation; journey: Journey }>(
      "POST", `/api/mutations/${mutationId}/dismiss`,
    ),

  uploadImage: async (nodeId: number, file: File): Promise<{ findings: ChartEntry[] }> => {
    const form = new FormData();
    form.append("image", file);
    const res = await fetch(`${API_BASE}/api/nodes/${nodeId}/images`, {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      let code = "vision_failed";
      let message = `upload failed (${res.status})`;
      try {
        const j = await res.json();
        if (j?.error) {
          code = j.error.code;
          message = j.error.message;
        }
      } catch { /* empty */ }
      throw new ApiError(res.status, code, message);
    }
    return res.json();
  },

  devInjectTurn: (sessionId: number, speaker: Role, text: string) =>
    req<TranscriptTurn>("POST", "/api/dev/inject-turn", {
      session_id: sessionId, speaker, text,
    }),

  devEndPatientTurn: (sessionId: number) =>
    req<{ flushed: boolean }>("POST", "/api/dev/end-patient-turn", { session_id: sessionId }),

  devReset: () => req<{ ok: boolean }>("POST", "/api/dev/reset"),
};

export const wsUrl = (path: string) => `ws://${location.hostname}:8000${path}`;
