"""Stage 1-2: triage picks the specialist panel, specialists find issues.

Specialists run in parallel and each persists + broadcasts as it returns.
The plan stage needs ALL findings, so the gather barrier here is inherent;
stragglers are cut off at SPECIALIST_TIMEOUT_S (SPEC.md § Latency budgets).
"""

import asyncio
import json
import logging

import events
import serialize
from config import MODEL_SONNET, SPECIALIST_TIMEOUT_S
from db import ex, ins, one
from llm import block, cached_block

from orchestrator import prompts
from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.analysis")

VALID_KINDS = ("contradiction", "gap", "ambiguity")


async def run_analysis(run_id: int) -> None:
    """Triage -> parallel specialists. Persists + broadcasts everything."""
    prefix = cached_block(prompts.corpus_prefix(run_id))

    out = await complete_json(
        MODEL_SONNET,
        [prefix, block(prompts.TRIAGE_SYSTEM)],
        prompts.TRIAGE_USER,
        max_tokens=512,
    )
    picks = out.get("specialists", [])[:4]
    if not picks:  # triage must never leave the demo empty-handed
        picks = [{"key": "general_medicine", "display_name": "General Medicine",
                  "rationale": "default reviewer"}]

    rows = []
    for p in picks:
        sid = ins(
            "specialists", run_id=run_id,
            key=str(p.get("key", "general_medicine")),
            display_name=str(p.get("display_name", p.get("key", "Specialist"))),
            rationale=str(p.get("rationale", "")),
            status="running",
        )
        row = one("SELECT * FROM specialists WHERE id=?", (sid,))
        rows.append(row)
        await events.broadcast(run_id, "specialist.selected", serialize.specialist(row))

    await asyncio.gather(*(_run_specialist(run_id, prefix, r) for r in rows))


async def _run_specialist(run_id: int, prefix: dict, spec: dict) -> None:
    try:
        out = await asyncio.wait_for(
            complete_json(
                MODEL_SONNET,
                [prefix, block(prompts.specialist_system(spec["display_name"], spec["rationale"]))],
                prompts.SPECIALIST_USER,
                max_tokens=2000,
            ),
            timeout=SPECIALIST_TIMEOUT_S,
        )
        findings = out.get("findings", [])
    except asyncio.TimeoutError:
        log.warning("specialist %s timed out after %ss — skipped",
                    spec["key"], SPECIALIST_TIMEOUT_S)
        findings = []
    except Exception:
        log.exception("specialist %s failed", spec["key"])
        findings = []

    for f in findings:
        try:
            kind = f["kind"] if f.get("kind") in VALID_KINDS else "ambiguity"
            fid = ins(
                "findings", run_id=run_id, specialist_id=spec["id"], kind=kind,
                severity="high" if f.get("severity") == "high" else "normal",
                title=str(f.get("title", ""))[:200],
                detail=str(f.get("detail", "")),
                quotes_json=json.dumps(f.get("quotes", [])),
                patient_answerable=1 if f.get("patient_answerable", True) else 0,
            )
            row = one("SELECT * FROM findings WHERE id=?", (fid,))
            await events.broadcast(run_id, "finding.created", serialize.finding(row))
        except Exception:
            log.exception("bad finding from %s: %r", spec["key"], f)

    ex("UPDATE specialists SET status='done' WHERE id=?", (spec["id"],))
    row = one("SELECT * FROM specialists WHERE id=?", (spec["id"],))
    await events.broadcast(run_id, "specialist.done", serialize.specialist(row))
