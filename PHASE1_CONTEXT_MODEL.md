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

## Phase 1.5 — the source-grounded PCM

Phase 1 proved the belief state but left it disconnected from its richest source: the PCM
was visit-scoped, seeded from hand-written facts, and the per-patient markdown files were a
*parallel* FHIR extraction with only document-level provenance. Phase 1.5 makes the PCM the
**canonical running summary of the patient's status across all sources**, with every fact
referencing its exact origin:

1. **Patient scoping.** `context_slots` is now `UNIQUE(patient_id, key)` — the running
   status survives across visits. Per-visit requiredness moved to
   `visit_slot_requirements(visit_id, slot_key, why_required)`; `derive_required_slots`
   writes that layer and completeness is computed over it (Maria's 52% → 68% flow is
   unchanged). Pre-existing DBs self-migrate (`db._migrate` drops the derived v1 tables;
   `seed_all` re-derives on startup).

2. **Typed `source_ref` on every ledger row.** The exact origin of every belief:
   `fhir:<record_id>#<ResourceType>/<id>[,...]` · `fhir:<record_id>#longitudinal` ·
   `turn:<turn_id>` · `note:<date>:<author>` · `file:<md_file>` · `agent:<name>`. Maria's
   seeds are now just another source (`note:2026-07-11:dr-zhang`); turn contributions pin
   `turn:<id>`; the markdown chart bridge's file reader cites `file:<md_file>`.

3. **FHIR ingestion through the one write path.** `backend/fhir_ingest.py` folds a dataset
   record into the PCM via `pcm.record_contribution` — one contribution per fact (problems,
   history, meds, social, vitals, labs, assessments, procedures, imaging, reports, orders,
   immunizations, the encounter itself), each citing its exact FHIR resource id(s).
   Idempotent: a fact already asserted from the same source is never re-written. When the
   dataset is present at the repo root, startup ingests all 25 synthetic patients.

4. **Markdown context files are projections of the PCM, not a parallel pipeline.**
   `backend/context_render.py` renders a patient's belief state as markdown — every line
   footnoted with the ledger entry justifying it (source_ref, actor, quote). The seed corpus
   in `backend/seed/patients/` is built that way (`scripts/build_patient_contexts.py`,
   throwaway DB, deterministic — regenerating twice is byte-identical), and the same
   renderer serves the live document at `GET /api/patients/{id}/context.md`, where
   scribe-conversation lines appear next to FHIR-derived ones.

5. **Vocabulary discipline.** Deterministic sources (FHIR ingest, seeds, derivation) may
   create slots (`record_contribution(..., label=...)`); the LLM integrator can only fill
   existing ones — an unknown key still writes its audit ledger row but materializes no slot.

New/changed surface: `GET /api/patients/{id}/context` (running status, all sources) and
`GET /api/patients/{id}/context.md` (rendered projection); `ContextLedgerEntry.source_ref`
in the event/REST shapes; ledger history rows in the ContextPanel show the ref.

### Verified (Phase 1.5)

- Seed → 26 patients (Maria + 25 roster), Maria 6 slots / 6 requirements, 52% / 4 gaps;
  seed rows carry `note:` refs. Stubbed worker pass over a real injected turn →
  `turn:<id>` refs, `from_patient`, honest `typed`, 68% / 3 gaps.
- FHIR: Ali Kuhic 37 slots, BP `98/83 mmHg` citing its exact `Observation/<id>`;
  re-ingest and `seed_all` re-runs are ledger no-ops; unknown LLM keys create no slot
  (audit row only).
- HTTP: visit view decorated with required/why; patient JSON + markdown views; 404s.
- v1→v2 migration drops/rebuilds derived tables, preserves `patients`, adds columns.
- Corpus build is deterministic (two runs byte-identical); `tsc -b && vite build` clean.

## Next (Phase 2+, per the architecture)

Gap Critic (diff the PCM against required slots on a slower cadence) → Acquisition Router
(measurement vs live clinician question vs async intake) → the patient-facing **intake
agent** feeding the same integrator through the existing `inject-turn` seam — its
contributions land with `agent:` source_refs through the same ledger.
