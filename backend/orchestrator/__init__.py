"""Orchestrator public interface — the pipeline's brain (SPEC.md § Pipeline).

Routes call exactly these:
    start_run(run_id)   — fire the full automatic pipeline as a background task
    finish_run(run_id)  — compile stage (also the interview's on_end callback)

Implementation lives in sibling modules (analysis, plan, interview, compile,
run, prompts, llm_call); imports are deferred so siblings can safely do
`from orchestrator import prompts` at import time.
"""

import logging

log = logging.getLogger("doc.orchestrator")


async def start_run(run_id: int) -> None:
    from orchestrator.run import start_run as _impl
    await _impl(run_id)


async def finish_run(run_id: int) -> None:
    from orchestrator.run import finish_run as _impl
    await _impl(run_id)
