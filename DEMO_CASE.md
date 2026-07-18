# DOC Demo Case — Maria Alvarez

> **Synthetic data.** Every document, name, and clinical detail below is fabricated for a hackathon stage demo. Not medical advice, not a real patient.

---

## 1. Patient snapshot

| Field | Value |
|---|---|
| Name | Maria Alvarez |
| DOB | 1968-03-12 (age 58) |
| Upcoming visit | 2026-07-20, Dr. R. Whitfield (primary care) |
| DOC pre-visit call | 2026-07-18 |

**One-line case:** A 58-year-old woman with hypertension and lifelong migraines has three weeks of exertional chest pressure and a *new, different* headache — but her record is a mess of contradictions (aspirin "allergy" vs. daily aspirin use, "never smoker" vs. "½ PPD"), silent gaps (no ECG ever, a transient word-finding episode nobody chased), and vagueness ("chest feels funny," "vision went weird"). Cardiology and neurology agents both have real work to do.

---

## 2. Seed documents (verbatim — what the agents read)

### Document A — Patient Summary, Dr. R. Whitfield (GP)
*Last updated 2026-07-10*

Maria is a 58 yo woman I have followed since 2019. Pleasant, works part-time at a school cafeteria, lives with husband. Hypertension diagnosed 2015, **well controlled on lisinopril 20 mg daily**, home readings "fine" per patient. Long history of migraine headaches since her thirties — right-sided, throbbing, with the flashing zigzag lights beforehand, responds to rest and OTC analgesia. Otherwise generally healthy, **never smoker**, occasional glass of wine.

Recent months have been bumpy. ED visit in June for a bad headache (CT negative, dx migraine), then an urgent care visit for some visual complaint — notes attached. She called the office this week about her head and her chest; front desk booked her for Monday 7/20. Would like to sort out what is actually going on, she is a poor historian on the phone.

**Allergies: ASPIRIN — hives.** No other known allergies.

---

### Document B — Office Visit Note, Dr. A. Okafor, Internal Medicine (covering)
*2026-05-02*

**S:** 58F HTN f/u. Reports **occasional chest discomfort x few wks — comes on climbing the stairs at home, goes away w/ rest after ~5 min**. No SOB, no diaphoresis. Also "some burning after big meals." Denies HA today.
**O:** BP 142/88 (single reading, R arm). HR 76 reg. Lungs CTA. CV: RRR, no exam abnormality noted.
**A/P:**
1. **Chest discomfort — atypical, likely GERD given postprandial burning. Start omeprazole 20 mg daily. RTC if worse.**
2. HTN — borderline today, cont lisinopril 20 mg, recheck next visit.

*No ECG performed this visit. No labs ordered.*

---

### Document C — Emergency Department Discharge Summary, Mercy General Hospital
*2026-06-20 — Attending: Dr. S. Patel, MD*

**Chief complaint:** Headache.
**HPI:** 58-year-old female presenting with **right-sided throbbing headache** with nausea and light sensitivity since this morning, described as similar to prior migraines but more intense.
**Workup:** CT head without contrast: no acute intracranial abnormality. Vitals stable (BP 156/92 on arrival).
**Exam:** Alert and oriented x3, **neuro exam grossly intact**, ambulating without difficulty.
**Social history:** **Smokes approx. ½ pack per day.** Denies alcohol excess.
**Disposition:** Diagnosed with migraine headache. Treated with IV fluids and antiemetic with good relief. Discharged home in stable condition with **prescription for sumatriptan 50 mg PO PRN migraine** and instructions to follow up with primary care within one week.

---

### Document D — Urgent Care Visit Note, Dr. L. Chen, MedFirst Urgent Care
*2026-06-29*

Ms. Alvarez is a very pleasant 58-year-old lady who presents today at the urging of her husband because, in her own words, **"my vision went weird for a bit"** two days ago. She finds the episode difficult to characterize and I was likewise unable to elicit a more precise description in the time available; it lasted "maybe twenty minutes or so" and resolved on its own without residual deficit that she can identify. She denies eye pain. Of note, she also mentions, almost in passing, that **there was a moment "last week" where she "couldn't find her words" for a few minutes**; this was not further characterized as the patient was in a hurry to pick up her grandson.

