#!/usr/bin/env node
// Replays Beat A of DEMO_SCRIPT.md into a live session via /api/dev/inject-turn,
// so the live-session screen can be built and tested with no mic, no Soniox,
// and no one reading lines out loud.
//
// Usage:
//   node scripts/replay-demo.mjs <session_id>     inject into a session the UI started
//   node scripts/replay-demo.mjs                  create a fresh session (nurse node) first
//   flags: --fast (300ms pauses)  --end (call End Session when done)
//
// Keep the lines below in sync with DEMO_SCRIPT.md — the script IS the spec.

const BASE = process.env.DOC_API ?? "http://localhost:8000";
const args = process.argv.slice(2);
const FAST = args.includes("--fast");
const END = args.includes("--end");
const sessionArg = args.find((a) => !a.startsWith("--"));

// [speaker, text, note-printed-after-injection]
// Consecutive staff turns are fine here: the backend only ticks on patient turns.
const TURNS = [
  ["staff", "Hi Maria, I'm Nurse Kim — how are you doing today?", null],
  ["patient", "I'm okay. The chest pain is still there, though. It comes and goes.",
    "expect: suggestion card (ask about location/character — Dr. Zhang's goal #1)"],
  ["staff", "Has the pain changed at all since last week — moved anywhere, or felt different?", null],
  ["patient", "Actually, yeah — the past couple of days it's been spreading to my left arm.",
    "⚡ GUARDRAIL #1 — expect: RED alert + mutation banner. Click ACCEPT in the UI now."],
  ["staff", "Okay, that's important — any numbness in that arm, or any shortness of breath?", null],
  ["patient", "A little tingling in my fingers this morning. No trouble breathing.",
    "expect: chart entries + todo for the cardiology node"],
  ["staff", "Are you still taking your medications — the lisinopril and the aspirin?", null],
  ["patient", "The blood pressure pill, yes, every morning. The aspirin was bothering my stomach, so I stopped it — maybe two weeks ago.",
    "🌱 contradiction seed — expect: chart entry + guardrail #3 flag"],
  ["staff", "Got it. And this morning — did you take anything before coming in?", null],
  ["patient", "Just my usual pills. I've been taking the aspirin every day like Dr. Zhang said.",
    "⚡ CONTRADICTION — expect: AMBER card citing both quotes verbatim"],
  ["staff", "Just so I have it right — when did you last actually take an aspirin?", null],
  ["patient", "…Honestly, it's been a couple of weeks. I didn't want Dr. Zhang to think I wasn't following the plan.",
    "expect: chart entry confirming aspirin stopped ~2 weeks ago"],
  ["staff", "Thanks for being honest — that's exactly what we need to know. Let me get your blood pressure.", null],
  ["staff", "One forty-two over eighty-eight.",
    "expect: vital chart entry; guardrail #4 NOT tripped (below 160/100)"],
  ["staff", "All right — we're going to have cardiology take a look first, then imaging, and Dr. Zhang will see you after that.", null],
];

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function api(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: body ? { "content-type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`${method} ${path} -> ${res.status} ${text}`);
  }
  return res.status === 204 ? null : res.json();
}

async function makeSession() {
  const { appointments } = await api("GET", "/api/appointments?station=nurse");
  if (!appointments?.length) throw new Error("no nurse appointments — did you run /api/dev/reset?");
  const { node_id, patient_name } = appointments[0];
  const s = await api("POST", "/api/sessions", { node_id });
  console.log(`created session ${s.session_id} for ${patient_name} (node ${node_id})`);
  console.log(`events: ${s.events_url}\n`);
  return s.session_id;
}

const sessionId = sessionArg ? Number(sessionArg) : await makeSession();

for (const [speaker, text, note] of TURNS) {
  console.log(`${speaker === "staff" ? "NURSE  " : "PATIENT"} | ${text}`);
  await api("POST", "/api/dev/inject-turn", { session_id: sessionId, speaker, text });
  if (note) console.log(`        └─ ${note}`);
  // patient turns get a longer pause so the five workers' cards can land between lines
  await sleep(FAST ? 300 : speaker === "patient" ? 4000 : 1500);
}

if (END) {
  console.log("\nending session (Fable compile)…");
  await api("POST", `/api/sessions/${sessionId}/end`);
  console.log("done — watch for session.compile.done on the events socket");
} else {
  console.log("\nreplay complete — click End Session in the UI (or re-run with --end)");
}
