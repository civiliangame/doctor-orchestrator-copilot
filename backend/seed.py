"""Seed data — the source of truth is DEMO_SCRIPT.md + SPEC.md § Seed data.

Everything here exists to make the scripted 3-minute demo land. The guardrail
numbers, the aspirin note, and the prior-visit details are all referenced
verbatim by the script's trigger lines — edit with care.

The journey is seeded WITH goals and guardrails already in place so the demo
survives even if Beat D (plan/generate) is skipped in a rehearsal; a live
plan/confirm overwrites them.
"""

import json

from config import PATIENTS_DIR
from db import ex, ins, now_iso, one

# Hand-written patient summary — used VERBATIM as the orchestrator prompt block.
MARIA_SUMMARY = """Maria Alvarez, 58. Hypertension x6 years, controlled on lisinopril 10 mg daily. \
Borderline-high LDL (132 mg/dL, not on a statin). No diabetes. No prior cardiac events, no known CAD. \
Former smoker, quit 2009.

Last visit 2026-07-11 (Dr. Zhang, primary care): intermittent chest pain x2 weeks — pressure-like, \
mostly with exertion, NOT radiating at that visit. No shortness of breath, no diaphoresis, no numbness. \
BP 138/86, HR 78. Resting ECG unremarkable. STARTED ASPIRIN 81 MG DAILY at that visit. \
History of stomach upset with NSAIDs (ibuprofen) — counseled to take aspirin with food. \
Plan: one-week follow-up (today's visit), chest CT if pain persists, escalation criteria per guardrails."""

INTENT_TEXT = """Follow-up in one week. Main question: has the chest pain progressed? If the pain radiates \
to the arm, jaw, or back, or she reports numbness or shortness of breath — escalate: I want a cardiology \
consult before any imaging. Confirm she's tolerating the daily aspirin (81mg); she's had stomach trouble \
with NSAIDs before. Chest CT if the pain persists. Recheck BP — if it's above 160/100, hold imaging and call me."""

CARDIOLOGY_INSERT = {
    "station": "cardiology",
    "specialist_name": "Dr. Osei",
    "specialist_profile": "Cardiologist — urgent consult slot",
    "before_station": "imaging",
}


def seed_all() -> None:
    from orchestrator import chart_md

    if one("SELECT id FROM patients LIMIT 1") is None:
        _seed_maria()
    else:
        # Databases seeded before the markdown chart bridge: link Maria to her file.
        ex("UPDATE patients SET md_file=? WHERE name='Maria Alvarez' AND md_file=''",
           (chart_md.DEMO_MD_FILE,))
    seed_dataset_patients()
    chart_md.ensure_demo_patient_file()


