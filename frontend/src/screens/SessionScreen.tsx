// Screen 4 — live session (DEMO_SCRIPT.md Beat A, the climax).
// All rendered state comes from useSessionEvents; useMic only pushes audio.
// Dev flow (inject-turn / replay-demo.mjs) must work with the mic off.

import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "../api";
import { useSessionEvents } from "../useSessionEvents";
import { useMic } from "../useMic";
import { JourneyTimeline } from "../components/JourneyTimeline";
import type {
  Contradiction,
  GuardrailAlert,
  Journey,
  JourneyMutation,
  Patient,
  Station,
  Suggestion,
} from "../types";

interface SessionScreenProps {
  sessionId: number;
  nodeId: number;
  patientId: number;
  station: Station;
}

const cap = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);

export function SessionScreen({ sessionId, nodeId, patientId, station }: SessionScreenProps) {
  const { state, connected, resolveMutation } = useSessionEvents(sessionId);
  const mic = useMic(sessionId);

  // Initial journey from the patient page; state.journey (journey.updated) overrides.
  const [initialJourney, setInitialJourney] = useState<Journey | null>(null);
  const [patient, setPatient] = useState<Patient | null>(null);
  useEffect(() => {
    let cancelled = false;
    api
      .patient(patientId, nodeId)
      .then((page) => {
        if (cancelled) return;
        setInitialJourney(page.journey);
        setPatient(page.patient);
      })
      .catch(() => undefined); // non-fatal; timeline appears on journey.updated
    return () => {
      cancelled = true;
    };
  }, [patientId, nodeId]);
  const journey = state.journey ?? initialJourney;

  // Local UI state
  const [localError, setLocalError] = useState<string | null>(null);
  const [dismissedEventError, setDismissedEventError] = useState<string | null>(null);
  const [dismissedMicError, setDismissedMicError] = useState<string | null>(null);
  const [mutationBusy, setMutationBusy] = useState(false);
  const [endBusy, setEndBusy] = useState(false);

  // F8 — off-screen operator key: force end-of-patient-turn (DEMO_SCRIPT H9 fallback).
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== "F8") return;
      e.preventDefault();
      api.devEndPatientTurn(sessionId).catch(() => undefined);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [sessionId]);

  // Auto-scroll transcript on new turns/partials.
  const bottomRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }, [state.turns.length, state.partial?.text]);

  const staffLabel = cap(station);
  const patientLabel = patient?.name ?? "Patient";

  const actOnMutation = useCallback(
    async (mutation: JourneyMutation, accept: boolean) => {
      setMutationBusy(true);
      try {
        if (accept) await api.mutationAccept(mutation.id);
        else await api.mutationDismiss(mutation.id);
        resolveMutation(mutation.id);
      } catch (err) {
        setLocalError(err instanceof Error ? err.message : "Mutation update failed.");
      } finally {
        setMutationBusy(false);
      }
    },
    [resolveMutation],
  );

  const endSession = useCallback(async () => {
    setEndBusy(true);
    try {
      await api.sessionEnd(sessionId);
    } catch (err) {
      setLocalError(err instanceof Error ? err.message : "Could not end the session.");
      setEndBusy(false);
    }
  }, [sessionId]);

  const patientPageHash = `#/patient/${patientId}/${nodeId}`;
  const stationForNode = (id: number): string => {
    const node = journey?.nodes.find((n) => n.id === id);
    return node ? cap(node.station) : `Node ${id}`;
  };

  // Newest-first views (hook accumulates in arrival order).
  const alerts: GuardrailAlert[] = [...state.alerts].reverse();
  const contradictions: Contradiction[] = [...state.contradictions].reverse();
  const suggestions: Suggestion[] = [...state.suggestions].reverse();

  const pending = state.pendingMutation;
  const eventError = state.error && state.error !== dismissedEventError ? state.error : null;
  const micError = mic.error && mic.error !== dismissedMicError ? mic.error : null;
  const overlayOpen = state.compiling || state.compileBriefs.length > 0;

  return (
    <div>
      <div className="session-head">
        <div className="title">
          {patientLabel} — {staffLabel} session
        </div>
        <div className="session-head-tools">
          {state.thinking && (
            <span className="thinking">
              <span className="pulse-dot" /> DOC is thinking
            </span>
          )}
          {!connected && <span className="muted">reconnecting…</span>}
          <button
            onClick={mic.status === "live" ? mic.stop : mic.start}
            disabled={mic.status === "connecting"}
          >
            {mic.status === "live" ? "Stop Mic" : "Start Mic"}
          </button>
          <span className="muted mic-status">mic: {mic.status}</span>
          <button
            className="danger"
            onClick={endSession}
            disabled={endBusy || state.compiling || state.ended}
          >
            End Session
          </button>
        </div>
      </div>

      {micError && (
        <div className="error-banner">
          {micError}{" "}
          <button className="dismiss" onClick={() => setDismissedMicError(mic.error)}>
            Dismiss
          </button>
        </div>
      )}
      {eventError && (
        <div className="error-banner">
          {eventError}{" "}
          <button className="dismiss" onClick={() => setDismissedEventError(state.error)}>
            Dismiss
          </button>
        </div>
      )}
      {localError && (
        <div className="error-banner">
          {localError}{" "}
          <button className="dismiss" onClick={() => setLocalError(null)}>
            Dismiss
          </button>
        </div>
      )}

      {state.ended && !state.compiling && state.compileBriefs.length === 0 && (
        <div className="ended-banner">
          Session ended. <a href={patientPageHash}>View patient page</a>
        </div>
      )}

      {journey && (
        <div className="panel">
          <h2>Journey</h2>
          <JourneyTimeline journey={journey} />
        </div>
      )}

      <div className="session-grid">
        {/* Transcript column */}
        <div className="session-col">
          <div className="panel">
            <h2>Transcript</h2>
            <div className="transcript-scroll">
              <div className="transcript">
                {state.turns.length === 0 && !state.partial && (
                  <div className="muted">Waiting for the conversation…</div>
                )}
                {state.turns.map((t) => (
                  <div
                    key={t.id}
                    className={`bubble ${t.speaker === "staff" ? "bubble-staff" : "bubble-patient"}`}
                  >
                    <span className="who">{t.speaker === "staff" ? staffLabel : patientLabel}</span>
                    {t.text}
                  </div>
                ))}
                {state.partial && (
                  <div
                    className={`bubble partial ${
                      state.partial.speaker === "staff" ? "bubble-staff" : "bubble-patient"
                    }`}
                  >
                    <span className="who">
                      {state.partial.speaker === "staff" ? staffLabel : patientLabel}
                    </span>
                    {state.partial.text}
                  </div>
                )}
                <div ref={bottomRef} />
              </div>
            </div>
          </div>
        </div>

        {/* DOC column: mutation banner, alerts, contradictions, suggestions */}
        <div className="session-col">
          {pending && (
            <div className="mutation-banner">
              <span className="desc">{pending.description}</span>
              <button
                className="primary"
                disabled={mutationBusy}
                onClick={() => actOnMutation(pending, true)}
              >
                Accept
              </button>
              <button disabled={mutationBusy} onClick={() => actOnMutation(pending, false)}>
                Dismiss
              </button>
            </div>
          )}

          {alerts.map((a) => (
            <div key={a.id} className="card card-alert">
              <span className="card-label">
                ⚠ Guardrail #{a.guardrail_num} — {a.condition_text}
              </span>
              <div className="card-quote">{a.triggered_by}</div>
              <div className="card-action">{a.action}</div>
            </div>
          ))}

          {contradictions.map((c) => (
            <div key={c.id} className="card card-contra">
              <span className="card-label">Contradiction</span>
              <div className="card-quote">{c.statement}</div>
              <div className="card-vs">conflicts with</div>
              <div className="card-quote">{c.conflicts_with}</div>
              <div className="card-probe">{c.suggested_probe}</div>
            </div>
          ))}

          {suggestions.map((s, i) =>
            i < 2 ? (
              <div key={s.id} className="card card-suggestion">
                <span className="card-label">
                  {s.kind} · {s.priority}
                </span>
                <div>{s.text}</div>
                <div className="card-reason">{s.reason}</div>
              </div>
            ) : (
              <div key={s.id} className="card card-suggestion collapsed">
                {s.text}
              </div>
            ),
          )}

          {!pending &&
            alerts.length === 0 &&
            contradictions.length === 0 &&
            suggestions.length === 0 && (
              <div className="muted">DOC cards will appear here as the conversation unfolds.</div>
            )}
        </div>
      </div>

      {overlayOpen && (
        <div className="compile-overlay">
          <div className="compile-box">
            {state.compiling ? (
              <div>
                <span className="spin" /> Compiling handoff…
              </div>
            ) : (
              <>
                <div className="compile-title">Handoff written</div>
                <div className="briefs">
                  {state.compileBriefs.map((b) => (
                    <div key={b.id} className="brief-line">
                      {cap(b.from_station)} → {stationForNode(b.node_id)} ·{" "}
                      {b.action_items.length} action item{b.action_items.length === 1 ? "" : "s"}
                    </div>
                  ))}
                </div>
                <button
                  className="primary big"
                  onClick={() => {
                    location.hash = patientPageHash;
                  }}
                >
                  View patient page
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
