# DOC — Doctor Orchestrator Copilot

DOC is an ambient clinical copilot that follows a patient across a multi-station visit
(Nurse → Imaging → Doctor, with a Cardiology consult that can be inserted mid-visit). It
listens to the live clinician↔patient conversation and, on every patient turn, runs a fleet
of specialized Claude workers that surface suggestions, contradictions, guardrail alerts,
chart entries, and to-dos — then compiles a handoff brief when the session ends.

This branch (`yilun`) adds the **Patient Context Model (PCM)** — Phase 1 of turning DOC from
a *reactive* copilot into an *agentic harness* that actively refines patient context and
reasons about what still needs to be gathered.

---

## The Patient Context Model (PCM)

### Why

Out of the box, DOC's knowledge of a patient is **scattered and passive**: append-only
`chart_entries`, a to-do list, and a hand-written summary. Nothing represents *"what we
believe about this patient right now, how confident we are, and what's still missing."*
Without that object, DOC can only *react* to what was just said — it can't decide what to go
**gather**.

The PCM is that object: a **living, structured, gap-aware belief state** the harness reasons
over. It is a *view* layered on top of the append-only chart — never a replacement for it
(the raw chart stays the audit trail; the PCM is the reconciled belief on top).

### The three ideas

**1. Typed slots with a status.** The PCM is a set of context **slots**, each carrying:

| field | meaning |
|---|---|
| `status` | `known` · `uncertain` · `stale` · `contradicted` · `missing` |
| `value` | current best value (clinical shorthand) |
| `confidence` | 0–1 |
| `why_required` | the guardrail/goal that made this slot matter today |
| `provenance` | pointer to the ledger row justifying the current value |

A `contradiction` flips a slot to `contradicted` (→ re-confirm); a value from last week that
today's visit needs fresh is `stale` (→ re-measure). Gaps aren't just "unknown" — they're
typed, so the harness can route each kind differently in later phases.

**2. Slots are *derived*, not hand-authored.** `derive_required_slots` reads the visit's
**guardrails + node goals** (plus a condition template) and materializes exactly the slots
today's visit needs. The node goals and guardrails *are* an implicit information requirement
spec — e.g. Guardrail #1 ("pain radiating to arm/jaw/back") derives the slot
`chest_pain.radiation`. Re-planning the visit re-derives the slots.

**3. Every belief has a provenance ledger — for quality.** `context_ledger` is an
append-only trail behind every belief. `record_contribution` is the **single write path**:
it always writes a ledger row *first*, then points the slot's `current_ledger_id` at it. Each
row captures where the belief came from, so its quality is auditable:

| dimension | example |
|---|---|
| **who** | `actor_name` = "Maria Alvarez" / "Dr. Zhang (prior visit note)" |
| **who they are** | `actor_role` = `patient` · `nurse` · `clinician` · `system` |
| **when** | `ts` (ISO 8601 UTC) |
| **from the patient?** | `from_patient` (bool) |
| **extracted from live speech?** | `extracted_from_speech` — honest: an injected/typed turn is `typed`, only Soniox audio is `speech` |
| **how** | `source_kind` = `seed` · `speech` · `typed` · `image` · `measurement` · `inferred` |
| **the citation** | `raw_quote` (verbatim), `turn_id` |
| **if inferred, by what** | `model`, `confidence` |

Nothing changes a slot's value except through this path, so **no belief is ever unattributed**.

### The integrator

