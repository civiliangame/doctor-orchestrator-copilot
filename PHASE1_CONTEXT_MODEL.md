# Phase 1 — Patient Context Model + Provenance Ledger

Branch `yilun`. First phase of turning DOC from a **reactive** per-turn copilot into an
**agentic harness** that refines patient context and reasons about what still needs to be
gathered. This phase builds the *substrate* the later phases (gap critic, acquisition
router, intake agent) will act on. No new agents yet — it proves the belief state.

## What this phase adds

1. **A living belief state (the PCM).** Today DOC's context is scattered across the
   append-only `chart_entries`, `todos`, and the hand-written `summary_text` — there is no
   object that says *"what we believe now, how sure we are, and what's still missing."*
   Phase 1 adds one: a set of typed **context slots**, each with a `status`
   (`known | uncertain | stale | contradicted | missing`), a `confidence`, and a value.
   It is a **view** on top of the chart, never a replacement (same discipline as
   `node_briefs` vs `chart_entries`).

2. **Slots are derived, not hand-authored.** `pcm.derive_required_slots` reads the visit's
   guardrails + node goals (+ a cardiac template) and materializes the slots today's visit
   actually needs, attributing each to the guardrail/goal that made it required
   (`why_required`). Re-planning the visit re-derives them.

3. **A provenance ledger for quality.** Every belief has a paper trail.
   `pcm.record_contribution` is the *only* way a slot value changes, and it always writes a
   `context_ledger` row first, capturing: **which user, who they are, when, whether it came
   from the patient, whether it was extracted from live speech vs typed vs seeded**, the
   verbatim quote, the model (if inferred), and confidence. The slot's `current_ledger_id`
   points at the row that justifies its present value; the full history is queryable.

4. **A context-integrator worker.** A sixth per-turn worker (`pcm`, Haiku), wired as an
   **accumulator** alongside chart/todos (never cancelled; covers every turn since the last
   pass). It folds each patient turn into the slots and broadcasts `context.slot_updated`
   with the changed slot + new completeness. Provenance is attributed by matching the
   model's quote back to the transcript turn that said it — so "from patient / live speech"
   is honest, not assumed (an injected demo turn is correctly recorded as `typed`, not
   `speech`).

5. **A completeness panel.** The live session screen shows a readiness meter (weighted 0–100
   with a per-status segmented bar), gap-first slot rows, and — the point — a provenance
   line per belief (`from patient · live speech · 2m ago · Maria Alvarez`) that expands to
   the full ledger history with verbatim quotes.

## Where it plugs in

| Layer | File(s) |
|---|---|
| Schema | `backend/db.py` — `context_slots`, `context_ledger` |
| PCM core | `backend/orchestrator/pcm.py` — derive / seed / `record_contribution` / completeness / serializers |
| Seed hook | `backend/seed.py` — derive + seed with provenance on reset |
| Worker | `backend/orchestrator/workers.py` (`_handle_pcm`, `_attribute_turn`), `prompts.py` (`PCM_SYSTEM` + slots block), `tick.py` via `ACCUMULATOR_WORKERS` |
| API | `backend/routes/context.py` — `GET /api/visits/{id}/context`; event `context.slot_updated` |
| UI | `frontend/src/components/ContextPanel.tsx`, `useSessionEvents.ts`, `SessionScreen.tsx`, `types.ts`, `api.ts`, `styles.css` |

## Seeded demo state (Maria Alvarez)

Derivation produces 6 required slots; seeding fills 5 from the record and leaves
`chest_pain.progression` a visible gap. `bp.current` is seeded **stale** on purpose (last
week's 138/86 exists but today needs a recheck). Baseline completeness: **52%, 4 open gaps**.
As the session gathers information, slots flip to `known` and completeness climbs (verified:
"spreading to my left arm" + "chest pain is worse" → 68%, gaps 4→3), each with a
patient-attributed, quoted ledger entry.

## Verified

- Derive → 6 slots; seed → 5 filled with `source_kind=seed` provenance, 1 missing.
- `record_contribution`: ledger write + slot upsert + `current_ledger_id`; no-op guard (same
  value+status does not spam the ledger).
- Handler path end-to-end (stubbed worker output over the real session turn): two
  `context.slot_updated` broadcasts, quote→turn attribution, `from_patient` correct,
  completeness 52%→68%.
- `GET /api/visits/1/context` over HTTP; graceful degradation with no API key (turn persists,
  workers fail-safe, server stays up).
- Frontend `tsc -b && vite build` clean.

*Not yet exercised live:* the actual Haiku extraction call (needs `CLAUDE_API_KEY`). The `pcm`
worker is wired identically to the existing five, so it runs whenever a key is present.

## Next (Phase 2+, per the architecture)

Gap Critic (diff the PCM against required slots on a slower cadence) → Acquisition Router
(measurement vs live clinician question vs async intake) → the patient-facing **intake
agent** feeding the same integrator through the existing `inject-turn` seam.
