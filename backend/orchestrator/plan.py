"""Stage 3: the orchestrator merges findings into the interview plan.

Fable (Opus fallback) — quality matters most here. Questions broadcast one by
one as parsed, then plan.ready. Backend guarantees every patient_answerable=0
finding ends up with a specialist_task even if the model missed it.
"""

import json
import logging

import events
import serialize
from config import MAX_INTERVIEW_QUESTIONS, MODEL_FABLE
from db import ins, one, q
from llm import block, cached_block

from orchestrator import prompts
from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.plan")


async def build_plan(run_id: int) -> None:
    finding_rows = q("SELECT * FROM findings WHERE run_id=? ORDER BY id", (run_id,))
    findings = [serialize.finding(r) for r in finding_rows]
    if not findings:
        await events.broadcast(run_id, "plan.ready",
                               {"id": run_id, "question_count": 0, "task_count": 0})
        return

    out = await complete_json(
        MODEL_FABLE,
        [cached_block(prompts.corpus_prefix(run_id)), block(prompts.PLAN_SYSTEM)],
        prompts.plan_user(findings),
        max_tokens=3000,
    )

    valid_ids = {f["id"] for f in findings}
    q_count = 0
    for i, qu in enumerate(out.get("questions", [])[:MAX_INTERVIEW_QUESTIONS]):
        try:
            fids = [fid for fid in qu.get("finding_ids", []) if fid in valid_ids]
            qid = ins(
                "questions", run_id=run_id,
                finding_ids_json=json.dumps(fids), ord=i,
                question=str(qu["question"]),
                sub_questions_json=json.dumps([str(s) for s in qu.get("sub_questions", [])]),
                completeness_criteria=str(qu.get("completeness_criteria", "")),
                status="asking" if i == 0 else "pending",
            )
            row = one("SELECT * FROM questions WHERE id=?", (qid,))
            await events.broadcast(run_id, "plan.question", serialize.question(row))
            q_count += 1
        except Exception:
            log.exception("bad question from planner: %r", qu)

    tasked: set[int] = set()
    t_count = 0

    async def _add_task(finding_id: int, for_specialist: str, instruction: str, why: str):
        nonlocal t_count
        tid = ins("specialist_tasks", run_id=run_id, finding_id=finding_id,
                  for_specialist=for_specialist, instruction=instruction, why=why)
        row = one("SELECT * FROM specialist_tasks WHERE id=?", (tid,))
        await events.broadcast(run_id, "plan.task", serialize.specialist_task(row))
        tasked.add(finding_id)
        t_count += 1

    for t in out.get("specialist_tasks", []):
        try:
            fid = t.get("finding_id")
            if fid in valid_ids and fid not in tasked:
                await _add_task(fid, str(t.get("for_specialist", "general_medicine")),
                                str(t.get("instruction", "")), str(t.get("why", "")))
        except Exception:
            log.exception("bad task from planner: %r", t)

    # Safety net: any non-answerable finding the model dropped still becomes a task.
    for f in findings:
        if not f["patient_answerable"] and f["id"] not in tasked:
            spec = one("SELECT key FROM specialists WHERE id=?", (f["specialist_id"],)) \
                if f["specialist_id"] else None
            await _add_task(f["id"], spec["key"] if spec else "general_medicine",
                            f["title"], f["detail"])

    await events.broadcast(run_id, "plan.ready",
                           {"id": run_id, "question_count": q_count, "task_count": t_count})