She has a longstanding history of migraine with visual aura, and on balance I suspect this represents **probable ocular migraine**. I reassured her at length and advised follow-up with her primary care physician, sooner should symptoms recur. Visual acuity was not formally tested today as the clinic's eye chart was in use; **fundoscopic, pupillary, and visual field examination deferred to PCP**.

---

### Document E — Nurse Triage Phone Note, RN J. Morales
*2026-07-15, 10:42*

Pt called office. States **"my head hurts again, worse than usual"** — points to **left temple** per pt description. Also states **"my chest feels funny"** when climbing the stairs to do laundry. Requesting appointment. Denies fever.

Meds per pt over phone: **lisinopril "I think so??" (pt unsure if still taking)**, omeprazole, sumatriptan as needed, **"baby aspirin" every morning**, Tylenol sometimes.

Advised to call 911 for severe chest pain, weakness, or facial droop. Appt booked 2026-07-20 w/ Dr. Whitfield. Pt verbalized understanding.

---

### Document F — Pharmacy Fill History, CarePoint Pharmacy #204
*Printed 2026-07-14*

| Medication | Sig | Last fill | Supply |
|---|---|---|---|
| Lisinopril 20 mg tab | 1 daily | **2026-01-15** | 90 days *(no refill since — exhausted ~2026-04-15)* |
| Omeprazole 20 mg cap | 1 daily | 2026-06-30 | 30 days (prior fill 2026-05-02) |
| Sumatriptan 50 mg tab | 1 PO PRN migraine, max 2/day | 2026-06-21 | 9 tabs |

*No OTC products on file. No aspirin dispensed at this pharmacy.*

---

## 3. Ground-truth answer key — 12 planted issues

| ID | Category | Conflicting / vague text (quoted) | Specialist | Patient-answerable? | Ideal probing question(s) |
|---|---|---|---|---|---|
| **C1** | Contradiction | Doc A: "Allergies: ASPIRIN — hives" vs. Doc E: "'baby aspirin' every morning" | General / med-rec | Yes | "Your chart says you're allergic to aspirin, but you told the nurse you take a baby aspirin every morning. Have you ever had a reaction to it? Where did the allergy note come from?" |
| **C2** | Contradiction | Doc A: "never smoker" vs. Doc C: "Smokes approx. ½ pack per day" | General (feeds cardio + neuro risk) | Yes | "One record says you've never smoked, another says half a pack a day. Which is right — do you smoke now, and did you ever?" |
| **C3** | Contradiction | Doc C: "right-sided throbbing headache… similar to prior migraines" vs. Doc E: "'my head hurts again, worse than usual' — left temple" | Neurology | Yes | "Is the headache you have now on the same side and the same kind of pain as your usual migraines, or is this one different?" *(Different = red flag; two distinct headaches.)* |
| **C4** | Contradiction | Doc A: "well controlled on lisinopril 20 mg daily" vs. Doc F: last lisinopril fill 2026-01-15, exhausted ~04-15; Doc E: "lisinopril 'I think so??'" | General / med-rec (cardio-relevant) | Yes | "Are you actually still taking the lisinopril every day? When did you last take one, and if you stopped — why?" |
| **C5** *(subtle)* | Contradiction | Doc B HPI: "comes on climbing the stairs… goes away w/ rest after ~5 min" vs. Doc B assessment: "atypical, likely GERD" — the documented pattern is textbook exertional angina, contradicted by the note's own conclusion | Cardiology | Yes (pattern confirmable) | "Does the chest feeling come on only with effort like stairs, and stop within minutes when you rest? Does eating or antacids change it at all?" *(Also flags: sumatriptan Rx from Doc C is contraindicated if this is angina.)* |
| **G1** | Gap | Chest discomfort documented twice (Doc B, Doc E) — no ECG anywhere in record ("No ECG performed this visit") | Cardiology | **No → manual task** | Specialist task: **12-lead ECG in office at 7/20 visit**; compare to none-on-file baseline. |
| **G2** | Gap | Visual episode + headaches, yet Doc D: "fundoscopic, pupillary, and visual field examination deferred to PCP" and Doc C: only "neuro exam grossly intact" | Neurology | **No → manual task** | Specialist task: **fundoscopic exam, pupillary light reflex, formal visual fields, focused neuro exam at 7/20 visit**. |
| **G3** | Gap | Doc D: "couldn't find her words for a few minutes… not further characterized" — transient aphasia never screened for TIA | Neurology | Yes | "Tell me about the day you couldn't find your words — how suddenly did it start, how long did it last, and was there any weakness, numbness, clumsiness, or face drooping with it?" |
| **G4** | Gap | No family history documented in any of the five records | General (cardio-relevant) | Yes → **reveals NEW fact** | "Has anyone in your immediate family had heart attacks, strokes, or aneurysms — especially at a young age?" *(Truth: father died of MI at 54 — in no document.)* |
| **A1** | Ambiguity | Doc E: "my head hurts again, worse than usual" | Neurology | Yes | "Where exactly does it hurt? What does the pain feel like — throbbing, stabbing, pressure? When did this one start? How bad, 0–10? What makes it better or worse?" |
| **A2** | Ambiguity | Doc E: "my chest feels funny" | Cardiology | Yes | "What does 'funny' feel like — pressure, burning, stabbing? Exactly what brings it on, how long does it last, does it go anywhere like your arm or jaw?" |
| **A3** | Ambiguity | Doc D: "my vision went weird for a bit" | Neurology | Yes | "Describe the vision episode: one eye or both? Zigzag shimmering lines, or a dark curtain/blackout? How did it spread, and how long till normal?" *(Zigzag 20 min = aura, reassuring; curtain = amaurosis, urgent.)* |

