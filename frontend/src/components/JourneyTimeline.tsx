// Straight horizontal timeline of journey nodes (SPEC: DAG in the data model,
// rendered linear). Shared by the patient page and the live session screen.
// Animates node insertion: a node id not seen on the previous render mounts
// with the .node-new class (one-shot CSS animation).

import { useEffect, useRef } from "react";
import type { Journey } from "../types";

export function JourneyTimeline({ journey }: { journey: Journey }) {
  const seenIds = useRef<Set<number>>(new Set());
  const prevSeen = seenIds.current;
  const nodes = [...journey.nodes].sort((a, b) => a.position - b.position);

  useEffect(() => {
    seenIds.current = new Set(nodes.map((n) => n.id));
  });

  return (
    <div className="timeline" role="list">
      {nodes.map((n, i) => (
        <div key={n.id} className="timeline-item" role="listitem">
          {i > 0 && <div className={`timeline-link ${n.status === "done" ? "done" : ""}`} />}
          <div
            className={[
              "node",
              `node-${n.status}`,
              prevSeen.size > 0 && !prevSeen.has(n.id) ? "node-new" : "",
            ].join(" ")}
          >
            <span className="node-dot">{n.status === "done" ? "✓" : i + 1}</span>
            <span className="node-station">{n.station}</span>
            <span className="node-specialist">{n.specialist_name}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
