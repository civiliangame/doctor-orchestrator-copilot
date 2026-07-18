// App shell + hash routing.
//
// Routes:
//   #/               patient page for the demo patient (screens 1 and 3 — the payoff)
//   #/run/:runId     run view — four stages lighting up live

import { useEffect, useState } from "react";
import { PatientScreen } from "./screens/PatientScreen";
import { RunScreen } from "./screens/RunScreen";

const DEMO_PATIENT_ID = 1;

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
  const parts = hash.replace(/^#\/?/, "").split("/").filter(Boolean);

  let screen: JSX.Element;
  if (parts[0] === "run" && parts.length >= 2 && Number.isFinite(Number(parts[1]))) {
    screen = <RunScreen runId={Number(parts[1])} />;
  } else {
    screen = <PatientScreen patientId={DEMO_PATIENT_ID} />;
  }

  return (
    <div className="app">
      <header className="topbar">
        <a className="brand" href="#/">
          <span className="brand-mark">DOC</span>
          <span className="brand-sub">cleans up context rot</span>
        </a>
        <span className="topbar-note">before the visit, not after</span>
      </header>
      <div className="disclaimer">Demo system — synthetic data only. Not for clinical use.</div>
      <main className="screen">{screen}</main>
    </div>
  );
}
