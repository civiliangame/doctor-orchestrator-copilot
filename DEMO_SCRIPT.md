# DOC Demo Script v2 — "The chart that doesn't lie"

**This script is the acceptance test.** Seed data, prompts, and pacing constants exist to
make these ~3 minutes land. Maria's verbatim phone lines live in `DEMO_CASE.md § 4` — the
role-player performs from there; this file is the presenter's run of show.

Cast: **PRESENTER** (drives the laptop, narrates) and **MARIA** (role-player with a phone,
on speaker). One laptop, projector, internet. Backend on :5000, ngrok up, frontend on :5173.

## Pre-flight (before going on stage)

```bash
curl -X POST http://localhost:5000/api/dev/reset
curl http://localhost:5000/health        # all keys loaded: claude, soniox, telnyx, livekit
# ngrok must be running: ngrok http --url=thoroughly-liberal-mouse.ngrok-free.app 5000
# Maria's phone number is seeded as patients.phone — verify it's the role-player's real phone.
# FALLBACK: if phone/ngrok is dead, run transport "sim" + scripts/replay-demo.mjs (§ Fallback).
```

## Beat 1 — The rotten chart (~25 s)

Patient page for Maria Alvarez. Five documents on screen: GP summary, a covering
internist's SOAP note, an ED discharge, a rambling urgent-care note, a pharmacy fill
history.

> PRESENTER: "Maria sees her doctor Monday. Her chart says she's allergic to aspirin — and
> that she takes aspirin every morning. It says she never smoked — and that she smokes half
> a pack a day. Five documents, four authors, and they don't agree with each other. Every
> clinic in the country has charts like this. DOC cleans them up — before the visit."

Click **Clean Up Context**.

## Beat 2 — The specialist panel (~40 s)

Run view, stages lighting up live. Triage picks the panel (expect: cardiology, neurology,
general medicine); findings stream in per specialist.

Point at, in order:

1. An easy one — **C1**: aspirin allergy vs. daily aspirin, both quotes on the card.
2. The subtle one — **C5**: *"the May note documents textbook exertional angina and then
   calls it reflux — in the same note. Cardiology caught the note contradicting itself."*
3. A gap card marked **can't ask the patient** — no ECG on file (**G1**): *"some things a
   phone call can't answer — watch where those go."*

Then the interview plan streams in: questions with sub-questions and completeness criteria.

> PRESENTER: "Nobody approves anything. It's already dialing her."

## Beat 3 — The call (~90 s)

`call.status: dialing` → **Maria's phone rings on stage. She answers on speaker.**

MARIA performs from `DEMO_CASE.md § 4`: vague first answer, specifics only under
follow-up. The agent drives; she answers whatever it asks. The stage path must hit:

| Moment | What the audience sees/hears |
|---|---|
| "My head hurts" → agent probes side/character/severity/onset | vague → **left temple, stabbing, 8/10, two days** appears in the answer panel (**A1**) |
| "Is it like your usual migraines?" → *"No... other side, and it stabs"* | **C3 resolved** — new headache ≠ migraine |
| "My chest feels funny" → probes → *"a fist... stairs... gone in five minutes... creeps into my jaw"* | **A2 + C5 resolved** — the GERD label falls apart live |
| Aspirin question → *"the hives were from penicillin — somebody typed it in wrong years ago"* | **C1 resolved**, contradiction card flips to resolved |
| Family history → *"My father died of a heart attack. He was 54. Nobody's ever asked me that before."* | **G4 — a fact in no document.** Pause. Let it land. |
| Agent: "we'll need an ECG and to check your pupils when you're in" → *"You'll have to check when I come in, honey"* | manual tasks route to the humans (**G1/G2**) |

Agent wraps with safety-netting; call ends itself. If time is dying, PRESENTER may end it:
the run compiles with whatever was answered.

> PRESENTER (over the compile spinner): "Every answer was recorded by tool call,
> mid-conversation. It kept probing until 'my head hurts' was specific enough for a
> neurologist."

## Beat 4 — Before / after (~25 s)

`intake.ready` → payoff screen: five messy documents on the left, the compiled Pre-Visit
Intake Brief on the right (`DEMO_CASE.md § 5` is the target shape).

Point at: two chief complaints with full HPI · the meds table — *"she stopped her blood
pressure pill in April; her chart said 'well controlled'"* · the sumatriptan
contraindication flag · the manual-task checklist for Monday's visit.

> PRESENTER: "Scribes document the visit. **DOC orchestrates it — starting before the
> patient walks in.** Synthetic data, real pipeline, three minutes."

## Fallback — no phone (sim transport)

Start the run with `{"transport": "sim"}` (dev toggle on the patient page). The identical
pipeline runs; the call happens as text in the run view. Answer as Maria via:

```bash
node scripts/replay-demo.mjs <run_id>        # auto-answers from DEMO_CASE.md's script
# or hand-drive one line:
curl -X POST http://localhost:5000/api/dev/sim-answer -H "Content-Type: application/json" \
     -d '{"call_id": 1, "text": "Oh - well, my head hurts, and my chest has been feeling funny."}'
```

`scripts/replay-demo.mjs` answers the agent's questions from the role-play script
(keyword-matched to the truth in `DEMO_CASE.md`), so the full run — findings, call,
compiled intake — reproduces end-to-end with zero audio. It must stay in sync with
`DEMO_CASE.md`.

## Timing tuning

Demo pacing constants live in `backend/config.py`: max plan questions for the call
(`MAX_INTERVIEW_QUESTIONS`), probe cap per question, specialist timeout. If Beat 3 runs
long in rehearsal, lower `MAX_INTERVIEW_QUESTIONS` before touching prompts — the
orchestrator keeps the highest-severity questions.
