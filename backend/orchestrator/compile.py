"""Stage 5: the intake compiler — the payoff artifact (SPEC.md § Pipeline).

Fable (Opus fallback). Source documents are untouched (append-only audit
trail); the intake is a curated view. Never leaves the run hanging: any
failure still produces a minimal intake so the demo reaches the payoff screen.
"""

import logging

import events
import serialize
from config import MODEL_FABLE
from db import ins, now_iso, one, q
from llm import block, cached_block

from orchestrator import prompts
from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.compile")


async def compile_intake(run_id: int) -> dict:
    answers = q(
        """SELECT a.*, qu.question FROM answers a
           JOIN questions qu ON qu.id = a.question_id
           WHERE qu.run_id=? ORDER BY a.ts""",
        (run_id,),
    )
    turns = q(
        """SELECT ct.* FROM call_turns ct JOIN calls c ON c.id = ct.call_id
           WHERE c.run_id=? ORDER BY ct.id""",
        (run_id,),
    )
    new_findings = q(
        "SELECT * FROM findings WHERE run_id=? AND specialist_id IS NULL", (run_id,)
    )
    tasks = q("SELECT * FROM specialist_tasks WHERE run_id=? ORDER BY id", (run_id,))
    deferred = q(
        "SELECT * FROM questions WHERE run_id=? AND status IN ('deferred','pending','asking')",
        (run_id,),
    )

    answer_lines = "\n".join(
        f"- Q: {a['question']}\n  A ({'complete' if a['complete'] else 'incomplete'}): {a['summary_text']}"
        for a in answers
    ) or "(no answers recorded)"
    new_lines = "\n".join(
        f"- [{f['kind']}] {f['title']}: {f['detail']}" for f in new_findings
    ) or "(none)"
    task_lines = "\n".join(
        f"- [{t['for_specialist']}] {t['instruction']} ({t['why']})" for t in tasks
    ) or "(none)"
    deferred_lines = "\n".join(f"- {d['question']}" for d in deferred) or "(none)"
    transcript = "\n".join(f"{t['speaker'].upper()}: {t['text']}" for t in turns)

    user = f"""RECORDED ANSWERS:
{answer_lines}

NEW FACTS SURFACED ON THE CALL (absent from or contradicting the record):
{new_lines}

MANUAL SPECIALIST TASKS FOR THE VISIT:
{task_lines}

QUESTIONS NOT RESOLVED ON THE CALL:
{deferred_lines}

FULL CALL TRANSCRIPT:
{transcript}

Compile the pre-visit intake. JSON only."""

    try:
        out = await complete_json(
            MODEL_FABLE,
            [cached_block(prompts.corpus_prefix(run_id)), block(prompts.COMPILE_SYSTEM)],
            user,
            max_tokens=4000,
        )
    except Exception:
        log.exception("compiler failed (run=%s) — writing minimal intake", run_id)
        out = {
            "chief_complaint": "See recorded answers",
            "hpi_md": answer_lines,
            "meds_reconciliation_md": "",
            "resolved_contradictions_md": "",
            "open_items_md": task_lines,
        }

    iid = ins(
        "intakes", run_id=run_id,
        chief_complaint=str(out.get("chief_complaint", "")),
        hpi_md=str(out.get("hpi_md", "")),
        meds_reconciliation_md=str(out.get("meds_reconciliation_md", "")),
        resolved_contradictions_md=str(out.get("resolved_contradictions_md", "")),
        open_items_md=str(out.get("open_items_md", "")),
        created_ts=now_iso(),
    )
    row = one("SELECT * FROM intakes WHERE id=?", (iid,))
    await events.broadcast(run_id, "intake.ready", serialize.intake(row))
    return row
