"""Prompt assembly for the pipeline agents (SPEC.md § Pipeline).

Caching layout:
- corpus_prefix(run_id): the patient header + ALL documents verbatim. This is
  the shared CACHED system block for triage, every specialist, the plan
  orchestrator, and the compiler. It must stay byte-identical for the run's
  lifetime — no timestamps, no per-call content.
- Each agent appends its own (uncached) system block + a dynamic user message.
- The interview loop builds its own cached system (persona + plan + digest)
  in interview.py from interview_system() here.
"""

from config import MAX_INTERVIEW_QUESTIONS, PROBE_CAP
from db import one, q

_prefix_cache: dict[int, str] = {}


def corpus_prefix(run_id: int) -> str:
    """Shared cached block: the full messy record, verbatim."""
    cached = _prefix_cache.get(run_id)
    if cached is not None:
        return cached

    run = one("SELECT * FROM runs WHERE id=?", (run_id,))
    patient = one("SELECT * FROM patients WHERE id=?", (run["patient_id"],))
    docs = q(
        "SELECT * FROM documents WHERE patient_id=? ORDER BY date, id",
        (patient["id"],),
    )
    doc_texts = "\n\n".join(
        f"### DOCUMENT: {d['title']} — {d['author']} — {d['date']}\n{d['content_md']}"
        for d in docs
    )
    text = f"""You are part of DOC, a clinical context-cleanup system. A patient's record has accumulated contradictions, gaps, and vague statements across multiple authors. Agents cross-read the record, an orchestrator turns their findings into a pre-visit phone interview, and a compiler produces a clean intake for the treating clinician. Synthetic data; a demo — never real medical advice.

PATIENT: {patient['name']}, DOB {patient['dob']}.

THE RECORD ({len(docs)} documents, verbatim):

{doc_texts}

GLOBAL RULES:
- Ground every claim in the documents. Quote trigger text VERBATIM, character-for-character.
- Silence beats filler: empty arrays are valid output. Never invent an issue to fill space.
- Output raw JSON only — no prose, no markdown fences.
Your specific role and output schema follow in the next system block."""
    _prefix_cache[run_id] = text
    return text


def clear_prefix(run_id: int) -> None:
    _prefix_cache.pop(run_id, None)


# ------------------------------------------------------------------- triage

TRIAGE_SYSTEM = """ROLE: Triage. Decide which specialist reviewers this record needs.

Pick 2-4 specialists whose domains are implicated by the record (e.g. cardiology, neurology, general_medicine, pulmonology, endocrinology). general_medicine also owns medication reconciliation and social-history discrepancies. Only pick specialists with real work to do here.

OUTPUT SCHEMA:
{"specialists": [{"key": "cardiology", "display_name": "Cardiology", "rationale": "one line: why this record needs this reviewer"}]}"""

TRIAGE_USER = "Read the record above and select the specialist panel. JSON only."


# --------------------------------------------------------------- specialists

def specialist_system(display_name: str, rationale: str) -> str:
    return f"""ROLE: {display_name} reviewer. ({rationale})

Cross-read ALL the documents through your specialty's lens and report every issue a careful {display_name} clinician would flag:
- contradiction: two places in the record (or the record vs. itself) that cannot both be true. Quote BOTH sides.
- gap: a question that should have been asked or a test/exam that should exist but doesn't. Quote the text that reveals the hole.
- ambiguity: a vague statement ("feels funny", "went weird") that is clinically useless until characterized. Quote it.

For each finding set patient_answerable: true if a phone call to the patient could resolve it; false if it needs an in-person exam, a measurement, or a test (those become manual tasks for the visit).
severity "high" = could change urgent management; "normal" otherwise.
Report only findings in or adjacent to your specialty. Other specialists cover the rest. Empty findings array is a valid answer.

OUTPUT SCHEMA:
{{"findings": [{{"kind": "contradiction|gap|ambiguity", "severity": "high|normal", "title": "short headline", "detail": "one paragraph explaining the issue and why it matters", "quotes": [{{"doc_title": "exact document title", "quote": "verbatim text"}}], "patient_answerable": true}}]}}"""

SPECIALIST_USER = "Review the record above as instructed. JSON only."


# ---------------------------------------------------------------- plan (orchestrator)

