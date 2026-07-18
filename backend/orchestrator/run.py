"""The run pipeline driver: analyzing -> planning -> calling -> compiling -> done.

Fully automatic (SPEC.md decision 3). routes/core.py fires start_run() as a
background task; every stage persists and broadcasts as it happens. Any
uncaught stage failure marks the run failed (never hangs the demo).
"""

import asyncio
import logging

import events
import serialize
from db import ex, ins, now_iso, one

from orchestrator import analysis, compile as compile_mod, interview, plan, prompts

log = logging.getLogger("doc.run")


async def start_run(run_id: int) -> None:
    try:
        await _set_status(run_id, "analyzing")
        await analysis.run_analysis(run_id)

        await _set_status(run_id, "planning")
        await plan.build_plan(run_id)

        await _set_status(run_id, "calling")
        await _start_call(run_id)
        # The interview session drives itself from here; finish_run() is its
        # on_end callback.
    except Exception:
        log.exception("run %s failed", run_id)
        await _set_status(run_id, "failed", ended=True)


async def _start_call(run_id: int) -> None:
    run = one("SELECT * FROM runs WHERE id=?", (run_id,))
    transport_kind = run["transport"]
    call_id = ins("calls", run_id=run_id, transport=transport_kind,
                  status="dialing", started_ts=now_iso())
    await _broadcast_call(run_id, call_id)

    if transport_kind == "telnyx":
        # telephony.telnyx dials out; the media-stream start event flips the
        # call to active and starts the InterviewSession (task: telephony/).
        from telephony import telnyx
        await telnyx.dial(run_id, call_id, on_end=finish_run)
        return

    # sim: "answered" instantly
    ex("UPDATE calls SET status='active' WHERE id=?", (call_id,))
    await _broadcast_call(run_id, call_id)
    session = interview.InterviewSession(
        run_id, call_id, interview.SimTransport(), on_end=finish_run
    )
    await session.start()


async def finish_run(run_id: int) -> None:
    try:
        await _set_status(run_id, "compiling")
        await compile_mod.compile_intake(run_id)
        await _set_status(run_id, "done", ended=True)
    except Exception:
        log.exception("compile stage failed (run=%s)", run_id)
        await _set_status(run_id, "failed", ended=True)
    finally:
        prompts.clear_prefix(run_id)


async def _set_status(run_id: int, status: str, ended: bool = False) -> None:
    if ended:
        ex("UPDATE runs SET status=?, ended_ts=? WHERE id=?",
           (status, now_iso(), run_id))
    else:
        ex("UPDATE runs SET status=? WHERE id=?", (status, run_id))
    row = one("SELECT * FROM runs WHERE id=?", (run_id,))
    await events.broadcast(run_id, "run.status", serialize.run(row))


async def _broadcast_call(run_id: int, call_id: int) -> None:
    row = one("SELECT * FROM calls WHERE id=?", (call_id,))
    await events.broadcast(run_id, "call.status", serialize.call(row))
