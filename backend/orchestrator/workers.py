"""The five per-turn workers: model call -> persist -> broadcast, per worker.

Each worker persists and broadcasts as soon as ITS call returns — urgent cards
are never blocked behind the accumulators (SPEC.md § Turn pipeline).
"""

import asyncio
import json
import logging
import re
import time

import events
from config import MAX_SUGGESTIONS_PER_TURN, MODEL_HAIKU, MODEL_SONNET
from db import ex, ins, jloads, now_iso, one, q
from llm import block, cached_block

from orchestrator import prompts, shapes
from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.orchestrator")

# name -> (model, max_tokens). Sonnet for judgment calls, Haiku for mechanical ones.
WORKER_SPECS: dict[str, tuple[str, int]] = {
    "contradictions": (MODEL_SONNET, 768),
    "suggestions": (MODEL_SONNET, 768),
    "guardrails": (MODEL_HAIKU, 512),
    "chart": (MODEL_HAIKU, 512),
    "todos": (MODEL_HAIKU, 512),
}

URGENT_WORKERS = ("contradictions", "suggestions", "guardrails")
ACCUMULATOR_WORKERS = ("chart", "todos")

# In-memory latency samples: (session_id, turn_id, worker, ms). For the 3s-budget check.
latency_samples: list[tuple[int, int, str, int]] = []


async def run_worker(
    ctx: dict, name: str, turn_id: int, since_turn_id: int | None = None
) -> None:
    """One worker for one tick: call the model, persist + broadcast the output.
    Swallows its own non-cancellation errors so siblings keep running."""
    model, max_tokens = WORKER_SPECS[name]
    mode = "accumulator" if name in ACCUMULATOR_WORKERS else "urgent"
    system = [
        cached_block(prompts.session_prefix(ctx)),  # identical across all 5 workers
        block(prompts.WORKER_SYSTEM[name]),
    ]
    user = prompts.dynamic_message(ctx, turn_id, mode, since_turn_id)

    t0 = time.perf_counter()
    try:
        out = await complete_json(model, system, user, max_tokens=max_tokens)
    except asyncio.CancelledError:
        log.info("worker %s cancelled (session=%s turn=%s) — latest-wins",
                 name, ctx["session"]["id"], turn_id)
        raise
    except Exception:
        log.exception("worker %s failed (session=%s turn=%s)", name, ctx["session"]["id"], turn_id)
        return
    ms = int((time.perf_counter() - t0) * 1000)
    latency_samples.append((ctx["session"]["id"], turn_id, name, ms))
    log.info("worker %-14s %5d ms (session=%s turn=%s model=%s)",
             name, ms, ctx["session"]["id"], turn_id, model)

    try:
        await _HANDLERS[name](ctx, out)
    except asyncio.CancelledError:
        raise
    except Exception:
        log.exception("worker %s persist/broadcast failed (session=%s)", name, ctx["session"]["id"])


# ---------------------------------------------------------------- handlers

async def _handle_contradictions(ctx: dict, out: dict) -> None:
    sid = ctx["session"]["id"]
    for item in out.get("contradictions") or []:
        statement = (item.get("statement") or "").strip()
        conflicts = (item.get("conflicts_with") or "").strip()
        if not statement or not conflicts:
            continue
        if one("SELECT id FROM contradictions WHERE session_id=? AND statement=?",
               (sid, statement)):
            continue  # exact duplicate of an already-shown card
        ts = now_iso()
        severity = item.get("severity") if item.get("severity") in ("high", "note") else "note"
        rid = ins("contradictions", session_id=sid, statement=statement,
                  conflicts_with=conflicts, severity=severity,
                  suggested_probe=item.get("suggested_probe") or "", ts=ts)
        row = one("SELECT * FROM contradictions WHERE id=?", (rid,))
        await events.broadcast(sid, "contradiction", shapes.contradiction_shape(row))


