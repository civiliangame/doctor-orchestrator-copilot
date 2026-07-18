"""End-of-session compile (Fable) — SPEC.md § End-of-session compile.

One llm call producing a handoff brief per outgoing edge + todo reconciliation.
The demo must never hang on End Session: any failure still ends the session,
flips node statuses, and broadcasts compile.done with empty briefs.
"""

import asyncio
import logging
import json

import events
from config import MODEL_FABLE, MODEL_FABLE_FALLBACK
from db import ex, ins, jloads, now_iso, one, q
from llm import block, cached_block

from orchestrator import prompts, shapes, tick, workers
from orchestrator.llm_call import complete_json

log = logging.getLogger("doc.orchestrator")


def _successor_nodes(node: dict) -> list[dict]:
    rows = q(
        "SELECT n.* FROM journey_edges e JOIN journey_nodes n ON e.to_node_id=n.id"
        " WHERE e.from_node_id=? ORDER BY n.position",
        (node["id"],),
    )
    if rows:
        return rows
    # Fallback for a linear journey whose edges weren't rerouted: next by position.
    nxt = one(
        "SELECT * FROM journey_nodes WHERE visit_id=? AND position>? ORDER BY position LIMIT 1",
        (node["visit_id"], node["position"]),
    )
    return [nxt] if nxt else []


def _compile_user_message(ctx: dict, successors: list[dict]) -> str:
    sid, vid = ctx["session"]["id"], ctx["visit"]["id"]
    next_lines = "\n".join(
        f"node {n['id']}: {n['station']} — {n['specialist_name']} ({n['specialist_profile']});"
        f" goals: {', '.join(jloads(n['goals_json'], [])) or '(none)'}"
        for n in successors
    ) or "(none — end of journey)"

    turns = q("SELECT * FROM transcript_turns WHERE session_id=? ORDER BY id", (sid,))
    transcript = "\n".join(f"[{t['speaker']}] {t['text']}" for t in turns) or "(empty)"

    chart = q("SELECT * FROM chart_entries WHERE visit_id=? AND node_id=? ORDER BY id",
              (vid, ctx["node"]["id"]))
    chart_lines = "\n".join(f"[{c['category']}] {c['text']}" for c in chart) or "(none)"

    alerts = q(
        "SELECT g.num, g.condition_text, a.triggered_by, a.action FROM guardrail_alerts a"
        " JOIN guardrails g ON a.guardrail_id=g.id WHERE a.session_id=? ORDER BY a.id", (sid,))
    alert_lines = "\n".join(
        f"#{a['num']} ({a['condition_text']}): {a['triggered_by']} -> {a['action']}"
        for a in alerts) or "(none)"

    cons = q("SELECT * FROM contradictions WHERE session_id=? ORDER BY id", (sid,))
    con_lines = "\n".join(
        f"[{c['severity']}] \"{c['statement']}\" vs \"{c['conflicts_with']}\""
        for c in cons) or "(none)"

    nodes = q("SELECT * FROM journey_nodes WHERE visit_id=? ORDER BY position", (vid,))
    station_by_node = {n["id"]: n["station"] for n in nodes}
    todos = q("SELECT * FROM todos WHERE visit_id=? ORDER BY id", (vid,))
    todo_lines = "\n".join(
        f"todo-{t['id']} [{t['status']}, {t['priority']}] for node {t['for_node_id']}"
        f" ({station_by_node.get(t['for_node_id'], '?')}): {t['text']}"
        for t in todos) or "(none)"
    journey_lines = "\n".join(
        f"node {n['id']} [{n['status']}]: {n['station']} — {n['specialist_name']}"
        for n in nodes)

    return f"""== NEXT NODES (write exactly one brief per node below) ==
{next_lines}

== JOURNEY ==
{journey_lines}

== FULL SESSION TRANSCRIPT ==
{transcript}

== CHART ENTRIES RECORDED THIS SESSION ==
{chart_lines}

== GUARDRAIL ALERTS FIRED THIS SESSION ==
{alert_lines}

== CONTRADICTIONS FLAGGED THIS SESSION ==
{con_lines}

== CURRENT TODOS (reconcile these) ==
{todo_lines}"""


async def compile_session(session_id: int) -> None:
    ctx = shapes.load_ctx(session_id)
    node, visit = ctx["node"], ctx["visit"]
    ts = now_iso()
    if not ctx["session"]["ended_ts"]:
        ex("UPDATE sessions SET ended_ts=? WHERE id=?", (ts, session_id))
    await events.broadcast(session_id, "session.compile.started", {})

    successors = _successor_nodes(node)
    system = [cached_block(prompts.session_prefix(ctx)), block(prompts.COMPILE_SYSTEM)]
    user = _compile_user_message(ctx, successors)

    brief_shapes: list[dict] = []
    try:
        try:
            out = await complete_json(MODEL_FABLE, system, user, max_tokens=4000)
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("Fable compile failed, retrying once on %s", MODEL_FABLE_FALLBACK)
            out = await complete_json(MODEL_FABLE_FALLBACK, system, user, max_tokens=4000)

        # Persist briefs (one per outgoing edge / listed successor).
        valid_ids = {n["id"]: n for n in successors}
        for b in out.get("briefs") or []:
            node_id = b.get("node_id")
            if node_id not in valid_ids:
                continue
            summary = (b.get("summary_md") or "").strip()
            if not summary:
                continue
            items = [
                {"text": (i.get("text") or "").strip(),
                 "priority": i.get("priority") if i.get("priority") in ("high", "normal") else "normal"}
                for i in (b.get("action_items") or []) if (i.get("text") or "").strip()
            ]
            bid = ins("node_briefs", node_id=node_id, from_node_id=node["id"],
                      from_station=node["station"], summary_md=summary,
                      action_items_json=json.dumps(items), created_ts=now_iso())
            row = one("SELECT * FROM node_briefs WHERE id=?", (bid,))
            brief_shapes.append(shapes.brief_shape(row))

        # Apply todo reconciliation (broadcasts todo.update per op).
        await workers.apply_todo_ops(ctx, out.get("todo_ops") or [])
    except asyncio.CancelledError:
        raise
    except Exception:
        log.exception("compile_session degraded (session=%s) — ending session anyway", session_id)
        await events.broadcast(session_id, "error", {
            "code": "compile_failed",
            "message": "End-of-session compile failed; session ended without briefs.",
        })

    # Flip node statuses regardless of compile success.
    ex("UPDATE journey_nodes SET status='done' WHERE id=?", (node["id"],))
    pending = [n for n in _successor_nodes(node)
               if one("SELECT status FROM journey_nodes WHERE id=?", (n["id"],))["status"] == "pending"]
    if pending:
        nxt = min(pending, key=lambda n: n["position"])
        ex("UPDATE journey_nodes SET status='active' WHERE id=?", (nxt["id"],))

    await events.broadcast(session_id, "journey.updated", shapes.journey_shape(visit["id"]))
    todos = q("SELECT * FROM todos WHERE visit_id=? ORDER BY id", (visit["id"],))
    await events.broadcast(session_id, "session.compile.done", {
        "briefs": brief_shapes,
        "todos": [shapes.todo_shape(t) for t in todos],
    })
    await events.broadcast(session_id, "session.ended", {})

    prompts.clear_session_prefix(session_id)
    tick.drop_state(session_id)
