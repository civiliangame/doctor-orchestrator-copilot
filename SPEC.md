# DOC Spec v2 — Context-Rot Cleanup

Locked decisions for the pivot (2026-07-18). Supersedes `DESIGN.md` and spec v1 (the live
in-room session) entirely. `API_CONTRACT.md` is the authoritative frontend↔backend contract;
`DEMO_SCRIPT.md` is the acceptance test; `DEMO_CASE.md` is the seeded case + ground-truth
answer key + Maria's role-play script.

## What the product does now

Medical records rot: contradictions accumulate across authors, vague complaints ("my head
hurts") get charted verbatim, and questions that should have been asked never are. DOC
cleans a patient's context **before** the visit: a panel of specialist agents cross-reads the
record, an orchestrator turns what they find into an interview plan, a voice agent phones
the patient and probes until every vague thing is clinically specific, and a compiler emits
a clean intake. What the patient can't answer becomes manual tasks for human specialists.

One-liner: **"DOC calls your patient before you ever see them — and hands you a chart that
doesn't lie to you."**

## Decisions log

1. **The live in-room session is dead.** The 5-worker per-turn orchestrator, mic relay, and
   session screen are removed. The event-bus, DB-helper, config-only-env, and seam patterns
   survive.
2. **One FastAPI app, port 5000.** UI REST + run events WS + Telnyx webhook + `/media-stream`
   all in one process (ngrok `thoroughly-liberal-mouse.ngrok-free.app` → 5000 gives Telnyx a
   public route; the frontend talks to localhost:5000 directly, CORS allows 5173).
3. **A run is fully automatic.** `POST /api/patients/{id}/runs` drives
   analyzing → planning → calling → compiling → done with no human gate. Every intermediate
   artifact is persisted and broadcast the moment it exists so the UI narrates the run live.
4. **The specialist panel is dynamic.** A triage call picks 2–4 specialists per run. Models
   propose *which specialists*, code creates the rows — same principle as v1's "models never
   edit the journey graph."
5. **The interview loop is transport-agnostic.** One conversation engine; transports only
   move utterances: `sim` (text in via `POST /api/dev/sim-answer`, text out via events) and
   `telnyx` (real phone). Both emit the identical event stream. This is the v2 version of
   the `inject-turn` seam — everything is buildable and testable without a phone.
6. **Telnyx integration ports the AHH pattern** (github.com/civiliangame/AHH, analyzed
   2026-07-18): raw REST via httpx, no SDK. See § Telnyx transport.
7. **Phone voice pipeline is STT → LLM → TTS**, not speech-to-speech: Soniox STT
   (`stt-rt-v5`), the interview loop as the LLM, LiveKit Inference TTS (uses the LiveKit
   Cloud creds already in `.env`; no separate TTS vendor key). Audio is PCMU 8 kHz on the
   wire; transcode at the boundary (`audioop-lts`).
8. **`documents` are append-only.** Agents never rewrite the record; the compiled `intake`
   is a curated view. New facts discovered on the call become `findings` rows
   (`specialist_id: null`), not document edits.
9. **Silence is still a valid output.** Specialists may return zero findings; the interview
   agent asks nothing not in the plan except follow-ups; verbatim quotes are mandatory
   evidence on every finding.

## Pipeline

```
POST /api/patients/{id}/runs
  → triage (Sonnet): all documents → [{key, display_name, rationale}] × 2–4
  → specialist agents (Sonnet, parallel, one per pick):
        findings[] {kind: contradiction|gap|ambiguity, title, detail,
                    quotes[{doc_title, quote}], patient_answerable, severity}
        — each persists + broadcasts as it returns (no barrier)
  → orchestrator (Fable, Opus fallback): all findings → dedupe/merge →
        interview_questions[] (ordered, with sub_questions + completeness_criteria)
        specialist_tasks[]   (patient_answerable=false findings)
        — questions stream to the UI as they're parsed; plan.ready fires last
  → interview call (transport: sim | telnyx):
        loop until end_call: agent asks → patient answers → agent probes or records
  → compiler (Fable, Opus fallback): plan + answers + call transcript →
        intake {chief_complaint, hpi_md, meds_reconciliation_md,
                resolved_contradictions_md, open_items_md}
  → run done
```

**Prompt caching:** triage, every specialist, and the orchestrator share one byte-identical
cached prefix: the patient header + all documents verbatim. Per-agent system text and
dynamic content append after it. The interview loop maintains its own cached prefix
(persona + full interview plan + record digest); each patient utterance extends the
conversation. Keep prefixes byte-identical or the cache breaks.

**Worker/model map** (constants in `config.py`):

| Stage | Model | Notes |
|---|---|---|
| triage | Sonnet | one call, JSON out |
| specialists | Sonnet | parallel, one per specialist, JSON out |
| orchestrator plan | Fable → Opus fallback | quality matters most here |
| interview loop | Sonnet | latency-critical, tool-use loop |
| compiler | Fable → Opus fallback | the payoff artifact |

## The interview agent

System prompt carries: warm plain-spoken phone persona ("this is a routine pre-visit call
from Dr. Chen's office"), the full interview plan, a digest of the record, and the rules:

- One question at a time, no medical jargon, never diagnose or alarm.
- Work the plan in `order`; mark each question `asking` before speaking it.
- After each patient utterance, judge it against the question's `completeness_criteria`:
  if unmet, probe with a `sub_questions` angle; if met, call `record_answer` and move on.
  Hard cap ~3 probes per question — then record what was gotten (`complete: false`) and move on.
- Tools: `record_answer(question_id, summary_text, complete)`,
  `flag_new_finding(kind, title, detail, quote)` for facts that contradict the record or
  are absent from it, `defer_question(question_id, reason)` when the patient can't answer
  (backend converts to a `specialist_tasks` row), `end_call(reason)` when the plan is
  exhausted or the patient begs off.
- Tool results return the next plan state, so the model always knows what's left.

The loop is turn-based and synchronous per call: one in-flight model call at a time; a
patient utterance arriving mid-call-generation is buffered and appended to the next turn
(phone conversations are naturally half-duplex; barge-in only flushes audio, it doesn't
spawn concurrent ticks).

## Telnyx transport

Ported from AHH. All raw REST (`httpx`), env via `config.py` only.

- **Dial:** `POST {TELNYX_API_BASE}/calls`, `Authorization: Bearer {TELNYX_API_KEY}`, body
  `{connection_id, to, from, stream_url, stream_track: "inbound_track",
  stream_bidirectional_mode: "rtp", stream_bidirectional_codec: "PCMU"}`. Stream params ride
  on the dial request — Telnyx opens the media WS when the callee answers. Per-call context
  (run_id/call_id) travels as query params on `stream_url` —
  `wss://{PUBLIC_HOSTNAME}{STREAM_PATH}?call_id=...`. Strip any scheme off `PUBLIC_HOSTNAME`
  before building the `wss://` URL.
- **Webhook** `POST /webhook`: ACK everything with 200. Outbound needs no webhook logic
  (streaming params are on the dial); hangup is detected by the media WS `stop` event.
  Also map `call.hangup` → end the call defensively.
- **Media WS** `/media-stream` (Telnyx connects to us): JSON text frames.
  In: `{"event":"start"|"media"|"stop"|"dtmf", ...}`; media payloads are ~20 ms base64
  G.711 μ-law 8 kHz mono; **filter `media.track == "inbound"`** or you echo yourself.
  Out: `{"event":"media","media":{"payload":"<b64 μ-law>"}}` and `{"event":"clear"}` to
  flush queued audio on barge-in.
- **STT:** relay inbound μ-law → PCM16 16 kHz (`audioop-lts`: `ulaw2lin` + `ratecv`) →
  Soniox WS. Soniox end-of-turn + the v1 debounce constant = end of patient utterance →
  feed the interview loop.
- **TTS:** agent text → LiveKit Inference TTS → PCM16 → μ-law 8 kHz → media frames.
  Speak nothing until BOTH the Telnyx `start` frame arrived and the TTS/STT pipeline is
  ready (greeting race — AHH gotcha). On barge-in (speech started while agent audio is
  queued): send `clear`, stop feeding TTS frames.
- Expect and swallow bad frames; no keepalives needed for short calls; **never run uvicorn
  `--reload` during a live call**.

## Data model (SQLite)

```
patients        (id, name, dob, phone)
documents       (id, patient_id, title, doc_type, author, date, content_md)   -- APPEND-ONLY
runs            (id, patient_id, status: analyzing|planning|calling|compiling|done|failed,
                 transport: sim|telnyx, started_ts, ended_ts NULL)
specialists     (id, run_id, key, display_name, rationale, status: running|done)
findings        (id, run_id, specialist_id NULL, kind: contradiction|gap|ambiguity,
                 severity: high|normal, title, detail, quotes_json, patient_answerable)
questions       (id, run_id, finding_ids_json, ord, question, sub_questions_json,
                 completeness_criteria, status: pending|asking|answered|deferred)
specialist_tasks(id, run_id, finding_id, for_specialist, instruction, why)
calls           (id, run_id, transport, telnyx_call_control_id NULL,
                 status: dialing|active|ended, started_ts, ended_ts NULL)
call_turns      (id, call_id, speaker: agent|patient, text, ts)
answers         (id, question_id, summary_text, complete, ts)
intakes         (id, run_id, chief_complaint, hpi_md, meds_reconciliation_md,
                 resolved_contradictions_md, open_items_md, created_ts)
```

`seed.py` seeds `DEMO_CASE.md`'s patient + five documents at startup and on
`POST /api/dev/reset`.

## Latency budgets

- Click → first `specialist.selected`: < 4 s (triage is one small call).
- Findings stream in per-specialist; no barrier before the orchestrator *except* the
  orchestrator needs all findings — that barrier is inherent, so specialists get a hard
  ~25 s timeout (skip stragglers, log it).
- Phone: patient end-of-utterance → agent audio starts: **< 2.5 s** (Sonnet + streamed TTS;
  first sentence of TTS can start before the model finishes).
- Sim: same loop minus audio; effectively instant transport.

## Env (all read via `backend/config.py` only)

Existing: `CLAUDE_API_KEY`/`ANTHROPIC_API_KEY`, `SONIOX_API_KEY`, `LIVEKIT_URL`,
`LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `PUBLIC_HOSTNAME`, `STREAM_PATH`,
`TELNYX_CONNECTION_ID`, `TELNYX_FROM_NUMBER`, `TELNYX_API_KEY`.
New constants: `PORT=5000`, `TELNYX_API_BASE=https://api.telnyx.com/v2`, model tiers,
utterance debounce, probe cap, specialist timeout.