**Difficulty spread:** C1, C2, A1, A2 are demo-safe obvious. C5 (angina mislabeled GERD by the note's own words) and G3 (buried transient aphasia in Chen's rambling prose) are the impressive subtle catches. G1 and G2 are the two patient-*cannot*-answer items that must surface as manual specialist tasks.

---

## 4. Hidden truth + phone role-play script

### What actually happened (coherent ground truth)

Maria is a 58-year-old **former smoker** (½ pack/day for ~20 years, quit 2018; the ED resident misheard and charted her as current — though she admits to "two or three" cigarettes in the last stressful month). Her father **died of a heart attack at 54** — she has never been asked. She has hypertension but **stopped lisinopril in mid-April** because of a nagging dry cough; she never told anyone and her home BP cuff has dead batteries. The "aspirin allergy" in her chart is a decades-old transcription error — **the hives were from penicillin**; her husband started her on a daily baby aspirin after the ED visit and she's had zero reaction.

For **three weeks** she has had **mid-chest pressure ("like a fist"), 4–5/10, brought on reliably by one flight of stairs or the hill to the bus stop, occasionally spreading to her jaw, gone within five minutes of rest.** Antacids do nothing (the omeprazole was for genuinely separate meal-time burning). This is exertional angina; the May note called it GERD.

Her migraines are real: right-sided, throbbing, preceded by **shimmering zigzag lights over ~20 minutes** — that was the June 20 ED visit and the June 27 "vision went weird" episode. But **~June 22** she had a genuinely different event: **sudden five-minute spell where she couldn't get words out and her right hand went clumsy** (she dropped a coffee mug — she's never told anyone about the hand). That's the TIA-flavored episode buried in Dr. Chen's note. And the **current headache is new and different**: left temple, sharp/stabbing, 8/10, started two days ago (2026-07-16), worse with bright light, not her usual pattern, Tylenol barely touches it. No weakness or numbness right now.

### Phone script (Maria's verbatim lines — role-play from this)

*Rule for the role-player: give the vague first answer; only give the specific detail when the agent asks the follow-up shown. If the agent asks something not covered, improvise consistent with the truth above.*

