"""Beat D: intent text -> per-node goals + numbered guardrails (draft).

One Sonnet call. Guardrail numbering follows the ORDER conditions appear in the
intent text (DEMO_SCRIPT.md cites "guardrail #1" = radiating pain). Attaching
the cardiology proposed_insert is deterministic: the model flags escalation
guardrails, and a keyword fallback catches radiating-pain/numbness/SOB wording
even if the flag is missed. The insert payload is seed.py's CARDIOLOGY_INSERT.
"""

import json
import logging
import re

from config import MODEL_SONNET
from db import ex, ins, jloads, one, q
from llm import block
from seed import CARDIOLOGY_INSERT

from orchestrator import prompts, shapes
from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.orchestrator")

_ESCALATION_RX = re.compile(
    r"\b(radiat\w*|arm|jaw|numb\w*|shortness of breath|sob)\b", re.IGNORECASE
)


def _plan_user_message(visit: dict, patient: dict, nodes: list[dict], intent_text: str) -> str:
    node_lines = "\n".join(
        f"node {n['id']} [position {n['position']}]: {n['station']} — "
        f"{n['specialist_name']} ({n['specialist_profile']})"
        for n in nodes
    )
    return f"""== PATIENT RECORD ==
{patient["summary_text"]}

== JOURNEY NODES (fixed; produce goals for each) ==
{node_lines}

== DOCTOR'S INTENT FOR THIS VISIT (extract goals + numbered guardrails from this) ==
{intent_text}"""


async def generate_plan(visit_id: int, intent_text: str) -> dict:
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    if visit is None:
        raise ValueError(f"unknown visit {visit_id}")
    patient = one("SELECT * FROM patients WHERE id=?", (visit["patient_id"],))
    nodes = q("SELECT * FROM journey_nodes WHERE visit_id=? ORDER BY position", (visit_id,))

    system = [block(prompts.PLAN_SYSTEM)]
    user = _plan_user_message(visit, patient, nodes, intent_text)
    out = await complete_json(MODEL_SONNET, system, user, max_tokens=1500)

    # --- persist goals (overwrite goals_json per node) ---------------------
    valid_ids = {n["id"] for n in nodes}
    for item in out.get("nodes") or []:
        node_id = item.get("node_id")
        goals = [g.strip() for g in (item.get("goals") or []) if isinstance(g, str) and g.strip()]
        if node_id in valid_ids and goals:
            ex("UPDATE journey_nodes SET goals_json=? WHERE id=?",
               (json.dumps(goals), node_id))

    # --- persist guardrails (DELETE + reinsert, numbered by intent order) --
    raw = [g for g in (out.get("guardrails") or [])
           if (g.get("condition_text") or "").strip() and (g.get("action_text") or "").strip()]
    raw.sort(key=lambda g: g.get("num") if isinstance(g.get("num"), int) else 999)
    ex("DELETE FROM guardrails WHERE visit_id=?", (visit_id,))
    for i, g in enumerate(raw, start=1):
        condition = g["condition_text"].strip()
        escalation = bool(g.get("cardiology_escalation")) or bool(_ESCALATION_RX.search(condition))
        ins("guardrails", visit_id=visit_id, num=i,
            condition_text=condition, action_text=g["action_text"].strip(),
            proposed_insert_json=json.dumps(CARDIOLOGY_INSERT) if escalation else None)
    log.info("generate_plan: visit=%s -> %d guardrails, goals for %d nodes",
             visit_id, len(raw), len(out.get("nodes") or []))

    ex("UPDATE visits SET intent_text=?, plan_confirmed=0 WHERE id=?",
       (intent_text, visit_id))

    guardrails = q("SELECT * FROM guardrails WHERE visit_id=? ORDER BY num", (visit_id,))
    return {
        "journey": shapes.journey_shape(visit_id),
        "guardrails": [shapes.guardrail_shape(g) for g in guardrails],
    }
