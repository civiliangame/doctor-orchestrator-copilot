// Screen 1 — Beat D planning. Dr. Zhang's intent (pre-typed on stage; only
// Generate is clicked live) → draft goals per journey node + numbered
// guardrails, inline-editable → Confirm → back to the patient page.

import { useEffect, useState } from "react";
import { api } from "../api";
import type { Guardrail, Journey, Station } from "../types";

const errMsg = (e: unknown) => (e instanceof Error ? e.message : String(e));

interface DraftNode {
  id: number;
  station: Station;
  specialist_name: string;
  goals: string[];
}

interface DraftGuardrail {
  id: number;
  num: number;
  condition_text: string;
  action_text: string;
}

function toDraft(journey: Journey, guardrails: Guardrail[]): { nodes: DraftNode[]; guardrails: DraftGuardrail[] } {
  return {
    nodes: [...journey.nodes]
      .sort((a, b) => a.position - b.position)
      .map((n) => ({ id: n.id, station: n.station, specialist_name: n.specialist_name, goals: [...n.goals] })),
    guardrails: guardrails.map((g) => ({ ...g })),
  };
}

export function PlanningScreen({
  visitId,
  patientId,
  nodeId,
}: {
  visitId: number;
  patientId: number;
  nodeId: number;
}) {
  const [patientName, setPatientName] = useState("");
  const [intent, setIntent] = useState("");
  const [confirmed, setConfirmed] = useState<Guardrail[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [nodes, setNodes] = useState<DraftNode[] | null>(null);
  const [guardrails, setGuardrails] = useState<DraftGuardrail[] | null>(null);
  const [generating, setGenerating] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api
      .patient(patientId, nodeId)
      .then((res) => {
        if (cancelled) return;
        setPatientName(res.patient.name);
        setIntent(res.visit.intent_text);
        setConfirmed(res.guardrails);
        setLoaded(true);
      })
      .catch((e: unknown) => {
        if (!cancelled) {
          setError(errMsg(e));
          setLoaded(true);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [patientId, nodeId]);

  const generate = async () => {
    setGenerating(true);
    setError(null);
    try {
      const res = await api.planGenerate(visitId, intent);
      const draft = toDraft(res.journey, res.guardrails);
      setNodes(draft.nodes);
      setGuardrails(draft.guardrails);
    } catch (e) {
      setError(errMsg(e));
    } finally {
      setGenerating(false);
    }
  };

  const confirm = async () => {
    if (!nodes || !guardrails) return;
    setConfirming(true);
    setError(null);
    try {
      await api.planConfirm(
        visitId,
        nodes.map((n) => ({ id: n.id, goals: n.goals.map((g) => g.trim()).filter((g) => g !== "") })),
        guardrails.map((g) => ({ id: g.id, condition_text: g.condition_text, action_text: g.action_text })),
      );
      location.hash = `#/patient/${patientId}/${nodeId}`;
    } catch (e) {
      setError(errMsg(e));
      setConfirming(false);
    }
  };

  const setGoal = (nodeIdx: number, goalIdx: number, value: string) =>
    setNodes((ns) =>
      ns
        ? ns.map((n, i) =>
            i === nodeIdx ? { ...n, goals: n.goals.map((g, j) => (j === goalIdx ? value : g)) } : n,
          )
        : ns,
    );

  const addGoal = (nodeIdx: number) =>
    setNodes((ns) => (ns ? ns.map((n, i) => (i === nodeIdx ? { ...n, goals: [...n.goals, ""] } : n)) : ns));

  const setGuardrailField = (idx: number, field: "condition_text" | "action_text", value: string) =>
    setGuardrails((gs) => (gs ? gs.map((g, i) => (i === idx ? { ...g, [field]: value } : g)) : gs));

  if (!loaded) {
    return (
      <p className="muted">
        <span className="spin" /> Loading…
      </p>
    );
  }

  return (
    <div>
      <h1 className="screen-title">Next-visit plan — {patientName || `patient ${patientId}`}</h1>
      {error && <div className="error-banner">{error}</div>}

      <div className="panel">
        <h2>Doctor's intent</h2>
        <textarea rows={6} value={intent} onChange={(e) => setIntent(e.target.value)} />
        <div className="plan-actions">
          <button className="primary" onClick={() => void generate()} disabled={generating}>
            Generate plan
          </button>
          {generating && (
            <span className="muted">
              <span className="spin" /> Generating (2–5s)…
            </span>
          )}
        </div>
      </div>

      {nodes === null && confirmed.length > 0 && (
        <div className="panel">
          <h2>Confirmed guardrails</h2>
          {confirmed.map((g) => (
            <div key={g.id} className="guardrail-row">
              <span className="guardrail-num">#{g.num}</span>
              <span>
                {g.condition_text} <span className="muted">→</span> <strong>{g.action_text}</strong>
              </span>
            </div>
          ))}
        </div>
      )}

      {nodes !== null && guardrails !== null && (
        <>
          {nodes.map((n, ni) => (
            <div key={n.id} className="panel">
              <h2>
                {n.station} — {n.specialist_name}
              </h2>
              <div className="goal-edit-list">
                {n.goals.map((g, gi) => (
                  <input key={gi} value={g} onChange={(e) => setGoal(ni, gi, e.target.value)} />
                ))}
              </div>
              <button className="add-goal" onClick={() => addGoal(ni)}>
                + Add goal
              </button>
            </div>
          ))}

          <div className="panel">
            <h2>Guardrails</h2>
            {guardrails.map((g, gi) => (
              <div key={g.id} className="guardrail-row">
                <span className="guardrail-num">#{g.num}</span>
                <input
                  value={g.condition_text}
                  onChange={(e) => setGuardrailField(gi, "condition_text", e.target.value)}
                  aria-label={`Guardrail ${g.num} condition`}
                />
                <input
                  value={g.action_text}
                  onChange={(e) => setGuardrailField(gi, "action_text", e.target.value)}
                  aria-label={`Guardrail ${g.num} action`}
                />
              </div>
            ))}
          </div>

          <button className="primary big" onClick={() => void confirm()} disabled={confirming}>
            {confirming ? (
              <>
                <span className="spin" /> Confirming…
              </>
            ) : (
              "Confirm plan"
            )}
          </button>
        </>
      )}
    </div>
  );
}
