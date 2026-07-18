"""Orchestrator public interface — the product's brain (SPEC.md).

turns.py and the routes call exactly these three signatures:
    on_patient_turn(session_id, turn_id)  — per-turn tick, five parallel workers
    compile_session(session_id)           — end-of-session Fable compile
    generate_plan(visit_id, intent_text)  — Beat D planner

Implementation lives in sibling modules (tick, workers, prompts, compile, plan,
shapes, llm_call); this module only re-exports. Imports are deferred so sibling
modules can safely do `from orchestrator import prompts, shapes` at import time.
"""

import logging

log = logging.getLogger("doc.orchestrator")


async def on_patient_turn(session_id: int, turn_id: int) -> None:
    """Fire the five per-turn workers for this session (latest-wins for
    contradictions/suggestions/guardrails; sequential accumulation for
    chart/todos). Broadcasts results via events.broadcast()."""
    from orchestrator.tick import on_patient_turn as _impl
    await _impl(session_id, turn_id)


async def compile_session(session_id: int) -> None:
    """End-of-session Fable compile: brief per outgoing edge, todo
    reconciliation, node status flip. Broadcasts session.compile.* events."""
    from orchestrator.compile import compile_session as _impl
    await _impl(session_id)


async def generate_plan(visit_id: int, intent_text: str) -> dict:
    """Beat D: intent text → per-node goals + numbered guardrails (draft).
    Returns {journey, guardrails} per API_CONTRACT.md."""
    from orchestrator.plan import generate_plan as _impl
    return await _impl(visit_id, intent_text)