async def _handle_suggestions(ctx: dict, out: dict) -> None:
    sid = ctx["session"]["id"]
    emitted = 0
    for item in out.get("suggestions") or []:
        if emitted >= MAX_SUGGESTIONS_PER_TURN:
            break
        text = (item.get("text") or "").strip()
        if not text:
            continue
        if one("SELECT id FROM suggestions WHERE session_id=? AND text=?", (sid, text)):
            continue  # exact duplicate of an already-shown suggestion
        kind = item.get("kind") if item.get("kind") in ("question", "action", "observation") else "question"
        priority = item.get("priority") if item.get("priority") in ("high", "normal") else "normal"
        rid = ins("suggestions", session_id=sid, kind=kind, text=text,
                  reason=item.get("reason") or "", priority=priority, ts=now_iso())
        row = one("SELECT * FROM suggestions WHERE id=?", (rid,))
        await events.broadcast(sid, "suggestion", shapes.suggestion_shape(row))
        emitted += 1


async def _handle_guardrails(ctx: dict, out: dict) -> None:
    sid, vid = ctx["session"]["id"], ctx["visit"]["id"]
    for item in out.get("guardrail_alerts") or []:
        num = item.get("guardrail_id", item.get("num"))
        try:
            num = int(num)
        except (TypeError, ValueError):
            continue
        grow = one("SELECT * FROM guardrails WHERE visit_id=? AND num=?", (vid, num))
        if grow is None:
            log.warning("guardrail worker cited unknown guardrail #%s", num)
            continue
        # ONE alert per guardrail num per session.
        if one("SELECT a.id FROM guardrail_alerts a JOIN guardrails g ON a.guardrail_id=g.id"
               " WHERE a.session_id=? AND g.num=?", (sid, num)):
            continue
        triggered_by = (item.get("triggered_by") or "").strip()
        action = (item.get("action") or grow["action_text"]).strip()
        rid = ins("guardrail_alerts", session_id=sid, guardrail_id=grow["id"],
                  triggered_by=triggered_by, action=action, ts=now_iso())
        row = one("SELECT * FROM guardrail_alerts WHERE id=?", (rid,))
        await events.broadcast(sid, "guardrail.alert", shapes.alert_shape(row, grow))
        # Deterministic post-processing: propose the journey mutation (not a model).
        await maybe_propose_mutation(ctx, grow)


async def maybe_propose_mutation(ctx: dict, guardrail_row: dict) -> None:
    """If the fired guardrail carries a proposed_insert, and the journey doesn't
    already contain that station, and there is no live (non-dismissed) proposal
    for this visit+station: insert a journey_mutations row and broadcast it."""
    insert = jloads(guardrail_row.get("proposed_insert_json"), None)
    if not insert:
        return
    sid, vid = ctx["session"]["id"], ctx["visit"]["id"]
    station = insert.get("station")
    before_station = insert.get("before_station")
    if not station or not before_station:
        return
    if one("SELECT id FROM journey_nodes WHERE visit_id=? AND station=?", (vid, station)):
        return  # station already in the journey (e.g. mutation already accepted)
    if one(
        "SELECT m.id FROM journey_mutations m JOIN sessions s ON m.session_id=s.id"
        " JOIN journey_nodes n ON s.node_id=n.id"
        " WHERE n.visit_id=? AND m.insert_station=? AND m.status!='dismissed'",
        (vid, station),
    ):
        return  # a live proposal for this visit+station already exists
    before = one("SELECT * FROM journey_nodes WHERE visit_id=? AND station=?",
                 (vid, before_station))
    if before is None:
        log.warning("proposed_insert before_station %r not in journey", before_station)
        return
    description = (
        f"Insert {station.capitalize()} consult ({insert.get('specialist_name', '')})"
        f" before {before['station'].capitalize()}"
    )
    mid = ins("journey_mutations", session_id=sid, guardrail_id=guardrail_row["id"],
              description=description, insert_station=station,
              insert_specialist_name=insert.get("specialist_name", ""),
              insert_specialist_profile=insert.get("specialist_profile", ""),
              before_node_id=before["id"], status="proposed", ts=now_iso())
    row = one("SELECT * FROM journey_mutations WHERE id=?", (mid,))
    await events.broadcast(sid, "journey.mutation_proposed", shapes.mutation_shape(row))


