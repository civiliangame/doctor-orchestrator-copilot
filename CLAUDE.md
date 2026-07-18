# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

DOC (Doctor Orchestrator Copilot) — a 24h-hackathon demo. A doctor's next-visit intent becomes a routed patient journey; during live sessions the backend listens to diarized speech and pushes suggestion cards, guardrail alerts, and contradiction flags per patient turn. Synthetic data only; the deliverable is a 3-minute stage demo.

**Read the docs in this order — they form a strict hierarchy:**

1. `API_CONTRACT.md` — the authoritative frontend↔backend contract. Change it *first*, then the code. snake_case JSON, integer IDs, ISO-8601 UTC timestamps, errors as `{"error": {"code", "message"}}`.
2. `SPEC.md` — locked design decisions; supersedes `DESIGN.md` where they differ.
3. `DEMO_SCRIPT.md` — the acceptance test. Every mechanism exists to make that script land. `scripts/replay-demo.mjs` must stay in sync with it.

## Commands

```bash
# Backend (FastAPI, port 8000) — venv lives at backend/.venv
cd backend && .venv/Scripts/activate && uvicorn main:app --reload

# Frontend (Vite, port 5173; calls the backend directly, CORS allows 5173)
cd frontend && npm run dev
cd frontend && npm run build        # tsc -b && vite build — this IS the type check

# Reset DB to seeded demo state (do this constantly between runs)
curl -X POST http://localhost:8000/api/dev/reset

# Replay the Beat A dialogue into a live session (no mic/Soniox/voice needed)
node scripts/replay-demo.mjs <session_id>    # flags: --fast, --end

# Sanity check keys loaded
curl http://localhost:8000/health
```

There is no test suite or linter. Verification = `npm run build` for types, plus replaying the demo script against a reset DB and watching the events.

Secrets live in `.env` at repo root (`SONIOX_API_KEY`, `CLAUDE_API_KEY` or `ANTHROPIC_API_KEY`). All env and constants are read **only** through `backend/config.py` — never `os.environ` elsewhere.

## Architecture

One data path, end to end:

```
mic → /ws/audio (voice.py: Soniox WS relay, speaker-role mapping, 900ms end-of-turn debounce)
    → turns.ingest_turn()   ← also fed by POST /api/dev/inject-turn (the integration seam)
    → orchestrator.on_patient_turn (tick.py)
    → 5 parallel Claude workers (workers.py)
    → SQLite (db.py) + events.broadcast()
    → /ws/session/{id}/events → React UI
```

- **`turns.ingest_turn()` is THE seam.** Voice and `inject-turn` both feed it; by the time a turn arrives it is final. Every patient turn fires an orchestrator tick; staff turns are just persisted. This makes everything buildable and testable without audio.
- **Two worker groups with different cancellation policies** (`orchestrator/tick.py`): the *urgent* group (contradictions + suggestions on Sonnet, guardrails on Haiku) is latest-wins — a new patient turn cancels the in-flight task and re-fires with the fuller transcript. The *accumulator* group (chart + todos on Haiku) is serialized per session and never cancelled; each pass covers all turns since the last completed pass. Each worker persists and broadcasts as soon as its own call returns.
- **Prompt caching:** all five workers share an identical cached system prefix (`prompts.session_prefix`) with per-worker system + dynamic suffix appended. Keep the prefix byte-identical across workers or the cache breaks.
- **End Session** runs the compiler (`orchestrator/compile.py`, Fable model with Opus fallback): one handoff brief per outgoing journey edge + to-do reconciliation, then marks the node done and activates the next. `chart_entries` is an append-only audit trail — the compiler never rewrites it.
- **Models never edit the journey graph.** The graph is seeded; the Beat D planning call only fills node goals/guardrails. When a guardrail with `proposed_insert` fires, the *backend* creates a `journey_mutations` row, the specialist clicks Accept, and the timeline re-routes.
- **Speaker mapping:** first speaker = staff (anchored by the scripted greeting), then turns strictly alternate. Diarization labels only confirm; on disagreement, alternation wins.
- **Event bus (`events.py`):** envelope `{seq, ts, type, data}`, `seq` monotonic per session and in-memory only. Clients dedupe by `(type, data.id)` and rehydrate via REST, so backend restarts are fine.
- **DB:** SQLite via thin helpers in `db.py` (`q`/`one`/`ins`/`ex`). `seed.py` seeds the demo journey at startup and on `/api/dev/reset`. Model tiers, debounce, and transcript-window constants live in `config.py`.

Frontend (`frontend/src/`): React + Vite + TS, no design system. Five screens (Planning → Appointments → Patient page → Live session → payoff is the patient page again). It's projected on stage: big type, high contrast. Worker prompt rules to preserve when editing `orchestrator/prompts.py`: empty output beats filler, never repeat an already-shown item, quote trigger text verbatim, ≤2 suggestions per turn.

Latency budget: patient end-of-turn → first card < 3s. `workers.latency_samples` collects per-worker timings; if the budget is blown, trim the transcript window (see `config.py`) before touching anything else.
