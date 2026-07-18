import { useEffect, useRef } from "react";
import { useTranscriber, Turn } from "./useTranscriber";

const SPEAKER_COLORS = ["#0e7490", "#7c3aed", "#b45309", "#be185d", "#15803d"];

function speakerColor(speaker: string): string {
  const n = parseInt(speaker, 10);
  return SPEAKER_COLORS[(Number.isNaN(n) ? 0 : n - 1) % SPEAKER_COLORS.length];
}

function TurnRow({ turn }: { turn: Turn }) {
  return (
    <div className="turn">
      <span className="speaker-chip" style={{ background: speakerColor(turn.speaker) }}>
        Speaker {turn.speaker}
      </span>
      <p className="turn-text">
        {turn.text.trim()}
        {turn.endpointed && <span className="endpoint-dot" title="end of turn detected" />}
      </p>
    </div>
  );
}

export default function App() {
  const { status, error, turns, interim, start, stop } = useTranscriber();
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [turns, interim]);

  const live = status === "live";
  const busy = status === "connecting" || status === "finishing";

  return (
    <div className="page">
      <header className="header">
        <div>
          <h1>DOC</h1>
          <p className="subtitle">Doctor Orchestrator Copilot — live transcription</p>
        </div>
        <div className="header-right">
          <span className={`status status-${status}`}>
            {live && <span className="pulse" />}
            {status}
          </span>
          <button
            className={live ? "btn stop" : "btn start"}
            disabled={busy}
            onClick={live ? stop : start}
          >
            {live ? "End Session" : busy ? "…" : "Start Session"}
          </button>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="transcript">
        {turns.length === 0 && !interim && (
          <p className="empty">
            Start a session and speak. Remember the grounding line: “Hi, I’m Doctor
            Zhang, how are you doing today?” — the first speaker is always staff.
          </p>
        )}
        {turns.map((t, i) => (
          <TurnRow key={i} turn={t} />
        ))}
        {interim && <p className="interim">{interim}</p>}
        <div ref={bottomRef} />
      </main>

      <footer className="footer">
        Demo system — synthetic data only. Not for clinical use.
      </footer>
    </div>
  );
}
