// App shell: station switcher + hash routing. Screens live in src/screens/.
//
// Routes:
//   #/                                appointments for the current station
//   #/patient/:patientId/:nodeId      patient page (also the payoff view)
//   #/plan/:visitId/:patientId/:nodeId  Beat D planning
//   #/session/:sessionId/:nodeId/:patientId  live session

import { useEffect, useState } from "react";
import type { Station } from "./types";
import { AppointmentsScreen } from "./screens/AppointmentsScreen";
import { PatientScreen } from "./screens/PatientScreen";
import { PlanningScreen } from "./screens/PlanningScreen";
import { SessionScreen } from "./screens/SessionScreen";

const STATIONS: Station[] = ["nurse", "cardiology", "imaging", "doctor"];

export function navigate(hash: string) {
  location.hash = hash;
}

function useHash(): string {
  const [hash, setHash] = useState(location.hash);
  useEffect(() => {
    const onChange = () => setHash(location.hash);
    window.addEventListener("hashchange", onChange);
    return () => window.removeEventListener("hashchange", onChange);
  }, []);
  return hash;
}

export default function App() {
  const hash = useHash();
  const [station, setStation] = useState<Station>(
    () => (localStorage.getItem("doc.station") as Station) || "nurse",
  );

  const setStationPersist = (s: Station) => {
    localStorage.setItem("doc.station", s);
    setStation(s);
    navigate("#/");
  };

  const parts = hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  let screen: JSX.Element;
  if (parts[0] === "patient" && parts.length >= 3) {
    screen = (
      <PatientScreen
        patientId={Number(parts[1])}
        nodeId={Number(parts[2])}
        station={station}
      />
    );
  } else if (parts[0] === "plan" && parts.length >= 4) {
    screen = (
      <PlanningScreen
        visitId={Number(parts[1])}
        patientId={Number(parts[2])}
        nodeId={Number(parts[3])}
      />
    );
  } else if (parts[0] === "session" && parts.length >= 4) {
    screen = (
      <SessionScreen
        sessionId={Number(parts[1])}
        nodeId={Number(parts[2])}
        patientId={Number(parts[3])}
        station={station}
      />
    );
  } else {
    screen = <AppointmentsScreen station={station} />;
  }

  return (
    <div className="app">
      <header className="topbar">
        <a className="brand" href="#/">
          <span className="brand-mark">DOC</span>
          <span className="brand-sub">Doctor Orchestrator Copilot</span>
        </a>
        <label className="station-switch">
          <span>Station</span>
          <select
            value={station}
            onChange={(e) => setStationPersist(e.target.value as Station)}
          >
            {STATIONS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </label>
      </header>
      <div className="disclaimer">Demo system — synthetic data only. Not for clinical use.</div>
      <main className="screen">{screen}</main>
    </div>
  );
}
