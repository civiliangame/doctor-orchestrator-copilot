"""Per-turn tick + per-session concurrency (SPEC.md § Per-turn workers).

- Urgent group (contradictions, suggestions, guardrails): LATEST-WINS.
  A new patient turn cancels the in-flight urgent task and re-fires with the
  fuller transcript.
- Accumulator group (chart, todos): NEVER cancelled, serialized per session.
  If a run is in flight when a new turn lands, the loop runs again afterwards,
  covering every turn since the last completed pass.
"""

import asyncio
import logging
from dataclasses import dataclass, field

import events

from orchestrator import workers
from orchestrator.shapes import load_ctx

log = logging.getLogger("doc.orchestrator")


@dataclass
class _SessionState:
    urgent_task: asyncio.Task | None = None
    acc_task: asyncio.Task | None = None
    acc_requested_turn: int = 0   # newest turn a pass has been requested for
    acc_done_turn: int = 0        # newest turn covered by a completed pass


_states: dict[int, _SessionState] = {}


def state_for(session_id: int) -> _SessionState:
    return _states.setdefault(session_id, _SessionState())


def drop_state(session_id: int) -> None:
    _states.pop(session_id, None)


async def on_patient_turn(session_id: int, turn_id: int) -> None:
    """Entry point called by turns.ingest_turn for every finalized patient turn."""
    try:
        await events.broadcast(session_id, "tick.started", {"turn_id": turn_id})
        ctx = load_ctx(session_id)
    except Exception:
        log.exception("tick setup failed (session=%s turn=%s)", session_id, turn_id)
        return

    st = state_for(session_id)

    # --- urgent group: latest-wins ---------------------------------------
    if st.urgent_task is not None and not st.urgent_task.done():
        st.urgent_task.cancel()
    st.urgent_task = asyncio.create_task(
        _run_urgent(ctx, turn_id), name=f"doc-urgent-s{session_id}-t{turn_id}"
    )

    # --- accumulator group: serialized, never cancelled ------------------
    st.acc_requested_turn = max(st.acc_requested_turn, turn_id)
    if st.acc_task is None or st.acc_task.done():
        st.acc_task = asyncio.create_task(
            _acc_loop(session_id), name=f"doc-acc-s{session_id}"
        )


async def _run_urgent(ctx: dict, turn_id: int) -> None:
    try:
        await asyncio.gather(
            *(workers.run_worker(ctx, name, turn_id) for name in workers.URGENT_WORKERS)
        )
    except asyncio.CancelledError:
        # run_worker logs per-worker cancellation; nothing to clean up (each
        # worker persists atomically as it completes).
        raise
    except Exception:
        log.exception("urgent group failed (session=%s turn=%s)", ctx["session"]["id"], turn_id)


async def _acc_loop(session_id: int) -> None:
    """Run chart+todos passes until every requested turn is covered. Each pass
    covers all turns since the last COMPLETED pass."""
    st = state_for(session_id)
    while st.acc_done_turn < st.acc_requested_turn:
        target = st.acc_requested_turn
        since = st.acc_done_turn
        try:
            ctx = load_ctx(session_id)
            # Continuous read: pick up external edits to the patient's markdown
            # chart file before this pass. Cheap (hash check) unless it changed.
            try:
                from orchestrator import chart_md
                await chart_md.sync_from_markdown(ctx["visit"]["id"], session_id=session_id)
            except Exception:
                log.exception("chart_md sync failed in accumulator pass (session=%s)", session_id)
            await asyncio.gather(
                *(workers.run_worker(ctx, name, target, since_turn_id=since)
                  for name in workers.ACCUMULATOR_WORKERS)
            )
        except asyncio.CancelledError:
            raise  # accumulators are never cancelled by design; be clean anyway
        except Exception:
            log.exception("accumulator pass failed (session=%s turns %s..%s)",
                          session_id, since + 1, target)
        st.acc_done_turn = target  # pass completed (or failed) for this range
