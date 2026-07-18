# DOC Demo Script — verbatim

**This script is the spec.** Seed data, guardrails, and prompts are built to make these exact
lines land. Two role-players: **STAFF** (plays Dr. Zhang, Nurse Kim, and the imaging tech) and
**PATIENT** (plays Maria Alvarez). One laptop, one mic, ~3 minutes.

Patient: **Maria Alvarez, 58** — chest-pain follow-up. Seeded record in `SPEC.md § Seed data`.

Trigger lines are marked. Say them close to verbatim — the guardrail and contradiction
detection are tuned to them, and paraphrasing is fine but don't drop the key phrases
(**"spreading to my left arm"**, **"taking the aspirin every day"**).

---

## Beat D — "Last week" (0:00–0:35)

*Screen: Dr. Zhang's planning view.*

**PRESENTER:** "Last week, Maria Alvarez saw Dr. Zhang for new chest pain. Here's how that
visit ended — Dr. Zhang writes what the *next* visit is for."

**STAFF (as Dr. Zhang)** types (may be pre-typed; hit Generate live):

> Follow-up in one week. Main question: has the chest pain progressed? If the pain radiates
> to the arm, jaw, or back, or she reports numbness or shortness of breath — escalate: I want
> a cardiology consult before any imaging. Confirm she's tolerating the daily aspirin (81mg);
> she's had stomach trouble with NSAIDs before. Chest CT if the pain persists. Recheck BP —
> if it's above 160/100, hold imaging and call me.

*Expected: DOC fills the seeded journey (Nurse Intake → Imaging → Dr. Zhang) with per-node
goals and numbered guardrails. Dr. Zhang clicks Confirm.*

**PRESENTER:** "That intent normally dies in a free-text note. DOC carries it into the room."

---

## Beat A — Nurse intake, live voice (0:35–2:15)

*Screen: nurse's appointments list → click "Maria Alvarez" → patient page (brief, action
items, journey line) → click **Start Session**. Mic is live from here.*

The first spoken line anchors diarization: **first speaker = staff.** Turns strictly
alternate from here — do not talk over each other.

**NURSE:** "Hi Maria, I'm Nurse Kim — how are you doing today?"

**PATIENT:** "I'm okay. The chest pain is still there, though. It comes and goes."

> *DOC: suggestion card — "Ask whether the pain has changed location or character since last
> week" (reason: Dr. Zhang's goal #1).*

**NURSE:** "Has the pain changed at all since last week — moved anywhere, or felt different?"

**PATIENT:** "Actually, yeah — the past couple of days it's been **spreading to my left arm**."
⚡ **GUARDRAIL TRIGGER (#1)**

> *DOC, within ~3s — the climax, give it a beat of silence:*
> - *Red guardrail alert: "Dr. Zhang's guardrail: radiating pain → escalate. Cardiology
>   consult before imaging." citing the trigger verbatim.*
> - *Suggestion: "Ask about numbness and shortness of breath now."*
> - *Journey mutation proposal: "Insert **Cardiology consult** before Imaging?" [Accept]*

**NURSE** clicks **Accept** — *the journey line visibly re-routes on screen.*

**NURSE:** "Okay, that's important — any numbness in that arm, or any shortness of breath?"

**PATIENT:** "A little tingling in my fingers this morning. No trouble breathing."

> *DOC: chart updates append; to-do added for the Cardiology node ("Evaluate radiating pain
> with finger paresthesia, onset ~2 days").*

**NURSE:** "Are you still taking your medications — the lisinopril and the aspirin?"

**PATIENT:** "The blood pressure pill, yes, every morning. The aspirin was bothering my
stomach, so I stopped it — maybe two weeks ago." 🌱 **CONTRADICTION SEED**

> *DOC: chart update ("reports stopping aspirin ~2 wks ago, GI upset") + guardrail #3 flag
> (aspirin non-adherence → flag to Dr. Zhang).*

**NURSE:** "Got it. And this morning — did you take anything before coming in?"

**PATIENT:** "Just my usual pills. I've been **taking the aspirin every day** like Dr. Zhang
said." ⚡ **CONTRADICTION TRIGGER**

> *DOC: amber contradiction card, both sources cited verbatim — the in-session statement
> ("the aspirin was bothering my stomach, so I stopped it") and the visit-N note (daily 81mg
> aspirin prescribed). Suggested probe: "Ask when she last actually took an aspirin."*

**NURSE:** "Just so I have it right — when did you last actually take an aspirin?"

**PATIENT:** "…Honestly, it's been a couple of weeks. I didn't want Dr. Zhang to think I
wasn't following the plan."

> *DOC: chart update — "Confirmed: aspirin stopped ~2 weeks ago (GI upset); initially
> misreported adherence."*

**NURSE:** "Thanks for being honest — that's exactly what we need to know. Let me get your
blood pressure." *(pause, mimes cuff)* "One forty-two over eighty-eight."

> *DOC: vital appended; guardrail #4 not tripped (below 160/100), imaging not blocked.*

**NURSE:** "All right — we're going to have cardiology take a look first, then imaging, and
Dr. Zhang will see you after that."

**NURSE** clicks **End Session**.

> *DOC: Fable compiles — handoff briefs appear on the Cardiology and Imaging nodes;
> the to-do list is reconciled (answered items closed, escalation items promoted).*

---

## Beat C — Imaging (2:15–2:45)

**PRESENTER:** "An hour later — cardiology has cleared her for imaging."
*(Operator: mark the Cardiology node complete via the dev control, off-screen, before this.)*

*Screen: imaging tech opens Maria's page. The brief shows the action items: "Radiating-pain
escalation in effect. Prioritize views of the upper-left thoracic region."*

**STAFF (as tech)** uploads the pre-selected CT slice.

> *DOC: multimodal read appends findings to the chart, framed as "flagged for Dr. Zhang's
> review" — never a diagnosis.*

---

## Payoff — Dr. Zhang's screen (2:45–3:00)

*Screen: Dr. Zhang's view of Maria — the straight-line journey with completed nodes, the
accumulated chart grouped by station, the contradiction entry surviving into the handoff, and
the compiled action items.*

**PRESENTER:** "Every department saw what the last one learned, and what the doctor wanted
checked. Scribes document the visit — **DOC orchestrates it.**"

---

## Operator notes & contingencies

- **Mic:** single laptop mic, role-players ~2ft away, patient slightly closer. Rehearse levels.
- **Turn-taking:** strict alternation, full stop between speakers. Diarization is advisory;
  alternation is authoritative — a diarization glitch is invisible if you don't overlap.
- **H9 fallback (if end-of-turn detection is flaky):** operator presses the off-screen
  "end patient turn" key after each PATIENT line. Invisible to judges.
- **Beat D text** is pre-typed in the box before the demo starts; only Generate is clicked live.
- **Backup:** screen recording of one clean run exists before demo day (Success Criteria).
- **Disclaimer banner** visible in every view: synthetic data, not medical advice.