A sixth per-turn worker (`pcm`, Haiku) runs as an **accumulator** alongside `chart`/`todos`
(never cancelled; covers every turn since the last completed pass). It folds each patient
turn into the slots, attributes each update to the transcript turn that said it (by matching
the model's quote back to the transcript), calls `record_contribution`, and broadcasts
`context.slot_updated` with the changed slot + new completeness score.

### What the demo looks like

Seeded patient **Maria Alvarez**: derivation produces 6 required slots; seeding fills 5 from
the record with provenance and leaves `chest_pain.progression` a visible gap. `bp.current` is
seeded **stale** on purpose (last week's 138/86 exists, but today needs a recheck). Baseline:
**52% ready, 4 open gaps**. As the session gathers information, slots flip to `known` and the
readiness meter climbs (e.g. "spreading to my left arm" + "chest pain is worse" → **68%**),
each backed by a patient-attributed, quoted ledger entry.

---

## Specs

### Data model (new tables, `backend/db.py`)

```
context_slots   (id, visit_id, key, label, category,
                 status,        -- known|uncertain|stale|contradicted|missing
                 value, confidence, required, why_required,
                 current_ledger_id,   -- provenance pointer -> context_ledger.id
                 updated_ts)
                 UNIQUE(visit_id, key)

context_ledger  (id, visit_id, slot_id, slot_key, value_written, status_written, confidence,
                 -- provenance / quality dimensions:
                 source_kind,           -- seed|speech|typed|image|measurement|inferred
                 source_channel,        -- seed|soniox|inject|image_upload|manual|compiler
                 actor_role, actor_id, actor_name,
                 from_patient, extracted_from_speech,
                 model, session_id, node_id, turn_id,
                 raw_quote,             -- verbatim citation
                 ts)                    -- append-only
```

### API

```
GET /api/visits/{visit_id}/context
    -> PatientContext { visit_id, slots[], completeness, ledger[] }   # belief + score + full trail
```

WebSocket event on `/ws/session/{id}/events`:

```ts
{ type: "context.slot_updated", data: { slot: ContextSlot; completeness: ContextCompleteness } }
```

Full TypeScript shapes (`ContextSlot`, `ContextLedgerEntry`, `ContextCompleteness`,
`PatientContext`) are in **`API_CONTRACT.md`** and mirrored in `frontend/src/types.ts`.

### Document index

| Doc | What it is |
|---|---|
| `SPEC.md` | System design — turn pipeline, the five base workers, data model, build order |
| `API_CONTRACT.md` | Authoritative frontend↔backend contract: types, REST, WebSocket event union (**includes the PCM**) |
| `PHASE1_CONTEXT_MODEL.md` | The PCM phase in depth — what was added, where it plugs in, what's verified, what's next |
| `DEMO_SCRIPT.md` | The scripted 3-minute acceptance demo |
| `DESIGN.md` | Original product/design notes |
| `FRONTEND_HANDOFF.md` | Frontend implementation handoff notes |

---

## Layout

```
backend/
  db.py                     SQLite layer + schema (context_slots, context_ledger)
  seed.py                   Maria Alvarez seed; derives + seeds the PCM on reset
  orchestrator/
    pcm.py                  PCM core: derive / seed / record_contribution / completeness / shapes
    workers.py              per-turn workers incl. the `pcm` integrator (_handle_pcm, _attribute_turn)
    prompts.py              worker prompts incl. PCM_SYSTEM + the CONTEXT SLOTS block
    tick.py                 per-turn fan-out; `pcm` runs in ACCUMULATOR_WORKERS
  routes/
    context.py             GET /api/visits/{id}/context
frontend/src/
  components/ContextPanel.tsx   readiness meter + gap-first slot rows + provenance/ledger UI
  useSessionEvents.ts           handles context.slot_updated
  screens/SessionScreen.tsx     renders the ContextPanel live
```

## Run

Backend (uses `uv`):

```bash
cd backend
uv venv && uv pip install -r requirements.txt
CLAUDE_API_KEY=sk-... uv run uvicorn main:app --port 8000   # key needed for live extraction
```

Frontend:

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173
```

Drive the orchestrator without a microphone (the integration seam):

```bash
curl -X POST localhost:8000/api/sessions -d '{"node_id":1}' -H 'content-type: application/json'
curl -X POST localhost:8000/api/dev/inject-turn -H 'content-type: application/json' \
  -d '{"session_id":1,"speaker":"patient","text":"The pain is spreading to my left arm."}'
curl localhost:8000/api/visits/1/context     # watch slots flip + completeness climb
```

Without `CLAUDE_API_KEY` the workers fail safe (turns persist, server stays up); the PCM
still serves its seeded belief state, and the deterministic derive/seed/ledger paths work.

## What's next (Phase 2+)

The PCM is the substrate. On top of it: a **Gap Critic** (diff the belief state against
required slots on a slower cadence), an **Acquisition Router** (measurement vs. live clinician
question vs. async patient intake), and a patient-facing **intake agent** that feeds the same
integrator through the existing `inject-turn` seam. See `PHASE1_CONTEXT_MODEL.md`.
