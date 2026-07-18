// Screen 2 — the run view. One screen, four stages that light up in order:
// specialist panel → interview plan → live call → compiled intake.
// Everything arrives over /ws/runs/{id}/events (rehydrated via GET /api/runs/{id}).

import { useEffect, useMemo, useRef, useState } from "react";
import { api } from "../api";
import { Markdown } from "../markdown";
import { useRunEvents } from "../useRunEvents";
import type {
  Answer,
  CallTurn,
  Finding,
  InterviewQuestion,
  RunStatus,
  Specialist,
  SpecialistTask,
} from "../types";

const STAGE_OF_STATUS: Record<RunStatus, number> = {
  analyzing: 0,
  planning: 1,
  calling: 2,
  compiling: 3,
  done: 4, // everything finished — all four stages render as done
  failed: -1,
};

const KIND_LABEL: Record<Finding["kind"], string> = {
  contradiction: "contradiction",
  gap: "gap",
  ambiguity: "ambiguity",
};

function Spinner() {
  return <span className="spinner" aria-label="running" />;
}

function StagePanel(props: {
  n: number;
  title: string;
  state: "idle" | "active" | "done";
  children: React.ReactNode;
}) {
  return (
    <section className={`stage stage-${props.state}`}>
      <header className="stage-head">
        <span className="stage-num">{props.state === "done" ? "✓" : props.n}</span>
        <h2 className="stage-title">{props.title}</h2>
        {props.state === "active" && <Spinner />}
      </header>
      <div className="stage-body">{props.children}</div>
    </section>
  );
}

function FindingCard({ f }: { f: Finding }) {
  return (
    <article className={`finding kind-${f.kind} sev-${f.severity} card-in`}>
      <header className="finding-head">
        <span className={`kind-badge kind-${f.kind}`}>{KIND_LABEL[f.kind]}</span>
        {f.severity === "high" && <span className="sev-badge">high</span>}
        {!f.patient_answerable && <span className="inperson-badge">needs in-person</span>}
      </header>
      <h3 className="finding-title">{f.title}</h3>
      <p className="finding-detail">{f.detail}</p>
      {f.quotes.length > 0 && (
        <div className="finding-quotes">
          {f.quotes.map((q, i) => (
            <blockquote key={i} className="quote">
              <span className="quote-text">“{q.quote}”</span>
              <span className="quote-doc">— {q.doc_title}</span>
            </blockquote>
          ))}
        </div>
      )}
    </article>
  );
}

function SpecialistBlock({
  spec,
  findings,
}: {
  spec: Specialist;
  findings: Finding[];
}) {
  return (
    <div className="spec-block card-in">
      <header className="spec-head">
        <span className="spec-name">{spec.display_name}</span>
        {spec.status === "running" ? (
          <span className="spec-status running">
            <Spinner /> reading the chart…
          </span>
        ) : (
          <span className="spec-status done">✓ done</span>
        )}
      </header>
      <p className="spec-rationale">{spec.rationale}</p>
      <div className="spec-findings">
        {findings.map((f) => (
          <FindingCard key={f.id} f={f} />
        ))}
      </div>
    </div>
  );
}

function QuestionCard({ q }: { q: InterviewQuestion }) {
  return (
    <article className={`question q-${q.status} card-in`}>
      <header className="question-head">
        <span className="q-order">Q{q.order + 1}</span>
        <span className={`q-status q-status-${q.status}`}>{q.status}</span>
      </header>
      <div className="q-text">{q.question}</div>
      {q.sub_questions.length > 0 && (
        <ul className="q-subs">
          {q.sub_questions.map((sq, i) => (
            <li key={i}>{sq}</li>
          ))}
        </ul>
      )}
      <div className="q-criteria">
        <span className="q-criteria-label">complete when:</span> {q.completeness_criteria}
      </div>
    </article>
  );
}