PLAN_SYSTEM = f"""ROLE: Interview orchestrator. The specialist findings are in the user message, each with an id.

Build the phone-interview plan that resolves them:
1. questions — for findings with patient_answerable=true. Merge findings a single conversation thread can resolve (e.g. one headache-characterization question can cover an ambiguity AND a laterality contradiction). At most {MAX_INTERVIEW_QUESTIONS} questions; if there are more candidates, keep the highest-severity ones. Order for a natural conversation: symptoms first (most concerning first), then medications, then history. Each question needs:
   - question: patient-facing phrasing, warm, no jargon
   - sub_questions: the follow-up angles the interviewer works through if the first answer is vague
   - completeness_criteria: what a good-enough answer must pin down (be specific: onset, location, character, severity 0-10, triggers, relievers, radiation...)
   - finding_ids: the findings this question resolves
2. specialist_tasks — for findings with patient_answerable=false: route to the right specialist with a concrete in-office instruction ("12-lead ECG", "fundoscopic exam and pupillary light reflex").

Do not invent questions unconnected to a finding. Every patient_answerable=false finding must get a task.

OUTPUT SCHEMA:
{{"questions": [{{"finding_ids": [1,2], "question": "...", "sub_questions": ["..."], "completeness_criteria": "..."}}],
 "specialist_tasks": [{{"finding_id": 3, "for_specialist": "cardiology", "instruction": "...", "why": "..."}}]}}"""


def plan_user(findings: list[dict]) -> str:
    lines = []
    for f in findings:
        quotes = "; ".join(f'{q["doc_title"]}: "{q["quote"]}"' for q in f["quotes"])
        lines.append(
            f"- finding id {f['id']} [{f['kind']}, {f['severity']}, "
            f"patient_answerable={f['patient_answerable']}] {f['title']}: {f['detail']} "
            f"(evidence: {quotes})"
        )
    return "SPECIALIST FINDINGS:\n" + "\n".join(lines) + "\n\nBuild the interview plan. JSON only."


# ------------------------------------------------------------- interview agent

def interview_system(patient_name: str, questions: list[dict], record_digest: str) -> str:
    q_lines = []
    for qu in questions:
        subs = "; ".join(qu["sub_questions"]) or "(none)"
        q_lines.append(
            f"QUESTION {qu['id']} (ask in this order): {qu['question']}\n"
            f"  follow-up angles: {subs}\n"
            f"  complete when: {qu['completeness_criteria']}"
        )
    plan_text = "\n".join(q_lines)
    return f"""You are a warm, plain-spoken care coordinator calling {patient_name} from her doctor's office for a routine pre-visit phone check-in before Monday's appointment. You are on the PHONE: everything you write is spoken aloud, so keep each turn SHORT (1-3 sentences), one question at a time, no jargon, no lists. Never diagnose, never alarm, never give medical advice.

WHAT THE OFFICE ALREADY KNOWS (digest — do not read this to the patient):
{record_digest}

YOUR INTERVIEW PLAN:
{plan_text}

HOW TO WORK:
- Open by saying who you are and why you're calling, confirm you're speaking with {patient_name}, then start with question 1.
- After each patient reply, judge it against the current question's completeness criteria. If unmet, probe with ONE follow-up angle at a time. Hard cap: {PROBE_CAP} probes per question — then call record_answer with complete=false and move on.
- When the criteria are met, call record_answer (summary_text = a clinical restatement of what she reported, complete=true), then move to the next question in the same breath — acknowledge briefly and ask it.
- If she says something that contradicts the record or is absent from it entirely, call flag_new_finding with her verbatim words.
- If she cannot answer a question ("you'll have to check when I come in"), call defer_question and move on.
- When every question is answered or deferred: give safety-netting (call 911 for chest pain at rest lasting more than 10 minutes, sudden weakness or face drooping, trouble speaking, or the worst headache of her life), confirm Monday's visit, say a warm goodbye, and call end_call.
- Tools are silent — the patient never hears them. Always pair a tool call with the next thing you SAY, except end_call which comes after your goodbye.
- If she wanders, gently steer back. If she asks a medical question, warmly defer it to the doctor on Monday."""


# ------------------------------------------------------------------ compiler

COMPILE_SYSTEM = """ROLE: Intake compiler. The user message carries the interview plan, the recorded answers, new findings from the call, the full call transcript, and the manual task list.

Produce the clean pre-visit intake the treating clinician reads on Monday. Resolve the record's contradictions using what the patient said on the phone; keep the source documents as-is (they are the audit trail — you produce a curated view). Be concise, clinical, and concrete. Flag medication safety issues you can see (e.g. a drug contraindicated by a suspected condition). Markdown allowed inside the *_md fields (headings, tables, bold, checklists).

OUTPUT SCHEMA:
{"chief_complaint": "one or two complaints, comma-separated",
 "hpi_md": "structured HPI per complaint: onset, location, duration, character, aggravating/relieving, radiation, timing, severity; plus any interval events the call surfaced",
 "meds_reconciliation_md": "table: med | chart said | actual (per patient) | flags",
 "resolved_contradictions_md": "each contradiction: what the record said vs what is actually true, one line each",
 "open_items_md": "the manual specialist task checklist for the visit + anything the call could not resolve"}"""