def _seed_maria() -> None:
    from orchestrator import chart_md

    ts = now_iso()
    patient_id = ins(
        "patients", name="Maria Alvarez", dob="1968-03-12", summary_text=MARIA_SUMMARY,
        md_file=chart_md.DEMO_MD_FILE,
    )
    visit_id = ins(
        "visits", patient_id=patient_id, date="2026-07-18",
        intent_text=INTENT_TEXT, plan_confirmed=0,
    )

    nurse = ins(
        "journey_nodes", visit_id=visit_id, station="nurse",
        specialist_name="Nurse Kim",
        specialist_profile="Intake nurse — vitals, symptom review, medication reconciliation",
        goals_json=json.dumps([
            "Assess chest pain progression since last week — especially radiation to arm/jaw/back, numbness, or shortness of breath",
            "Verify daily aspirin 81mg adherence and stomach tolerance",
            "Recheck blood pressure",
        ]),
        status="active", position=1, sched_time="09:00",
    )
    imaging = ins(
        "journey_nodes", visit_id=visit_id, station="imaging",
        specialist_name="Tech Rivera",
        specialist_profile="CT imaging technician",
        goals_json=json.dumps([
            "Chest CT",
            "Prioritize any regions flagged during intake",
        ]),
        status="pending", position=2, sched_time="10:30",
    )
    doctor = ins(
        "journey_nodes", visit_id=visit_id, station="doctor",
        specialist_name="Dr. Zhang",
        specialist_profile="Primary care physician — Maria's attending",
        goals_json=json.dumps([
            "Review intake and imaging findings",
            "Decide on medication escalation and cardiology follow-up",
        ]),
        status="pending", position=3, sched_time="13:00",
    )
    ins("journey_edges", visit_id=visit_id, from_node_id=nurse, to_node_id=imaging)
    ins("journey_edges", visit_id=visit_id, from_node_id=imaging, to_node_id=doctor)

    # Guardrail numbers are load-bearing: DEMO_SCRIPT.md and the worker prompts cite them.
    ins("guardrails", visit_id=visit_id, num=1,
        condition_text="Chest pain radiating to the arm, jaw, or back",
        action_text="Escalate: cardiology consult before any imaging",
        proposed_insert_json=json.dumps(CARDIOLOGY_INSERT))
    ins("guardrails", visit_id=visit_id, num=2,
        condition_text="New numbness or shortness of breath",
        action_text="Escalate: cardiology consult before any imaging (same escalation as #1)",
        proposed_insert_json=json.dumps(CARDIOLOGY_INSERT))
    ins("guardrails", visit_id=visit_id, num=3,
        condition_text="Aspirin non-adherence or GI side effects",
        action_text="Flag to Dr. Zhang before continuing the aspirin plan",
        proposed_insert_json=None)
    ins("guardrails", visit_id=visit_id, num=4,
        condition_text="Blood pressure above 160/100",
        action_text="Hold imaging; call Dr. Zhang",
        proposed_insert_json=None)

    # Dr. Zhang's standing brief for the intake nurse — this is what renders BIG
    # on the nurse's patient page before the session starts.
    ins("node_briefs", node_id=nurse, from_node_id=doctor, from_station="doctor",
        summary_md=(
            "One-week follow-up for **intermittent exertional chest pain** (onset ~3 weeks ago). "
            "Last week: pressure-like, non-radiating, ECG unremarkable, BP 138/86. "
            "Started **aspirin 81mg daily** — she has a history of stomach trouble with NSAIDs. "
            "Escalation criteria are active as guardrails #1–#4."
        ),
        action_items_json=json.dumps([
            {"text": "Ask about pain progression — radiation to arm/jaw/back, numbness, shortness of breath", "priority": "high"},
            {"text": "Verify daily aspirin 81mg adherence and stomach tolerance", "priority": "high"},
            {"text": "Recheck blood pressure", "priority": "normal"},
        ]),
        created_ts=ts)

    # Patient Context Model: derive the slots this visit needs from the guardrails +
    # goals just seeded, then fill what the record already establishes (with provenance).
    from orchestrator import pcm
    pcm.derive_required_slots(visit_id)
    pcm.seed_context(visit_id)


def seed_dataset_patients() -> None:
    """One patient + visit + minimal nurse->doctor journey per entry in
    seed/patients/index.json. Idempotent per patient (keyed on md_file), so new
    dataset files are picked up on restart without reseeding. The PCM for these
    visits is NOT seeded here — chart_md.sync_from_markdown ingests each patient's
    markdown file (LLM extraction) when their first session starts."""
    index_path = PATIENTS_DIR / "index.json"
    if not index_path.exists():
        return
    roster = json.loads(index_path.read_text(encoding="utf-8")).get("patients", [])
    for i, p in enumerate(roster):
        if one("SELECT id FROM patients WHERE md_file=?", (p["file"],)):
            continue
        patient_id = ins(
            "patients", name=p["name"], dob=p["birth_date"],
            summary_text=p["summary_text"], md_file=p["file"],
        )
        visit_id = ins(
            "visits", patient_id=patient_id, date=p["visit_date"],
            intent_text="", plan_confirmed=0,
        )
        sched = f"{9 + i // 4:02d}:{(i % 4) * 15:02d}"
        nurse = ins(
            "journey_nodes", visit_id=visit_id, station="nurse",
            specialist_name="Nurse Kim",
            specialist_profile="Intake nurse — vitals, symptom review, medication reconciliation",
            goals_json=json.dumps([
                f"Intake for: {p['visit_title']}",
                "Record vitals and current symptoms",
                "Reconcile current medications",
            ]),
            status="active", position=1, sched_time=sched,
        )
        doctor = ins(
            "journey_nodes", visit_id=visit_id, station="doctor",
            specialist_name="Attending physician",
            specialist_profile="Attending — reviews intake findings and sets the plan",
            goals_json=json.dumps([
                "Review intake findings",
                f"Address: {p['visit_title']}",
            ]),
            status="pending", position=2, sched_time="",
        )
        ins("journey_edges", visit_id=visit_id, from_node_id=nurse, to_node_id=doctor)
