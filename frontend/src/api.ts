// REST client — API_CONTRACT.md v2. Backend on :5000 (CORS allows 5173).

import type { CallTransport, PatientPage, Run, RunState } from "./types";

export const API_BASE = `http://${location.hostname}:5000`;

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
  patient: (patientId: number) => req<PatientPage>("GET", `/api/patients/${patientId}`),

  startRun: (patientId: number, transport: CallTransport) =>
    req<Run>("POST", `/api/patients/${patientId}/runs`, { transport }),

  run: (runId: number) => req<RunState>("GET", `/api/runs/${runId}`),

  devReset: () => req<{ ok: boolean }>("POST", "/api/dev/reset"),

  devSimAnswer: (callId: number, text: string) =>
    req<unknown>("POST", "/api/dev/sim-answer", { call_id: callId, text }),

  devHangup: (callId: number) =>
    req<unknown>("POST", "/api/dev/hangup", { call_id: callId }),
};

export const wsUrl = (path: string) => `ws://${location.hostname}:5000${path}`;