_CATEGORIES = ("symptom", "vital", "finding", "note", "contradiction")


async def _handle_chart(ctx: dict, out: dict) -> None:
    sid, vid, node = ctx["session"]["id"], ctx["visit"]["id"], ctx["node"]
    for item in out.get("chart_updates") or []:
        text = (item.get("text") or "").strip()
        if not text:
            continue
        if one("SELECT id FROM chart_entries WHERE visit_id=? AND text=?", (vid, text)):
            continue
        category = item.get("category") if item.get("category") in _CATEGORIES else "note"
        rid = ins("chart_entries", visit_id=vid, node_id=node["id"], ts=now_iso(),
                  category=category, text=text)
        row = one("SELECT * FROM chart_entries WHERE id=?", (rid,))
        await events.broadcast(sid, "chart.entry",
                               shapes.chart_entry_shape(row, node["station"]))


_TODO_ID = re.compile(r"(\d+)")


def _parse_todo_id(raw) -> int | None:
    if isinstance(raw, int):
        return raw
    m = _TODO_ID.search(str(raw or ""))
    return int(m.group(1)) if m else None


async def apply_todo_ops(ctx: dict, ops: list[dict]) -> None:
    """Shared by the todos worker and the end-of-session compiler."""
    sid, vid, node = ctx["session"]["id"], ctx["visit"]["id"], ctx["node"]
    valid_nodes = {n["id"] for n in q("SELECT id FROM journey_nodes WHERE visit_id=?", (vid,))}
    for item in ops or []:
        op = item.get("op")
        if op == "add":
            text = (item.get("text") or "").strip()
            if not text:
                continue
            if one("SELECT id FROM todos WHERE visit_id=? AND text=? AND status='open'",
                   (vid, text)):
                continue
            for_node = item.get("for_node_id")
            if for_node not in valid_nodes:
                for_node = node["id"]
            priority = item.get("priority") if item.get("priority") in ("high", "normal") else "normal"
            tid = ins("todos", visit_id=vid, created_by_node_id=node["id"],
                      for_node_id=for_node, text=text, priority=priority, status="open")
            row = one("SELECT * FROM todos WHERE id=?", (tid,))
            await events.broadcast(sid, "todo.update",
                                   {"op": "add", "todo": shapes.todo_shape(row)})
        elif op in ("complete", "edit"):
            tid = _parse_todo_id(item.get("id"))
            if tid is None:
                continue
            row = one("SELECT * FROM todos WHERE id=? AND visit_id=?", (tid, vid))
            if row is None:
                continue
            if op == "complete":
                if row["status"] == "done":
                    continue
                ex("UPDATE todos SET status='done' WHERE id=?", (tid,))
            else:
                new_text = (item.get("text") or "").strip() or row["text"]
                new_priority = item.get("priority") if item.get("priority") in ("high", "normal") else row["priority"]
                if new_text == row["text"] and new_priority == row["priority"]:
                    continue
                ex("UPDATE todos SET text=?, priority=? WHERE id=?", (new_text, new_priority, tid))
            row = one("SELECT * FROM todos WHERE id=?", (tid,))
            await events.broadcast(sid, "todo.update",
                                   {"op": op, "todo": shapes.todo_shape(row)})


async def _handle_todos(ctx: dict, out: dict) -> None:
    await apply_todo_ops(ctx, out.get("todo_updates") or [])


_HANDLERS = {
    "contradictions": _handle_contradictions,
    "suggestions": _handle_suggestions,
    "guardrails": _handle_guardrails,
    "chart": _handle_chart,
    "todos": _handle_todos,
}
