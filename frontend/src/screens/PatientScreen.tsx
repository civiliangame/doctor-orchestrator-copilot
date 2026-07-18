// Screen 3 — patient page. Doubles as the final payoff view (Dr. Zhang at
// journey end): briefs + action items render BIG, the chart accumulates by
// station with contradictions surviving in amber. Beat C's imaging upload
// also lives here (only when the viewing node is the imaging station).

import { useCallback, useEffect, useState } from "react";
import type { ReactNode } from "react";
import { api } from "../api";
import type { ChartEntry, PatientPage, Station } from "../types";
import { JourneyTimeline } from "../components/JourneyTimeline";

const errMsg = (e: unknown) => (e instanceof Error ? e.message : String(e));

// Minimal markdown for brief bodies: **bold** and line breaks only.
function renderMd(md: string): ReactNode {
  return md.split("\n").map((line, i) => (
    <span key={i}>
      {line
        .split(/\*\*(.+?)\*\*/g)
        .map((part, j) => (j % 2 === 1 ? <strong key={j}>{part}</strong> : part))}
      <br />
    </span>
  ));
}

// Group by node_station in order of first appearance, chronological within.
function groupChart(entries: ChartEntry[]): { station: Station; entries: ChartEntry[] }[] {
  const sorted = [...entries].sort((a, b) => a.ts.localeCompare(b.ts));
  const groups: { station: Station; entries: ChartEntry[] }[] = [];
  const byStation = new Map<Station, ChartEntry[]>();
  for (const e of sorted) {
    let bucket = byStation.get(e.node_station);
    if (!bucket) {
      bucket = [];
      byStation.set(e.node_station, bucket);
      groups.push({ station: e.node_station, entries: bucket });
    }
    bucket.push(e);
  }
  return groups;
}

export function PatientScreen({
  patientId,
  nodeId,
  station,
}: {
  patientId: number;
  nodeId: number;
  station: Station;
}) {
  const [data, setData] = useState<PatientPage | null>(null);
  const [chart, setChart] = useState<ChartEntry[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  // Imaging upload (Beat C)
  const [file, setFile] = useState<File | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadNote, setUploadNote] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoadError(null);
    try {
      const res = await api.patient(patientId, nodeId);
      setData(res);
      setChart(res.chart);
    } catch (e) {
      setLoadError(errMsg(e));
    }
  }, [patientId, nodeId]);

  useEffect(() => {
    setData(null);
    void load();
  }, [load]);

  if (loadError) {
    return (
      <div>
        <div className="error-banner">{loadError}</div>
        <button onClick={() => void load()}>Retry</button>
      </div>
    );
  }
  if (!data) {
    return (
      <p className="muted">
        <span className="spin" /> Loading patient…
      </p>
    );
  }

  const { patient, visit, journey, guardrails, briefs, todos } = data;
  const viewingNode = journey.nodes.find((n) => n.id === nodeId);
  const openTodos = todos.filter((t) => t.status === "open");

  const startSession = async () => {
    setActionError(null);
    setStarting(true);
    try {
      const res = await api.sessionCreate(nodeId);
      location.hash = `#/session/${res.session_id}/${nodeId}/${patientId}`;
    } catch (e) {
      setActionError(errMsg(e));
      setStarting(false);
    }
  };

  const analyze = async () => {
    if (!file) return;
    setAnalyzing(true);
    setUploadError(null);
    setUploadNote(null);
    try {
      const res = await api.uploadImage(nodeId, file);
      setChart((c) => [...c, ...res.findings]);
      setUploadNote(
        `${res.findings.length} finding${res.findings.length === 1 ? "" : "s"} added to the chart — flagged for Dr. Zhang's review.`,
      );
    } catch (e) {
      setUploadError(errMsg(e));
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div>
      <div className="page-head">
        <div>
          <h1 className="screen-title">
            {patient.name} <span className="muted">· DOB {patient.dob}</span>
          </h1>
          <div className="muted">Visit {visit.date}</div>
        </div>
        <div className="head-actions">
          {data.active_session_id !== null ? (
            <button
              className="primary"
              onClick={() => {
                location.hash = `#/session/${data.active_session_id}/${nodeId}/${patientId}`;
              }}
            >
              Resume Session
            </button>
          ) : (
            viewingNode?.status === "active" && (
              <button className="primary big" onClick={() => void startSession()} disabled={starting}>
                {starting ? (
                  <>
                    <span className="spin" /> Starting…
                  </>
                ) : (
                  "Start Session"
                )}
              </button>
            )
          )}
          {station === "doctor" && (
            <button
              onClick={() => {
                location.hash = `#/plan/${visit.id}/${patientId}/${nodeId}`;
              }}
            >
              Plan next visit
            </button>
          )}
        </div>
      </div>
      {actionError && <div className="error-banner">{actionError}</div>}

      <div className="panel">
        <h2>Visit journey</h2>
        <JourneyTimeline journey={journey} />
      </div>

      <div className="two-col">
        <div>
          <div className="panel">
            <h2>Patient summary</h2>
            <div>{patient.summary_text}</div>
          </div>
          <div className="panel">
            <h2>Dr. Zhang's guardrails</h2>
            {guardrails.length === 0 && <p className="muted">No guardrails set for this visit.</p>}
            {guardrails.map((g) => (
              <div key={g.id} className="guardrail-row">
                <span className="guardrail-num">#{g.num}</span>
                <span>
                  {g.condition_text} <span className="muted">→</span> <strong>{g.action_text}</strong>
                </span>
              </div>
            ))}
          </div>
        </div>

        <div>
          {briefs.length === 0 && (
            <div className="panel">
              <h2>Handoffs</h2>
              <p className="muted">No handoff briefs yet — they appear after the previous station ends its session.</p>
            </div>
          )}
          {briefs.map((b) => (
            <div key={b.id} className="panel">
              <h2>Handoff from {b.from_station}</h2>
              <div className="brief-summary">{renderMd(b.summary_md)}</div>
              <div className="action-items">
                {b.action_items.map((item, i) => (
                  <div key={i} className={`action-item ${item.priority}`}>
                    {item.text}
                  </div>
                ))}
              </div>
            </div>
          ))}
          {openTodos.length > 0 && (
            <div className="panel">
              <h2>Requested by earlier stations</h2>
              {openTodos.map((t) => (
                <div key={t.id} className="todo-row">
                  <span className={`badge ${t.priority}`}>{t.priority}</span>
                  <span>{t.text}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {viewingNode?.station === "imaging" && (
        <div className="panel">
          <h2>Upload imaging / labs</h2>
          <div className="upload-row">
            <input
              type="file"
              accept="image/png,image/jpeg"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
            <button className="primary" onClick={() => void analyze()} disabled={!file || analyzing}>
              Analyze
            </button>
            {analyzing && (
              <span className="muted">
                <span className="spin" /> Analyzing… (3–8s)
              </span>
            )}
            {uploadNote && !analyzing && <span className="success-note">{uploadNote}</span>}
          </div>
          {uploadError && !analyzing && <div className="error-banner" style={{ marginTop: 12 }}>{uploadError}</div>}
        </div>
      )}

      <div className="panel">
        <h2>Chart</h2>
        {chart.length === 0 && <p className="muted">No chart entries yet.</p>}
        {groupChart(chart).map((g) => (
          <div key={g.station} className="chart-group">
            <h3>{g.station}</h3>
            {g.entries.map((e) => (
              <div
                key={e.id}
                className={e.category === "contradiction" ? "chart-entry contradiction" : "chart-entry"}
              >
                <span className="chart-cat">{e.category}</span>
                <span>{e.text}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
