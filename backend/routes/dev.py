"""Dev/operator endpoints: inject-turn, end-patient-turn, node complete, reset.

No auth — used off-screen during the demo (API_CONTRACT.md § Dev controls).
"""

import inspect
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

import db
import events
import seed
import turns
from db import ex, one, q
from routes.core import ApiError, ContractRoute, journey

router = APIRouter(prefix="/api/dev", route_class=ContractRoute)


class InjectTurnBody(BaseModel):
    session_id: int
    speaker: Literal["staff", "patient"]
    text: str


@router.post("/inject-turn")
async def inject_turn(body: InjectTurnBody):
    try:
        return await turns.ingest_turn(body.session_id, body.speaker, body.text)
    except ValueError as e:
        msg = str(e)
        if "unknown" in msg:
            raise ApiError(404, "not_found", msg)
        raise ApiError(409, "session_ended", msg)


class EndPatientTurnBody(BaseModel):
    session_id: int


@router.post("/end-patient-turn")
async def end_patient_turn(body: EndPatientTurnBody):
    try:
        from voice import force_end_patient_turn
    except ImportError:
        raise ApiError(
            501, "not_implemented", "voice.force_end_patient_turn is not available yet"
        )
    result = force_end_patient_turn(body.session_id)
    if inspect.isawaitable(result):
        result = await result
    return {"flushed": bool(result)}


@router.post("/nodes/{node_id}/complete")
async def complete_node(node_id: int):
    node = one("SELECT * FROM journey_nodes WHERE id=?", (node_id,))
    if node is None:
        raise ApiError(404, "not_found", f"unknown node {node_id}")
    visit_id = node["visit_id"]
    ex("UPDATE journey_nodes SET status='done' WHERE id=?", (node_id,))
    nxt = one(
        "SELECT * FROM journey_nodes WHERE visit_id=? AND status='pending' "
        "ORDER BY position LIMIT 1",
        (visit_id,),
    )
    if nxt:
        ex("UPDATE journey_nodes SET status='active' WHERE id=?", (nxt["id"],))

    fresh_journey = journey(visit_id)
    # Broadcast to every session of this visit (no-listener sessions are harmless).
    session_rows = q(
        """SELECT s.id FROM sessions s
           JOIN journey_nodes n ON n.id = s.node_id
           WHERE n.visit_id=?""",
        (visit_id,),
    )
    for s in session_rows:
        await events.broadcast(s["id"], "journey.updated", fresh_journey)
    return fresh_journey


@router.post("/reset")
async def reset():
    db.wipe_db()
    seed.seed_all()
    return {"ok": True}
