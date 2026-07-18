"""Sessions: create/rehydrate/end, mutations, /ws/session/{id}/events (API_CONTRACT.md).

REST paths carry the /api prefix explicitly (no router prefix) because this
router also owns the events websocket, which lives at /ws/... per the contract.
"""

import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import events
import orchestrator
from db import ex, ins, now_iso, one, q
from routes.core import (
    ApiError,
    ContractRoute,
    alert,
    chart_entry,
    contradiction,
    journey,
    mutation,
    suggestion,
    todo,
    turn,
)

log = logging.getLogger("doc.api")

router = APIRouter(route_class=ContractRoute)


class SessionCreateBody(BaseModel):
    node_id: int


@router.post("/api/sessions")
async def create_session(body: SessionCreateBody):
    node = one("SELECT * FROM journey_nodes WHERE id=?", (body.node_id,))
    if node is None:
        raise ApiError(400, "bad_node", f"unknown node {body.node_id}")
    if node["status"] != "active":
        raise ApiError(
            400,
            "node_not_active",
            f"node {body.node_id} has status '{node['status']}' — sessions can only "
            "start on the 'active' journey node",
        )
    session_id = ins("sessions", node_id=body.node_id, started_ts=now_iso())
    # Visit-start read: fold the patient's markdown chart file into the PCM.
    # First session on a dataset patient runs the LLM extraction here; after
    # that it is a cheap hash check (and re-ingests only if the file changed).
    try:
        from orchestrator import chart_md
        await chart_md.sync_from_markdown(node["visit_id"], session_id=session_id)
    except Exception:
        log.exception("chart_md sync failed at session start (node=%s)", body.node_id)
    return {
        "session_id": session_id,
        "events_url": f"ws://localhost:8000/ws/session/{session_id}/events",
        "audio_url": f"ws://localhost:8000/ws/audio?session_id={session_id}",
    }


@router.get("/api/sessions/{session_id}")
async def get_session(session_id: int):
    session = one("SELECT * FROM sessions WHERE id=?", (session_id,))
    if session is None:
        raise ApiError(404, "not_found", f"unknown session {session_id}")
    node = one("SELECT * FROM journey_nodes WHERE id=?", (session["node_id"],))

    turns = q(
        "SELECT * FROM transcript_turns WHERE session_id=? ORDER BY id", (session_id,)
    )
    suggestions = q(
        "SELECT * FROM suggestions WHERE session_id=? ORDER BY id", (session_id,)
    )
    alerts = q(
        """SELECT a.*, g.num AS guardrail_num, g.condition_text AS condition_text
           FROM guardrail_alerts a JOIN guardrails g ON g.id = a.guardrail_id
           WHERE a.session_id=? ORDER BY a.id""",
        (session_id,),
    )
    contradictions = q(
        "SELECT * FROM contradictions WHERE session_id=? ORDER BY id", (session_id,)
    )
    chart_rows = q(
        """SELECT c.*, n.station AS node_station
           FROM chart_entries c JOIN journey_nodes n ON n.id = c.node_id
           WHERE c.node_id=? AND c.ts >= ? ORDER BY c.id""",
        (session["node_id"], session["started_ts"]),
    )
    todos = q(
        "SELECT * FROM todos WHERE visit_id=? ORDER BY id", (node["visit_id"],)
    ) if node else []
    pending = one(
        "SELECT * FROM journey_mutations WHERE session_id=? AND status='proposed' "
        "ORDER BY id DESC LIMIT 1",
        (session_id,),
    )
    return {
        "session": {
            "id": session["id"],
            "node_id": session["node_id"],
            "started_ts": session["started_ts"],
            "ended_ts": session["ended_ts"],
        },
        "turns": [turn(r) for r in turns],
        "suggestions": [suggestion(r) for r in suggestions],
        "alerts": [alert(r) for r in alerts],
        "contradictions": [contradiction(r) for r in contradictions],
        "chart_entries": [chart_entry(r) for r in chart_rows],
        "todos": [todo(r) for r in todos],
        "pending_mutation": mutation(pending) if pending else None,
        "last_seq": events.last_seq(session_id),
    }


