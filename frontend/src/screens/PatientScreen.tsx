// Screen 1 (the rotten chart + Clean Up Context) and screen 3 (before/after payoff).
// One screen, two layouts: when latest_intake exists we split before | after.

import { useCallback, useEffect, useState } from "react";
import { navigate } from "../App";
import { api, ApiError } from "../api";
import { Markdown } from "../markdown";
import type { CallTransport, Document, Intake, PatientPage, SpecialistTask } from "../types";

function DocumentCard({ doc, index }: { doc: Document; index: number }) {
  return (
    <article className="doc-card card-in" style={{ animationDelay: `${index * 60}ms` }}>
      <header className="doc-head">
        <h3 className="doc-title">{doc.title}</h3>
        <span className="doc-date">{doc.date}</span>
      </header>
      <div className="doc-author">{doc.author}</div>
      <div className="doc-body">
        <Markdown text={doc.content_md} />
      </div>
    </article>
  );
}

function IntakePanel({ intake }: { intake: Intake }) {
  return (
    <article className="intake-card card-in">
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
    </article>
  );
}

function TaskChecklist({ tasks }: { tasks: SpecialistTask[] }) {
  if (tasks.length === 0) return null;
  return (
    <div className="panel task-panel card-in">
      <h2>For the visit — specialist checklist</h2>
      <ul className="task-list">
        {tasks.map((t) => (
          <li key={t.id} className="task-item">
            <span className="task-check">☐</span>
            <div>
              <div className="task-instruction">{t.instruction}</div>
              <div className="task-meta">
                <span className="task-for">{t.for_specialist.replace(/_/g, " ")}</span>
                <span className="task-why">{t.why}</span>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function PatientScreen({ patientId }: { patientId: number }) {
  const [page, setPage] = useState<PatientPage | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [starting, setStarting] = useState(false);
  const [transport, setTransport] = useState<CallTransport>(
    () => (localStorage.getItem("doc.transport") as CallTransport) || "sim",
  );

  const load = useCallback(() => {
    api
      .patient(patientId)
      .then((p) => {
        setPage(p);
        setError(null);
      })
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "load failed"));
  }, [patientId]);

  useEffect(load, [load]);

  const setTransportPersist = (t: CallTransport) => {
    localStorage.setItem("doc.transport", t);
    setTransport(t);
  };

  const startRun = async () => {
    if (!page || starting) return;
    setStarting(true);
    setError(null);
    try {
      const run = await api.startRun(patientId, transport);
      navigate(`#/run/${run.id}`);
    } catch (e: unknown) {
      if (e instanceof ApiError && e.code === "run_in_progress" && page.latest_run) {
        navigate(`#/run/${page.latest_run.id}`);
      } else {
        setError(e instanceof Error ? e.message : "failed to start run");
      }
    } finally {
      setStarting(false);
    }
  };

  if (!page) {
    return (
      <div>
        {error && <div className="error-banner">{error}</div>}
        <p className="muted">Loading patient…</p>
      </div>
    );
  }

  const { patient, documents, latest_run, latest_intake, specialist_tasks } = page;
  const hasIntake = latest_intake !== null;
  const runUnfinished =
    latest_run !== null && !["done", "failed"].includes(latest_run.status);

  return (
    <div className="patient-screen">
      {error && <div className="error-banner">{error}</div>}

      <header className="patient-head">
        <div>
          <h1 className="patient-name">{patient.name}</h1>
          <div className="patient-meta">
            DOB {patient.dob} · {patient.phone} ·{" "}
            {documents.length} documents on file
          </div>
        </div>
        <div className="patient-actions">
          <label className="transport-toggle" title="dev control">
            <span>call via</span>
            <select
              value={transport}
              onChange={(e) => setTransportPersist(e.target.value as CallTransport)}
            >
              <option value="sim">sim</option>
              <option value="telnyx">telnyx</option>
            </select>
          </label>
          {runUnfinished ? (
            <button className="primary big" onClick={() => navigate(`#/run/${latest_run.id}`)}>
              View run in progress →
            </button>
          ) : (
            <button className="primary big cleanup-btn" onClick={startRun} disabled={starting}>
              {starting ? "Starting…" : "Clean Up Context"}
            </button>
          )}
          {latest_run && !runUnfinished && (
            <a className="run-link" href={`#/run/${latest_run.id}`}>
              last run →
            </a>
          )}
        </div>
      </header>

      {hasIntake ? (
        <div className="before-after">
          <section className="ba-col">
            <h2 className="ba-title before">
              Before <span className="ba-sub">the messy record — {documents.length} documents, untouched</span>
            </h2>
            <div className="doc-stack">
              {documents.map((d, i) => (
                <DocumentCard key={d.id} doc={d} index={i} />
              ))}
            </div>
          </section>
          <section className="ba-col">
            <h2 className="ba-title after">
              After <span className="ba-sub">one compiled intake, phone-verified</span>
            </h2>
            <IntakePanel intake={latest_intake} />
            <TaskChecklist tasks={specialist_tasks} />
          </section>
        </div>
      ) : (
        <div className="doc-grid">
          {documents.map((d, i) => (
            <DocumentCard key={d.id} doc={d} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}
