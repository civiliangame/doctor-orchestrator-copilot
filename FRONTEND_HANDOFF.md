# Frontend Handoff — start here

You're building the UI for DOC (Doctor Orchestrator Copilot), a 24h-hackathon demo.
Three documents, in reading order:

1. **This file** — how to work, build order, how to test without waiting on anyone.
2. **`API_CONTRACT.md`** — every endpoint, every payload type, the WebSocket event union.
   This is the commitment; build against it exactly. If something is missing or wrong,
   change the contract first, then the code.
3. **`DEMO_SCRIPT.md`** — the 3-minute stage performance your UI has to carry. When in
   doubt about a design decision, optimize for what looks good *on a projector during
   that script*.

Stack: React + Vite + TypeScript (already scaffolded in `frontend/`). Styling is yours —
no design system mandated. Constraint: it's projected on stage, so **big type, high
contrast, dark-mode friendly**.

## Running things

```
# backend (FastAPI, port 8000)
cd backend && .venv/Scripts/activate && uvicorn main:app --reload

# frontend (Vite, port 5173, proxies /api and /ws to 8000)
cd frontend && npm run dev

# reset the database to the seeded demo state (do this constantly)
curl -X POST http://localhost:8000/api/dev/reset
```

## The one thing that makes this parallelizable

**You never need the microphone, Soniox, or the Claude workers to build any screen.**

`POST /api/dev/inject-turn` feeds a typed line into the same pipeline a spoken line goes
through. The backend then emits the same `transcript.turn`, `suggestion`,
`guardrail.alert`, `contradiction`, `chart.entry`, `todo.update`, and
`journey.mutation_proposed` events over `/ws/session/{id}/events` that real speech
produces. So the workflow for the live-session screen is:

1. Open the app, click through to Maria's patient page, click **Start Session**.
2. Note the session id (surface it in the UI footer or console — you'll want it).
3. In a terminal: `node scripts/replay-demo.mjs <session_id>`

That script replays the entire Beat A dialogue from `DEMO_SCRIPT.md`, line by line, with
realistic pauses. Your screen should light up exactly the way it will on stage: suggestion
cards, then the red guardrail alert + journey-mutation banner, then the amber
contradiction card. Run it a hundred times; `api/dev/reset` between runs.

Until the backend's orchestrator lands, inject-turn will still echo `transcript.turn`
events even if the worker cards don't fire yet — so the transcript pane, layout, and
event plumbing are buildable from day one. If the backend isn't running at all, stub
`ServerEvent` frames from a fixture file; the types in `API_CONTRACT.md` are exact.

## Build order (matches demo importance)

**1. Live session screen (screen 4) — the climax, build it first.**
- Transcript pane: staff turns left/plain, patient turns right/accented;
  `transcript.partial` renders as a live-updating italic line, replaced in place,
  cleared when the finalized `transcript.turn` arrives.
- Card stack: `suggestion` (neutral), `guardrail.alert` (**red, loudest thing on the
  screen, persists until session end**), `contradiction` (**amber, distinct**). Cards
  arrive staggered after each patient turn — render on arrival, never batch. Newest 2
  suggestions prominent, older ones collapse.
- The verbatim quotes (`triggered_by`, `statement`, `conflicts_with`) are the demo —
  render them as quoted text, visually citation-like.
- Journey timeline strip (see below) with the `journey.mutation_proposed` banner:
  Accept / Dismiss buttons → `POST /api/mutations/{id}/accept|dismiss`. On
  `journey.updated`, animate the inserted node.
- "DOC is thinking" indicator on `tick.started`, cleared by the first resulting card or
  the next tick.
- **End Session** button → `POST /api/sessions/{id}/end` → show a compiling state on
  `session.compile.started`, then a brief "handoff written" confirmation with the
  returned briefs on `session.compile.done`.
- Reconnect rule from the contract: on socket drop, rehydrate via
  `GET /api/sessions/{id}`, dedupe by `(type, data.id)`. A mid-demo browser refresh must
  lose nothing.

**2. Patient page (screen 3) — doubles as the final payoff screen.**
- Header: patient name/DOB, `summary_text`, disclaimer banner.
- **Action items from `briefs[]` render BIG** — they're "what the last specialist needs
  you to do" and the payoff beat zooms in on them.
- Journey timeline (shared component): horizontal line of nodes ordered by `position`;
  `done` dimmed with a check, `active` highlighted, `pending` plain.
- Chart: `chart[]` grouped by `node_station`, chronological within group;
  `category: "contradiction"` entries get the amber treatment here too.
- **Start Session** button (only on the viewer's `active` node) → `POST /api/sessions`.

**3. Appointments list (screen 2).** Thin: station switcher (frontend-only dropdown:
nurse / cardiology / imaging / doctor) → `GET /api/appointments?station=` → rows →
click → patient page. The switcher is how one laptop plays four roles on stage.

**4. Planning screen (screen 1, Beat D).** Textarea (pre-filled from
`visit.intent_text` if present) → **Generate** → `plan/generate` (2–5s, show progress) →
render draft goals per node + numbered guardrails, inline-editable → **Confirm** →
`plan/confirm`. The generated guardrails appearing under each journey node is the beat.

**5. Imaging upload (Beat C).** On the imaging node's patient page: file picker →
`POST /api/nodes/{id}/images` (3–8s, show analyzing state) → returned `findings`
render as new chart entries, flagged "for Dr. Zhang's review".

## Definition of done

`DEMO_SCRIPT.md` runs end-to-end on your screens: reset → Beat D generate/confirm →
appointments → Maria → Start Session → `replay-demo.mjs` → red alert fires and the
timeline re-routes on Accept → amber contradiction card cites both quotes → End Session
compiles → imaging upload lands findings → doctor's patient page shows the accumulated
chart with the contradiction surviving. If a pixel decision helps that run land on a
projector, it's right.

## Not your problem

Speaker diarization, role mapping, end-of-turn debounce, Claude calls, prompt design,
SQLite — all backend. If an event or field you need is missing, that's a contract
conversation, not something to work around client-side.
