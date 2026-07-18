// The one render pipeline: /ws/session/{id}/events + REST rehydration.
// Contract rules implemented here so screens stay dumb:
//  - rehydrate via GET /api/sessions/{id} on connect AND reconnect
//  - dedupe events by (type, data.id) so overlap with rehydration is safe
//  - transcript.partial replaces in place; cleared by the finalized turn
//  - tick.started shows "DOC is thinking"; cleared by the first card or next tick

import { useCallback, useEffect, useReducer, useRef, useState } from "react";
import { api } from "./api";
import type {
  ChartEntry,
  Contradiction,
  GuardrailAlert,
  Journey,
  JourneyMutation,
  NodeBrief,
  Role,
  ServerEvent,
  SessionInfo,
  Suggestion,
  Todo,
  TranscriptTurn,
} from "./types";

export interface SessionViewState {
  session: SessionInfo | null;
  turns: TranscriptTurn[];
  partial: { speaker: Role; text: string } | null;
  suggestions: Suggestion[];
  alerts: GuardrailAlert[];
  contradictions: Contradiction[];
  chartEntries: ChartEntry[];
  todos: Todo[];
  pendingMutation: JourneyMutation | null;
  journey: Journey | null; // set only when a journey.updated arrives mid-session
  thinking: boolean;
  compiling: boolean;
  compileBriefs: NodeBrief[];
  ended: boolean;
  error: string | null;
}

const initial: SessionViewState = {
  session: null,
  turns: [],
  partial: null,
  suggestions: [],
  alerts: [],
  contradictions: [],
  chartEntries: [],
  todos: [],
  pendingMutation: null,
  journey: null,
  thinking: false,
  compiling: false,
  compileBriefs: [],
  ended: false,
  error: null,
};

type Action =
  | { kind: "rehydrate"; state: Partial<SessionViewState> }
  | { kind: "event"; event: ServerEvent }
  | { kind: "mutation_resolved"; mutationId: number };

function upsert<T extends { id: number }>(list: T[], item: T): T[] {
  return list.some((x) => x.id === item.id)
    ? list.map((x) => (x.id === item.id ? item : x))
    : [...list, item];
}

function reducer(s: SessionViewState, a: Action): SessionViewState {
  if (a.kind === "rehydrate") return { ...s, ...a.state };
  if (a.kind === "mutation_resolved") {
    return s.pendingMutation?.id === a.mutationId ? { ...s, pendingMutation: null } : s;
  }
  const e = a.event;
  switch (e.type) {
    case "transcript.partial":
      return { ...s, partial: e.data };
    case "transcript.turn":
      return { ...s, partial: null, turns: upsert(s.turns, e.data) };
    case "tick.started":
      return { ...s, thinking: true };
    case "suggestion":
      return { ...s, thinking: false, suggestions: upsert(s.suggestions, e.data) };
    case "guardrail.alert":
      return { ...s, thinking: false, alerts: upsert(s.alerts, e.data) };
    case "contradiction":
      return { ...s, thinking: false, contradictions: upsert(s.contradictions, e.data) };
    case "chart.entry":
      return { ...s, chartEntries: upsert(s.chartEntries, e.data) };
    case "todo.update":
      return { ...s, todos: upsert(s.todos, e.data.todo) };
    case "journey.mutation_proposed":
      return { ...s, pendingMutation: e.data };
    case "journey.updated":
      return { ...s, journey: e.data, pendingMutation: null };
    case "session.compile.started":
      return { ...s, compiling: true, thinking: false };
    case "session.compile.done":
      return { ...s, compiling: false, compileBriefs: e.data.briefs, todos: e.data.todos };
    case "session.ended":
      return {
        ...s,
        ended: true,
        compiling: false,
        thinking: false,
        partial: null,
        session: s.session ? { ...s.session, ended_ts: e.ts } : s.session,
      };
    case "error":
      return { ...s, error: e.data.message };
    default:
      return s;
  }
}

export function useSessionEvents(sessionId: number | null) {
  const [state, dispatch] = useReducer(reducer, initial);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const closedRef = useRef(false);

  const rehydrate = useCallback(async (id: number) => {
    const full = await api.session(id);
    dispatch({
      kind: "rehydrate",
      state: {
        session: full.session,
        turns: full.turns,
        suggestions: full.suggestions,
        alerts: full.alerts,
        contradictions: full.contradictions,
        chartEntries: full.chart_entries,
        todos: full.todos,
        pendingMutation: full.pending_mutation,
        ended: full.session.ended_ts !== null,
      },
    });
  }, []);

  useEffect(() => {
    if (sessionId === null) return;
    closedRef.current = false;
    let retryTimer: number | undefined;

    const connect = () => {
      if (closedRef.current) return;
      const ws = new WebSocket(
        `ws://${location.hostname}:8000/ws/session/${sessionId}/events`,
      );
      wsRef.current = ws;
      ws.onopen = () => {
        setConnected(true);
        // Rehydrate on every (re)connect; events dedupe by id, so overlap is safe.
        rehydrate(sessionId).catch(() => undefined);
      };
      ws.onmessage = (m) => {
        try {
          dispatch({ kind: "event", event: JSON.parse(m.data) as ServerEvent });
        } catch {
          /* ignore malformed frame */
        }
      };
      ws.onclose = () => {
        setConnected(false);
        if (!closedRef.current) retryTimer = window.setTimeout(connect, 1500);
      };
      ws.onerror = () => ws.close();
    };

    connect();
    return () => {
      closedRef.current = true;
      window.clearTimeout(retryTimer);
      wsRef.current?.close();
    };
  }, [sessionId, rehydrate]);

  const resolveMutation = useCallback((mutationId: number) => {
    dispatch({ kind: "mutation_resolved", mutationId });
  }, []);

  return { state, connected, resolveMutation };
}