@router.post("/api/sessions/{session_id}/end")
async def end_session(session_id: int):
    session = one("SELECT * FROM sessions WHERE id=?", (session_id,))
    if session is None:
        raise ApiError(404, "not_found", f"unknown session {session_id}")
    if session["ended_ts"]:
        raise ApiError(409, "already_ended", f"session {session_id} already ended")
    # compile_session owns ended_ts, node status flips, and all compile events.
    asyncio.create_task(orchestrator.compile_session(session_id))
    return JSONResponse(status_code=202, content={"compiling": True})


def _get_mutation(mutation_id: int) -> dict:
    row = one("SELECT * FROM journey_mutations WHERE id=?", (mutation_id,))
    if row is None:
        raise ApiError(404, "not_found", f"unknown mutation {mutation_id}")
    return row


@router.post("/api/mutations/{mutation_id}/accept")
async def accept_mutation(mutation_id: int):
    mut = _get_mutation(mutation_id)
    if mut["status"] != "proposed":
        raise ApiError(
            409, "not_proposed", f"mutation {mutation_id} is '{mut['status']}', not 'proposed'"
        )
    before = one("SELECT * FROM journey_nodes WHERE id=?", (mut["before_node_id"],))
    if before is None:
        raise ApiError(409, "bad_mutation", f"before_node {mut['before_node_id']} not found")
    visit_id = before["visit_id"]
    pos = before["position"]

    # Shift before_node and everything after it right, insert the new node at pos.
    ex(
        "UPDATE journey_nodes SET position = position + 1 WHERE visit_id=? AND position >= ?",
        (visit_id, pos),
    )
    new_id = ins(
        "journey_nodes",
        visit_id=visit_id,
        station=mut["insert_station"],
        specialist_name=mut["insert_specialist_name"],
        specialist_profile=mut["insert_specialist_profile"],
        goals_json="[]",
        status="pending",
        position=pos,
        sched_time="",
    )

    # Rewire edges: X -> before becomes X -> new -> before.
    incoming = one(
        "SELECT * FROM journey_edges WHERE visit_id=? AND to_node_id=?",
        (visit_id, before["id"]),
    )
    if incoming:
        ex("UPDATE journey_edges SET to_node_id=? WHERE id=?", (new_id, incoming["id"]))
    ins("journey_edges", visit_id=visit_id, from_node_id=new_id, to_node_id=before["id"])

    ex("UPDATE journey_mutations SET status='accepted' WHERE id=?", (mutation_id,))
    fresh_journey = journey(visit_id)
    await events.broadcast(mut["session_id"], "journey.updated", fresh_journey)
    return {"mutation": mutation(_get_mutation(mutation_id)), "journey": fresh_journey}


@router.post("/api/mutations/{mutation_id}/dismiss")
async def dismiss_mutation(mutation_id: int):
    mut = _get_mutation(mutation_id)
    if mut["status"] != "proposed":
        raise ApiError(
            409, "not_proposed", f"mutation {mutation_id} is '{mut['status']}', not 'proposed'"
        )
    ex("UPDATE journey_mutations SET status='dismissed' WHERE id=?", (mutation_id,))
    before = one("SELECT * FROM journey_nodes WHERE id=?", (mut["before_node_id"],))
    visit_id = before["visit_id"] if before else 0
    return {"mutation": mutation(_get_mutation(mutation_id)), "journey": journey(visit_id)}


@router.websocket("/ws/session/{session_id}/events")
async def ws_events(ws: WebSocket, session_id: int):
    await ws.accept()
    events.register(session_id, ws)
    try:
        while True:
            # All frames are pushed by events.broadcast(); inbound content is
            # ignored — this loop only exists to detect disconnect.
            msg = await ws.receive()
            if msg.get("type") == "websocket.disconnect":
                break
    except WebSocketDisconnect:
        pass
    finally:
        events.unregister(session_id, ws)