1. **[Agent: introduces itself, confirms identity, asks what's been going on before Monday's visit]**
   Maria: *"Oh — well, my head hurts, and my chest has been feeling funny. That's mostly it."*
2. **[Agent: let's start with the headache — where does it hurt?]**
   Maria: *"Just… my head. Here on the side."* **[if asked which side]** *"The left. Right at my temple."*
3. **[Agent: what does the pain feel like, and how strong is it 0–10?]**
   Maria: *"It's sharp. Like a little knife poking. Pretty bad — I'd say an eight when it's going."*
4. **[Agent: when did this headache start?]**
   Maria: *"A couple weeks ago I guess…"* **[if pressed: this exact headache, or headaches in general?]** *"Oh, THIS one — this one started two days ago. Thursday. The couple-weeks thing is everything else that's been going on."*
5. **[Agent: is it like your usual migraines?]**
   Maria: *"No, that's the thing. My migraines are on the right side and they throb, and I see the zigzag sparkles first. This one's the other side and it stabs. No sparkles. Bright light makes it worse though. Tylenol doesn't do much."*
   → **resolves C3** (two different headaches; new left-temporal pain confirmed distinct from migraine history).
6. **[Agent: any weakness, numbness, trouble speaking, face drooping now?]**
   Maria: *"No, nothing like that right now."*
7. **[Agent: the urgent care note mentions you couldn't find your words one day — tell me about that]**
   Maria: *"Oh, that was strange. It was a Monday — around the 22nd of June. I was talking to my sister and all of a sudden the words just wouldn't come out. Maybe five minutes. And you know what, my right hand went clumsy too — I dropped my coffee mug. I never told the doctor about the hand, it seemed silly. Then it all went back to normal."*
   → **fills G3**, and the right-hand clumsiness is detail no document has.
8. **[Agent: and the 'vision went weird' episode — one eye or both? What did you see?]**
   Maria: *"Both, I think? It was like shimmering zigzag lines off to one side, and they kind of grew for maybe twenty minutes and then faded. Same as before my migraines, actually. No curtain or blackout or anything."*
   → **resolves A3** as classic aura, distinct from the word-finding spell.
9. **[Agent: now the chest — what does 'funny' mean?]**
   Maria: *"Hard to say. Just funny."* **[if asked: pressure, burning, or stabbing?]** *"Pressure. Like a fist pressing in the middle of my chest."*
10. **[Agent: what brings it on, and how long does it last?]**
    Maria: *"The stairs, mostly. Every time I carry the laundry up. Or the hill to the bus stop. If I stop and stand still it goes away in about five minutes. Been about three weeks now. Maybe a four or five out of ten. Sometimes it kind of creeps up into my jaw, which is odd."*
    → **resolves A2 and confirms C5** (exertional, rest-relieved, jaw radiation — not GERD; antacids *"don't touch it"* if asked).
11. **[Agent: your chart says aspirin gives you hives, but you told the nurse you take a baby aspirin daily — which is it?]**
    Maria: *"Oh, that allergy thing has been in my chart forever and it's wrong. The hives were from penicillin when I was a girl — somebody typed it in wrong years ago. My husband started giving me his baby aspirin after the emergency room in June. Every morning. Never had any problem with it."*
    → **resolves C1** (and surfaces true penicillin allergy for the chart).
12. **[Agent: one note says you never smoked, another says half a pack a day — can you clear that up?]**
    Maria: *"I smoked half a pack a day for twenty years, but I quit in 2018. The young doctor at the ER must have written it down wrong. Although… honestly, I've bummed two or three cigarettes this past month. It's been stressful."*
    → **resolves C2**.
13. **[Agent: are you still taking the lisinopril?]**
    Maria: *"…No. I stopped around April. It gave me this dry cough that drove me crazy, so I just quit taking it. I didn't want to bother anyone. My blood pressure cuff at home needs batteries so I honestly don't know what my pressure's been."*
    → **resolves C4**.
14. **[Agent: any heart attacks, strokes, or aneurysms in your close family?]**
    Maria: *"My father died of a heart attack. He was 54. Nobody's ever asked me that before."*
    → **NEW FACT (G4)** — appears in no seed document.
15. **[Agent: asks something only an exam can answer — e.g., "we'll need to check your pupils' reaction to light and do an ECG tracing of your heart"]**
    Maria: *"I wouldn't know how to do any of that myself, honey. You'll have to check when I come in."*
    → demonstrates the **manual-task handoff** (G1, G2) on stage.
16. **[Agent: wraps up, confirms Monday 7/20, safety-netting: call 911 for chest pain at rest >10 min, sudden weakness, face droop, or worst-ever headache]**
    Maria: *"I will. Thank you — nobody's ever gone through it all like this before."*

---

## 5. The clean output — target post-call intake document

*(This is the "after" screen. Before = five messy documents above; after = this.)*

### Pre-Visit Intake Brief — Maria Alvarez (DOB 1968-03-12) — prepared 2026-07-18 by DOC

**Chief complaints (2):**
1. New-pattern headache, distinct from known migraine.
2. Exertional chest pressure, 3 weeks.

**HPI — Headache:** Acute onset 2026-07-16. Left temporal. Sharp/stabbing. Constant-intermittent over 2 days. Severity 8/10. Worse with bright light; minimal relief from acetaminophen. No radiation. **Explicitly different from baseline migraines** (right-sided, throbbing, preceded by 20-min scintillating zigzag aura). No current focal weakness, numbness, speech difficulty.

**HPI — Chest:** Onset ~3 weeks ago. Mid-sternal pressure, "like a fist." Reproducibly provoked by one flight of stairs / uphill walking; relieved by rest within ~5 min. 4–5/10. Occasional radiation to jaw. Not affected by antacids or meals (postprandial burning is a separate, ongoing symptom). Pattern consistent with exertional angina; contradicts 2026-05-02 GERD assessment.

**Interval neuro event (patient-reported, previously uncharacterized):** ~2026-06-22, sudden onset, ~5 min: expressive word-finding difficulty **plus right-hand clumsiness (dropped mug) — hand symptom not in any prior record.** Full resolution. TIA workup not yet performed.

**Medication reconciliation (resolved):**
| Med | Chart said | Actual |
|---|---|---|
| Lisinopril 20 mg | Taking, "well controlled" | **Stopped ~2026-04 due to dry cough; untreated HTN since. Home BP unknown (cuff broken).** |
| Aspirin 81 mg | Allergic (hives) | **Taking daily since ~2026-06-21, no reaction.** |
| Omeprazole 20 mg | Taking | Taking daily. |
| Sumatriptan 50 mg PRN | Taking PRN | Has it; **flag: hold pending cardiac evaluation (contraindicated in suspected angina).** |
| Acetaminophen | — | PRN, minimal effect on new headache. |

**Allergy correction:** Remove aspirin. **Add: penicillin — hives (childhood).**

**Resolved-contradictions log:** smoking = former ½ PPD ×20 yrs, quit 2018, 2–3 cigarettes past month (was "never" vs "current"); headache laterality = two distinct headache types (was R vs L conflict); lisinopril adherence = stopped April (was "controlled" vs fill lapse); aspirin allergy = charting error (was allergy vs daily use).

**New history:** Father died of MI at age 54 (first-degree premature CAD — previously undocumented).

**Manual tasks for 7/20 visit (patient cannot self-report):**
- [ ] **Cardiology:** 12-lead ECG (none on file despite recurrent exertional chest pain); in-office BP both arms; cardiac auscultation; consider troponin/lipids and stress vs. CT-angio pathway.
- [ ] **Neurology:** fundoscopic exam, pupillary light reflex, formal visual fields, full focal neuro exam; carotid auscultation; expedite TIA workup for the 06-22 aphasia + right-hand episode.
- [ ] **General:** restart antihypertensive (cough on lisinopril — consider ARB); replace home BP cuff batteries / recheck; update allergy list and smoking status in EHR.

**Safety-netting given:** 911 criteria reviewed (rest chest pain >10 min, sudden weakness/speech change/face droop, thunderclap headache). Patient verbalized understanding.
