// Screen 2 — today's appointments for the current station. Thin by design.

import { useCallback, useEffect, useState } from "react";
import { api } from "../api";
import type { Appointment, Station } from "../types";

export function AppointmentsScreen({ station }: { station: Station }) {
  const [appts, setAppts] = useState<Appointment[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.appointments(station);
      setAppts(res.appointments);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
      setAppts(null);
    } finally {
      setLoading(false);
    }
  }, [station]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div>
      <div className="page-head">
        <h1 className="screen-title">Today — {station}</h1>
        <button onClick={() => void load()} disabled={loading}>
          {loading ? <span className="spin" /> : "Refresh"}
        </button>
      </div>
      {error && <div className="error-banner">{error}</div>}
      {loading && appts === null && (
        <p className="muted">
          <span className="spin" /> Loading appointments…
        </p>
      )}
      {appts !== null && appts.length === 0 && (
        <p className="muted">No appointments for this station today.</p>
      )}
      {appts?.map((a) => (
        <button
          key={a.node_id}
          className="appt-row"
          onClick={() => {
            location.hash = `#/patient/${a.patient_id}/${a.node_id}`;
          }}
        >
          <span className="appt-time">{a.time}</span>
          <span className="appt-name">{a.patient_name}</span>
          <span className={`badge ${a.status}`}>{a.status}</span>
        </button>
      ))}
    </div>
  );
}
