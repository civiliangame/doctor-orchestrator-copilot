// The one render pipeline for the run view: /ws/runs/{id}/events + REST rehydration.
// Contract rules implemented here so the screen stays dumb:
//  - on (re)connect, open the WS first and buffer frames, then GET /api/runs/{id},
//    replace state wholesale, and replay only buffered frames with seq > last_seq
//  - every entity list upserts by id, so overlapping rehydrate + events
//    (the contract's "dedupe by (type, data.id)") is always safe
//  - question.status / run.status / call.status upsert the same rows in place

import { useCallback, useEffect, useReducer, useRef, useState } from "react";
import { api, wsUrl } from "./api";
import type {
  Answer,
  Call,
  CallTurn,
  Finding,
  Intake,
  InterviewQuestion,
  Run,
  RunEvent,
  Specialist,
  SpecialistTask,
} from "./types";

export interface RunViewState {
  run: Run | null;
  specialists: Specialist[];
  findings: Finding[];
  questions: InterviewQuestion[];
  tasks: SpecialistTask[];
  call: Call | null;
  callTurns: CallTurn[];
  answers: Answer[];
  intake: Intake | null;
  planReady: boolean;
  error: string | null;
}

const initial: RunViewState = {
  run: null,
  specialists: [],
  findings: [],
  questions: [],
  tasks: [],
  call: null,
  callTurns: [],
  answers: [],
  intake: null,
  planReady: false,
  error: null,
};

type Action =
  | { kind: "rehydrate"; state: RunViewState }
  | { kind: "event"; event: RunEvent }
  | { kind: "error"; message: string };

function upsert<T extends { id: number }>(list: T[], item: T): T[] {
  return list.some((x) => x.id === item.id)
    ? list.map((x) => (x.id === item.id ? item : x))
    : [...list, item];
}

function reducer(s: RunViewState, a: Action): RunViewState {
  if (a.kind === "rehydrate") return a.state;
  if (a.kind === "error") return { ...s, error: a.message };
  const e = a.event;
  switch (e.type) {
    case "run.status":
      return { ...s, run: e.data };
    case "specialist.selected":
    case "specialist.done":
      return { ...s, specialists: upsert(s.specialists, e.data) };
    case "finding.created":
      return { ...s, findings: upsert(s.findings, e.data) };
    case "plan.question":
    case "question.status":
      return { ...s, questions: upsert(s.questions, e.data) };
    case "plan.task":
      return { ...s, tasks: upsert(s.tasks, e.data) };
    case "plan.ready":
      return { ...s, planReady: true };
    case "call.status":
      return { ...s, call: e.data };
    case "call.turn":
      return { ...s, callTurns: upsert(s.callTurns, e.data) };
    case "answer.recorded":
      return { ...s, answers: upsert(s.answers, e.data) };
    case "intake.ready":
      return { ...s, intake: e.data };
    default:
      return s;
  }
}

export function useRunEvents(runId: number | null) {
  const [state, dispatch] = useReducer(reducer, initial);
  const [connected, setConnected] = useState(false);
  const closedRef = useRef(false);

  const rehydrate = useCallback(async (id: number): Promise<number> => {
    const full = await api.run(id);
    dispatch({
      kind: "rehydrate",
      state: {
        run: full.run,
        specialists: full.specialists,
        findings: full.findings,
        questions: full.questions,
        tasks: full.specialist_tasks,
        call: full.call,
        callTurns: full.call_turns,
        answers: full.answers,
        intake: full.intake,
        planReady:
          full.questions.length > 0 &&
          ["calling", "compiling", "done"].includes(full.run.status),
        error: null,
      },
    });
    return full.last_seq;
  }, []);

  useEffect(() => {
    if (runId === null) return;
    closedRef.current = false;
    let retryTimer: number | undefined;
    let ws: WebSocket | null = null;

    const connect = () => {
      if (closedRef.current) return;
      ws = new WebSocket(wsUrl(`/ws/runs/${runId}/events`));
      const sock = ws;

      // Buffer frames until rehydration lands, then replay only newer seqs.
      let buffer: RunEvent[] | null = [];
      const onEvent = (ev: RunEvent) => {
        if (buffer) buffer.push(ev);
        else dispatch({ kind: "event", event: ev });
      };

      sock.onopen = () => {
        setConnected(true);
        rehydrate(runId)
          .then((lastSeq) => {
            const pending = buffer ?? [];
            buffer = null;
            for (const ev of pending) {
              if (ev.seq > lastSeq) dispatch({ kind: "event", event: ev });
            }
          })
          .catch((err: unknown) => {
            buffer = null; // fall back to raw event stream
            dispatch({
              kind: "error",
              message: err instanceof Error ? err.message : "rehydration failed",
            });
          });
      };
      sock.onmessage = (m) => {
        try {
          onEvent(JSON.parse(m.data) as RunEvent);
        } catch {
          /* ignore malformed frame */
        }
      };
      sock.onclose = () => {
        setConnected(false);
        if (!closedRef.current) retryTimer = window.setTimeout(connect, 1500);
      };
      sock.onerror = () => sock.close();
    };

    connect();
    return () => {
      closedRef.current = true;
      window.clearTimeout(retryTimer);
      ws?.close();
    };
  }, [runId, rehydrate]);

  return { state, connected };
}
