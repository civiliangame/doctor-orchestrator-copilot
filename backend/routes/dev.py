"""Dev/operator endpoints: reset, sim-answer, hangup (API_CONTRACT.md § Dev).

sim-answer is THE integration seam: it feeds the same
InterviewSession.on_patient_utterance() the telnyx STT path feeds, so the
whole pipeline is buildable and testable without a phone. No auth — demo only.
"""

import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

import db
import seed
from orchestrator import interview
from routes.core import ApiError, ContractRoute

router = APIRouter(prefix="/api/dev", route_class=ContractRoute)


@router.post("/reset")
async def reset():
    interview.SESSIONS.clear()
    db.wipe_db()
    seed.seed_all()
    return {"ok": True}


class SimAnswerBody(BaseModel):
    call_id: int
    text: str


@router.post("/sim-answer")
async def sim_answer(body: SimAnswerBody):
    session = interview.SESSIONS.get(body.call_id)
    if session is None or session.ended:
        raise ApiError(409, "call_not_active", f"call {body.call_id} is not active")
    # Fire-and-forget: the reply arrives as call.turn events over the run WS.
    asyncio.create_task(session.on_patient_utterance(body.text))
    return {"ok": True}


class HangupBody(BaseModel):
    call_id: int


@router.post("/hangup")
async def hangup(body: HangupBody):
    session = interview.SESSIONS.get(body.call_id)
    if session is None:
        raise ApiError(409, "call_not_active", f"call {body.call_id} is not active")
    asyncio.create_task(session.force_end())
    return {"ok": True}