function TaskRow({ t }: { t: SpecialistTask }) {
  return (
    <li className="task-item card-in">
      <span className="task-check">☐</span>
      <div>
        <div className="task-instruction">{t.instruction}</div>
        <div className="task-meta">
          <span className="task-for">{t.for_specialist.replace(/_/g, " ")}</span>
          <span className="task-why">{t.why}</span>
        </div>
      </div>
    </li>
  );
}

type FeedItem =
  | { kind: "turn"; ts: string; id: number; turn: CallTurn }
  | { kind: "answer"; ts: string; id: number; answer: Answer };

export function RunScreen({ runId }: { runId: number }) {
  const { state, connected } = useRunEvents(runId);
  const { run, specialists, findings, questions, tasks, call, callTurns, answers, intake } =
    state;

  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const feedRef = useRef<HTMLDivElement | null>(null);

  const stage = run ? STAGE_OF_STATUS[run.status] : 0;
  const failed = run?.status === "failed";

  const specFindings = useMemo(() => {
    const by = new Map<number, Finding[]>();
    for (const f of findings) {
      if (f.specialist_id === null) continue;
      const list = by.get(f.specialist_id) ?? [];
      list.push(f);
      by.set(f.specialist_id, list);
    }
    return by;
  }, [findings]);
  const liveFindings = useMemo(
    () => findings.filter((f) => f.specialist_id === null),
    [findings],
  );

  const sortedQuestions = useMemo(
    () => [...questions].sort((a, b) => a.order - b.order),
    [questions],
  );

  const feed = useMemo<FeedItem[]>(() => {
    const items: FeedItem[] = [
      ...callTurns.map((t): FeedItem => ({ kind: "turn", ts: t.ts, id: t.id, turn: t })),
      ...answers.map((a): FeedItem => ({ kind: "answer", ts: a.ts, id: a.id, answer: a })),
    ];
    return items.sort((a, b) => (a.ts < b.ts ? -1 : a.ts > b.ts ? 1 : a.id - b.id));
  }, [callTurns, answers]);

  // keep the transcript pinned to the latest turn
  useEffect(() => {
    const el = feedRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [feed.length]);

  const showSimInput =
    call !== null && call.status === "active" && (run?.transport ?? "sim") === "sim";

  const sendSimAnswer = async () => {
    if (!call || !draft.trim() || sending) return;
    setSending(true);
    try {
      await api.devSimAnswer(call.id, draft.trim());
      setDraft("");
    } catch {
      /* keep the draft so the operator can retry */
    } finally {
      setSending(false);
    }
  };

  const stageState = (n: number): "idle" | "active" | "done" =>
    failed ? (n < 1 ? "done" : "idle") : stage > n ? "done" : stage === n ? "active" : "idle";

  return (
    <div className="run-screen">
      <header className="run-head">
        <h1 className="run-title">
          Cleanup run <span className="run-id">#{runId}</span>
        </h1>
        <div className="run-status-row">
          {run && (
            <span className={`run-status status-${run.status}`}>
              {run.status === "done" ? "✓ done" : run.status}
            </span>
          )}
          <span className={`conn-dot ${connected ? "on" : "off"}`} title={connected ? "live" : "reconnecting"} />
          {run?.status === "done" && (
            <a className="payoff-link" href="#/">
              View patient page — before / after →
            </a>
          )}
        </div>
      </header>

      {state.error && <div className="error-banner">{state.error}</div>}
      {failed && <div className="error-banner">Run failed — check the backend logs.</div>}

      <div className="stages">
        <StagePanel n={1} title="Specialist panel" state={stageState(0)}>
          {specialists.length === 0 && (
            <p className="muted stage-empty">Triage is reading the chart and picking specialists…</p>
          )}
          {specialists.map((sp) => (
            <SpecialistBlock key={sp.id} spec={sp} findings={specFindings.get(sp.id) ?? []} />
          ))}
          {liveFindings.length > 0 && (
            <div className="spec-block live-block card-in">
              <header className="spec-head">
                <span className="spec-name">Found live on the call</span>
              </header>
              <div className="spec-findings">
                {liveFindings.map((f) => (
                  <FindingCard key={f.id} f={f} />
                ))}
              </div>
            </div>
          )}
        </StagePanel>

        <StagePanel n={2} title="Interview plan" state={stageState(1)}>
          {sortedQuestions.length === 0 && (
            <p className="muted stage-empty">
              {stage >= 1
                ? "The orchestrator is turning findings into questions…"
                : "Waiting on the specialist panel."}
            </p>
          )}
          {sortedQuestions.map((q) => (
            <QuestionCard key={q.id} q={q} />
          ))}
          {tasks.length > 0 && (
            <div className="plan-tasks">
              <h3 className="plan-tasks-title">For the visit (can’t ask by phone)</h3>
              <ul className="task-list">
                {tasks.map((t) => (
                  <TaskRow key={t.id} t={t} />
                ))}
              </ul>
            </div>
          )}
        </StagePanel>

        <StagePanel n={3} title="Live call" state={stageState(2)}>
          {call ? (
            <div className={`call-banner call-${call.status} card-in`}>
              {call.status === "dialing" && (
                <>
                  <Spinner /> Dialing the patient…
                </>
              )}
              {call.status === "active" && <>● Call in progress — {call.transport}</>}
              {call.status === "ended" && <>Call ended</>}
            </div>
          ) : (
            <p className="muted stage-empty">
              {stage >= 2 ? "Placing the call…" : "The call fires as soon as the plan is ready."}
            </p>
          )}
          <div className="call-feed" ref={feedRef}>
            {feed.map((item) =>
              item.kind === "turn" ? (
                <div
                  key={`t${item.id}`}
                  className={`turn turn-${item.turn.speaker} card-in`}
                >
                  <span className="turn-speaker">
                    {item.turn.speaker === "agent" ? "DOC" : "Patient"}
                  </span>
                  <div className="turn-bubble">{item.turn.text}</div>
                </div>
              ) : (
                <div key={`a${item.id}`} className="answer-card card-in">
                  <span className="answer-check">✓ recorded</span>
                  <span className="answer-text">{item.answer.summary_text}</span>
                  {!item.answer.complete && <span className="answer-partial">partial</span>}
                </div>
              ),
            )}
          </div>
          {showSimInput && (
            <form
              className="sim-input"
              onSubmit={(e) => {
                e.preventDefault();
                void sendSimAnswer();
              }}
            >
              <input
                value={draft}
                onChange={(e) => setDraft(e.target.value)}
                placeholder="answer as the patient (dev sim)…"
                disabled={sending}
              />
              <button type="submit" disabled={sending || !draft.trim()}>
                {sending ? "…" : "Send"}
              </button>
            </form>
          )}
        </StagePanel>

        <StagePanel n={4} title="Compiled intake" state={stageState(3)}>
          {intake ? (
            <div className="intake card-in">
              <div className="intake-kicker">Pre-Visit Intake Brief</div>
              <h3 className="intake-cc">{intake.chief_complaint}</h3>
              <section className="intake-section">
                <h4>History of Present Illness</h4>
                <Markdown text={intake.hpi_md} />
              </section>
              <section className="intake-section">
                <h4>Medication Reconciliation</h4>
                <Markdown text={intake.meds_reconciliation_md} />
              </section>
              <section className="intake-section">
                <h4>Resolved Contradictions</h4>
                <Markdown text={intake.resolved_contradictions_md} />
              </section>
              <section className="intake-section">
                <h4>Open Items</h4>
                <Markdown text={intake.open_items_md} />
              </section>
              {run?.status === "done" && (
                <a className="payoff-link big" href="#/">
                  View patient page — before / after →
                </a>
              )}
            </div>
          ) : (
            <p className="muted stage-empty">
              {run?.status === "compiling"
                ? "Compiling every recorded answer into one clean intake…"
                : "The intake compiles when the call wraps."}
            </p>
          )}
        </StagePanel>
      </div>
    </div>
  );
}
