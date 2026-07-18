"""Patient page, run start, run rehydration, run events WS (API_CONTRACT.md).

Also home of the ApiError/ContractRoute error machinery used by routes/dev.py.
Error bodies are exactly {"error": {"code", "message"}}.
"""

import asyncio
from typing import Callable, Literal

from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel

import events
import orchestrator
import serialize
from db import ins, now_iso, one, q

# ---------------------------------------------------------------------------
# Error machinery (contract: status + {"error": {code, message}})
# ---------------------------------------------------------------------------


class ApiError(Exception):
    """Raised by route handlers; rendered with the exact contract error body."""

    def __init__(self, status_code: int, code: str, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class ContractRoute(APIRoute):
    """APIRoute subclass that catches ApiError and emits the contract shape."""

    def get_route_handler(self) -> Callable:
        original = super().get_route_handler()

        async def handler(request: Request) -> Response:
            try:
                return await original(request)
            except ApiError as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"error": {"code": e.code, "message": e.message}},
                )

        return handler


router = APIRouter(route_class=ContractRoute)


# ---------------------------------------------------------------------------
# Patient page
# ---------------------------------------------------------------------------


@router.get("/api/patients/{patient_id}")
async def get_patient(patient_id: int):
    patient = one("SELECT * FROM patients WHERE id=?", (patient_id,))
    if patient is None:
        raise ApiError(404, "not_found", f"unknown patient {patient_id}")

    documents = q(
        "SELECT * FROM documents WHERE patient_id=? ORDER BY date, id", (patient_id,)
    )
    latest_run = one(
        "SELECT * FROM runs WHERE patient_id=? ORDER BY id DESC LIMIT 1", (patient_id,)
    )
    latest_intake = None
    specialist_tasks = []
    if latest_run:
        latest_intake = one(
            "SELECT * FROM intakes WHERE run_id=? ORDER BY id DESC LIMIT 1",
            (latest_run["id"],),
        )
        specialist_tasks = q(
            "SELECT * FROM specialist_tasks WHERE run_id=? ORDER BY id",
            (latest_run["id"],),
        )
    return {
        "patient": serialize.patient(patient),
        "documents": [serialize.document(d) for d in documents],
        "latest_run": serialize.run(latest_run) if latest_run else None,
        "latest_intake": serialize.intake(latest_intake) if latest_intake else None,
        "specialist_tasks": [serialize.specialist_task(t) for t in specialist_tasks],
    }


# ---------------------------------------------------------------------------
# Runs
# ---------------------------------------------------------------------------


class RunCreateBody(BaseModel):
    transport: Literal["sim", "telnyx"] = "sim"


@router.post("/api/patients/{patient_id}/runs", status_code=201)
async def create_run(patient_id: int, body: RunCreateBody):
    patient = one("SELECT * FROM patients WHERE id=?", (patient_id,))
    if patient is None:
        raise ApiError(404, "not_found", f"unknown patient {patient_id}")
    unfinished = one(
        "SELECT id FROM runs WHERE patient_id=? AND status NOT IN ('done','failed') LIMIT 1",
        (patient_id,),
    )
    if unfinished:
        raise ApiError(409, "run_in_progress",
                       f"run {unfinished['id']} is still in progress")

    run_id = ins("runs", patient_id=patient_id, status="analyzing",
                 transport=body.transport, started_ts=now_iso())
    asyncio.create_task(orchestrator.start_run(run_id))
    row = one("SELECT * FROM runs WHERE id=?", (run_id,))
    return serialize.run(row)


@router.get("/api/runs/{run_id}")
async def get_run(run_id: int):
    run = one("SELECT * FROM runs WHERE id=?", (run_id,))
    if run is None:
        raise ApiError(404, "not_found", f"unknown run {run_id}")

    call = one("SELECT * FROM calls WHERE run_id=? ORDER BY id DESC LIMIT 1", (run_id,))
    call_turns = []
    if call:
        call_turns = q("SELECT * FROM call_turns WHERE call_id=? ORDER BY id",
                       (call["id"],))
    answers = q(
        """SELECT a.* FROM answers a JOIN questions qu ON qu.id = a.question_id
           WHERE qu.run_id=? ORDER BY a.id""",
        (run_id,),
    )
    intake = one("SELECT * FROM intakes WHERE run_id=? ORDER BY id DESC LIMIT 1",
                 (run_id,))
    return {
        "run": serialize.run(run),
        "specialists": [serialize.specialist(r) for r in
                        q("SELECT * FROM specialists WHERE run_id=? ORDER BY id", (run_id,))],
        "findings": [serialize.finding(r) for r in
                     q("SELECT * FROM findings WHERE run_id=? ORDER BY id", (run_id,))],
        "questions": [serialize.question(r) for r in
                      q("SELECT * FROM questions WHERE run_id=? ORDER BY ord", (run_id,))],
        "specialist_tasks": [serialize.specialist_task(r) for r in
                             q("SELECT * FROM specialist_tasks WHERE run_id=? ORDER BY id", (run_id,))],
        "call": serialize.call(call) if call else None,
        "call_turns": [serialize.call_turn(r) for r in call_turns],
        "answers": [serialize.answer(r) for r in answers],
        "intake": serialize.intake(intake) if intake else None,
        "last_seq": events.last_seq(run_id),
    }


# ---------------------------------------------------------------------------
# Run events WebSocket
# ---------------------------------------------------------------------------


@router.websocket("/ws/runs/{run_id}/events")
async def ws_events(ws: WebSocket, run_id: int):
    await ws.accept()
    events.register(run_id, ws)
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
        events.unregister(run_id, ws)
