"""Seeds the demo case from DEMO_CASE.md (§2 documents, verbatim).

Runs at startup and on POST /api/dev/reset. The documents table is append-only
demo data — the pipeline never edits it. The planted issues (C1-C5, G1-G4,
A1-A3) live inside these texts; edit only in lockstep with DEMO_CASE.md.
"""

from config import PATIENT_PHONE
from db import ins, one, wipe_db

PATIENT = {
    "name": "Maria Alvarez",
    "dob": "1968-03-12",
    # The number the telnyx transport dials — the role-player's real phone.
    "phone": PATIENT_PHONE or "+15555550100",
}

DOCUMENTS = [
    {
        "title": "Patient Summary",
        "doc_type": "summary",
        "author": "Dr. R. Whitfield, Primary Care",
        "date": "2026-07-10",
        "content_md": (
            "Maria is a 58 yo woman I have followed since 2019. Pleasant, works part-time at a "
            "school cafeteria, lives with husband. Hypertension diagnosed 2015, **well controlled "
            "on lisinopril 20 mg daily**, home readings \"fine\" per patient. Long history of "
            "migraine headaches since her thirties — right-sided, throbbing, with the flashing "
            "zigzag lights beforehand, responds to rest and OTC analgesia. Otherwise generally "
            "healthy, **never smoker**, occasional glass of wine.\n\n"
            "Recent months have been bumpy. ED visit in June for a bad headache (CT negative, dx "
            "migraine), then an urgent care visit for some visual complaint — notes attached. She "
            "called the office this week about her head and her chest; front desk booked her for "
            "Monday 7/20. Would like to sort out what is actually going on, she is a poor "
            "historian on the phone.\n\n"
            "**Allergies: ASPIRIN — hives.** No other known allergies."
        ),
    },
    {
        "title": "Office Visit Note",
        "doc_type": "visit_note",
        "author": "Dr. A. Okafor, Internal Medicine (covering)",
        "date": "2026-05-02",
        "content_md": (
            "**S:** 58F HTN f/u. Reports **occasional chest discomfort x few wks — comes on "
            "climbing the stairs at home, goes away w/ rest after ~5 min**. No SOB, no "
            "diaphoresis. Also \"some burning after big meals.\" Denies HA today.\n\n"
            "**O:** BP 142/88 (single reading, R arm). HR 76 reg. Lungs CTA. CV: RRR, no exam "
            "abnormality noted.\n\n"
            "**A/P:**\n"
            "1. **Chest discomfort — atypical, likely GERD given postprandial burning. Start "
            "omeprazole 20 mg daily. RTC if worse.**\n"
            "2. HTN — borderline today, cont lisinopril 20 mg, recheck next visit.\n\n"
            "*No ECG performed this visit. No labs ordered.*"
        ),
    },
    {
        "title": "ED Discharge Summary",
        "doc_type": "ed_discharge",
        "author": "Dr. S. Patel, MD — Mercy General Hospital",
        "date": "2026-06-20",
        "content_md": (
            "**Chief complaint:** Headache.\n\n"
            "**HPI:** 58-year-old female presenting with **right-sided throbbing headache** with "
            "nausea and light sensitivity since this morning, described as similar to prior "
            "migraines but more intense.\n\n"
            "**Workup:** CT head without contrast: no acute intracranial abnormality. Vitals "
            "stable (BP 156/92 on arrival).\n\n"
            "**Exam:** Alert and oriented x3, **neuro exam grossly intact**, ambulating without "
            "difficulty.\n\n"
            "**Social history:** **Smokes approx. 1/2 pack per day.** Denies alcohol excess.\n\n"
            "**Disposition:** Diagnosed with migraine headache. Treated with IV fluids and "
            "antiemetic with good relief. Discharged home in stable condition with **prescription "
            "for sumatriptan 50 mg PO PRN migraine** and instructions to follow up with primary "
            "care within one week."
        ),
    },
    {
        "title": "Urgent Care Visit Note",
        "doc_type": "visit_note",
        "author": "Dr. L. Chen, MedFirst Urgent Care",
        "date": "2026-06-29",
        "content_md": (
            "Ms. Alvarez is a very pleasant 58-year-old lady who presents today at the urging of "
            "her husband because, in her own words, **\"my vision went weird for a bit\"** two "
            "days ago. She finds the episode difficult to characterize and I was likewise unable "
            "to elicit a more precise description in the time available; it lasted \"maybe twenty "
            "minutes or so\" and resolved on its own without residual deficit that she can "
            "identify. She denies eye pain. Of note, she also mentions, almost in passing, that "
            "**there was a moment \"last week\" where she \"couldn't find her words\" for a few "
            "minutes**; this was not further characterized as the patient was in a hurry to pick "
            "up her grandson.\n\n"
            "She has a longstanding history of migraine with visual aura, and on balance I "
            "suspect this represents **probable ocular migraine**. I reassured her at length and "
            "advised follow-up with her primary care physician, sooner should symptoms recur. "
            "Visual acuity was not formally tested today as the clinic's eye chart was in use; "
            "**fundoscopic, pupillary, and visual field examination deferred to PCP**."
        ),
    },
    {
        "title": "Nurse Triage Phone Note",
        "doc_type": "triage_note",
        "author": "RN J. Morales",
        "date": "2026-07-15",
        "content_md": (
            "Pt called office 10:42. States **\"my head hurts again, worse than usual\"** — "
            "points to **left temple** per pt description. Also states **\"my chest feels "
            "funny\"** when climbing the stairs to do laundry. Requesting appointment. Denies "
            "fever.\n\n"
            "Meds per pt over phone: **lisinopril \"I think so??\" (pt unsure if still taking)**, "
            "omeprazole, sumatriptan as needed, **\"baby aspirin\" every morning**, Tylenol "
            "sometimes.\n\n"
            "Advised to call 911 for severe chest pain, weakness, or facial droop. Appt booked "
            "2026-07-20 w/ Dr. Whitfield. Pt verbalized understanding."
        ),
    },
    {
        "title": "Pharmacy Fill History",
        "doc_type": "pharmacy",
        "author": "CarePoint Pharmacy #204",
        "date": "2026-07-14",
        "content_md": (
            "| Medication | Sig | Last fill | Supply |\n"
            "|---|---|---|---|\n"
            "| Lisinopril 20 mg tab | 1 daily | **2026-01-15** | 90 days *(no refill since — "
            "exhausted ~2026-04-15)* |\n"
            "| Omeprazole 20 mg cap | 1 daily | 2026-06-30 | 30 days (prior fill 2026-05-02) |\n"
            "| Sumatriptan 50 mg tab | 1 PO PRN migraine, max 2/day | 2026-06-21 | 9 tabs |\n\n"
            "*No OTC products on file. No aspirin dispensed at this pharmacy.*"
        ),
    },
]


def seed_all() -> None:
    if one("SELECT id FROM patients LIMIT 1"):
        return  # already seeded
    pid = ins("patients", **PATIENT)
    for d in DOCUMENTS:
        ins("documents", patient_id=pid, **d)


def reset_and_seed() -> None:
    wipe_db()
    seed_all()
