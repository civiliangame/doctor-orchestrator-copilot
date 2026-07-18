// Patient Context Model panel (Phase 1). Shows the live belief state the agentic
// harness reasons over: how complete today's context is, each slot's status/value,
// and — the point of the ledger — WHERE each belief came from (who, when, patient
// or not, live speech or seeded record). Baseline is fetched once; live
// context.slot_updated events overlay it in place.

import { useEffect, useMemo, useState } from "react";
import { api } from "../api";
import type {
  ContextCompleteness,
  ContextLedgerEntry,
  ContextSlot,
  PatientContext,
  SlotStatus,
} from "../types";

const STATUS_META: Record<SlotStatus, { label: string; cls: string }> = {
  known: { label: "known", cls: "slot-known" },
  uncertain: { label: "uncertain", cls: "slot-uncertain" },
  stale: { label: "stale", cls: "slot-stale" },
  contradicted: { label: "conflict", cls: "slot-contradicted" },
  missing: { label: "missing", cls: "slot-missing" },
};

// Gaps first — the harness's job is to close these, so they belong at the top.
const STATUS_ORDER: SlotStatus[] = ["contradicted", "missing", "stale", "uncertain", "known"];

const SOURCE_LABEL: Record<string, string> = {
  seed: "prior record",
  speech: "live speech",
  typed: "typed",
  image: "imaging",
  measurement: "measured",
  inferred: "inferred",
};

function mergeSlots(base: ContextSlot[], live: ContextSlot[]): ContextSlot[] {
  const byId = new Map(base.map((s) => [s.id, s]));
  for (const s of live) byId.set(s.id, s);
  return [...byId.values()].sort(
    (a, b) => STATUS_ORDER.indexOf(a.status) - STATUS_ORDER.indexOf(b.status),
  );
}

function relTime(ts: string): string {
  const secs = Math.max(0, (Date.now() - new Date(ts).getTime()) / 1000);
  if (secs < 60) return "just now";
  if (secs < 3600) return `${Math.floor(secs / 60)}m ago`;
  if (secs < 86400) return `${Math.floor(secs / 3600)}h ago`;
  return `${Math.floor(secs / 86400)}d ago`;
}

function ProvenanceLine({ p }: { p: ContextLedgerEntry }) {
  const who = p.from_patient ? "from patient" : `from ${p.actor_role}`;
  const how = SOURCE_LABEL[p.source_kind] ?? p.source_kind;
  return (
    <div className="slot-prov">
      <span className={`prov-chip ${p.from_patient ? "prov-patient" : ""}`}>{who}</span>
      <span className="prov-chip">{how}</span>
      {p.extracted_from_speech && <span className="prov-chip prov-speech">🎙 speech</span>}
      <span className="prov-meta">
        {p.actor_name} · {relTime(p.ts)}
        {p.confidence ? ` · ${Math.round(p.confidence * 100)}%` : ""}
      </span>
    </div>
  );
}

export function ContextPanel({
  visitId,
  liveSlots,
  liveCompleteness,
}: {
  visitId: number;
  liveSlots: ContextSlot[];
  liveCompleteness: ContextCompleteness | null;
}) {
  const [base, setBase] = useState<PatientContext | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    api
      .context(visitId)
      .then((pc) => !cancelled && setBase(pc))
      .catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [visitId]);

  const slots = useMemo(() => mergeSlots(base?.slots ?? [], liveSlots), [base, liveSlots]);
  const completeness: ContextCompleteness | null = liveCompleteness ?? base?.completeness ?? null;

  // Ledger history for a slot key: baseline ledger (+ the slot's current provenance,
  // which may be newer than the last baseline fetch).
  const historyFor = (slot: ContextSlot): ContextLedgerEntry[] => {
    const baseHist = (base?.ledger ?? []).filter((l) => l.slot_key === slot.key);
    const cur = slot.provenance;
    if (cur && !baseHist.some((h) => h.id === cur.id)) return [cur, ...baseHist];
    return baseHist;
  };

  if (!base && slots.length === 0) {
    return (
      <div className="panel">
        <h2>Patient Context</h2>
        <div className="muted">Loading context model…</div>
      </div>
    );
  }

  return (
    <div className="panel context-panel">
      <div className="context-head">
        <h2>Patient Context</h2>
        {completeness && (
          <span className="context-pct" title={`${completeness.open_gaps} open gap(s)`}>
            {completeness.percent}% ready · {completeness.open_gaps} gap
            {completeness.open_gaps === 1 ? "" : "s"}
          </span>
        )}
      </div>

      {completeness && (
        <div className="completeness-bar" aria-label="context completeness">
          {STATUS_ORDER.slice()
            .reverse()
            .map((st) => {
              const n = completeness.counts[st] ?? 0;
              if (!n) return null;
              const pct = (n / completeness.total_required) * 100;
              return (
                <span
                  key={st}
                  className={`cbar-seg ${STATUS_META[st].cls}`}
                  style={{ width: `${pct}%` }}
                  title={`${n} ${STATUS_META[st].label}`}
                />
              );
            })}
        </div>
      )}

      <div className="slot-list">
        {slots.map((s) => {
          const open = expanded === s.key;
          const hist = open ? historyFor(s) : [];
          return (
            <div key={s.key} className={`slot-row ${STATUS_META[s.status].cls}`}>
              <button
                className="slot-main"
                onClick={() => setExpanded(open ? null : s.key)}
                title={s.why_required}
              >
                <span className={`slot-pill ${STATUS_META[s.status].cls}`}>
                  {STATUS_META[s.status].label}
                </span>
                <span className="slot-label">{s.label}</span>
                <span className="slot-value">{s.value || "— not yet gathered"}</span>
              </button>
              {s.provenance && <ProvenanceLine p={s.provenance} />}
              {open && (
                <div className="slot-history">
                  <div className="slot-why">Required by: {s.why_required}</div>
                  {hist.length === 0 && <div className="muted">No recorded history.</div>}
                  {hist.map((h) => (
                    <div key={h.id} className="hist-row">
                      <span className="hist-status">{h.status}</span>
                      <span className="hist-val">{h.value}</span>
                      {h.raw_quote && <span className="hist-quote">“{h.raw_quote}”</span>}
                      <span className="hist-src">
                        {h.from_patient ? "patient" : h.actor_name} ·{" "}
                        {SOURCE_LABEL[h.source_kind] ?? h.source_kind}
                        {h.model ? ` · ${h.model}` : ""}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
