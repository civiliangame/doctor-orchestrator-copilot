"""Appointments, patient page, Beat D plan endpoints (API_CONTRACT.md).

Also home of the shared row -> contract-shape serializers and the
ApiError/ContractRoute error machinery used by routes/sessions.py and
routes/dev.py. Error bodies are exactly {"error": {"code", "message"}}.
"""

import json
from typing import Callable

from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel

import orchestrator
from db import ex, jloads, one, q

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


# ---------------------------------------------------------------------------
# Shared serializers: DB row -> API_CONTRACT.md shape
# ---------------------------------------------------------------------------


def journey(visit_id: int) -> dict:
    nodes = [
        {
            "id": r["id"],
            "visit_id": r["visit_id"],
            "station": r["station"],
            "specialist_name": r["specialist_name"],
            "specialist_profile": r["specialist_profile"],
            "goals": jloads(r["goals_json"]),
            "status": r["status"],
            "position": r["position"],
        }
        for r in q(
            "SELECT * FROM journey_nodes WHERE visit_id=? ORDER BY position", (visit_id,)
        )
    ]
    edges = [
        {"id": r["id"], "from_node_id": r["from_node_id"], "to_node_id": r["to_node_id"]}
        for r in q("SELECT * FROM journey_edges WHERE visit_id=? ORDER BY id", (visit_id,))
    ]
    return {"nodes": nodes, "edges": edges}


def guardrail(r: dict) -> dict:
    return {
        "id": r["id"],
        "num": r["num"],
        "condition_text": r["condition_text"],
        "action_text": r["action_text"],
    }


def brief(r: dict) -> dict:
    return {
        "id": r["id"],
        "node_id": r["node_id"],
        "from_node_id": r["from_node_id"],
        "from_station": r["from_station"],
        "summary_md": r["summary_md"],
        "action_items": jloads(r["action_items_json"]),
        "created_ts": r["created_ts"],
    }


def todo(r: dict) -> dict:
    return {
        "id": r["id"],
        "visit_id": r["visit_id"],
        "created_by_node_id": r["created_by_node_id"],
        "for_node_id": r["for_node_id"],
        "text": r["text"],
        "priority": r["priority"],
        "status": r["status"],
    }


def chart_entry(r: dict) -> dict:
    """Expects the row joined with journey_nodes.station AS node_station."""
    return {
        "id": r["id"],
        "visit_id": r["visit_id"],
        "node_id": r["node_id"],
        "node_station": r["node_station"],
        "category": r["category"],
        "text": r["text"],
        "ts": r["ts"],
    }


def suggestion(r: dict) -> dict:
    return {
        "id": r["id"],
        "session_id": r["session_id"],
        "kind": r["kind"],
        "text": r["text"],
        "reason": r["reason"],
        "priority": r["priority"],
        "ts": r["ts"],
    }


def alert(r: dict) -> dict:
    """Expects the row joined with guardrails.num AS guardrail_num and
    guardrails.condition_text AS condition_text (denormalized per contract)."""
    return {
        "id": r["id"],
        "session_id": r["session_id"],
        "guardrail_id": r["guardrail_id"],
        "guardrail_num": r["guardrail_num"],
        "condition_text": r["condition_text"],
        "triggered_by": r["triggered_by"],
        "action": r["action"],
        "ts": r["ts"],
    }


def contradiction(r: dict) -> dict:
    return {
        "id": r["id"],
        "session_id": r["session_id"],
        "statement": r["statement"],
        "conflicts_with": r["conflicts_with"],
        "severity": r["severity"],
        "suggested_probe": r["suggested_probe"],
        "ts": r["ts"],
    }


def mutation(r: dict) -> dict:
    return {
        "id": r["id"],
        "session_id": r["session_id"],
        "guardrail_id": r["guardrail_id"],
        "description": r["description"],
        "insert_station": r["insert_station"],
        "before_node_id": r["before_node_id"],
        "status": r["status"],
        "ts": r["ts"],
    }


def turn(r: dict) -> dict:
    return {
        "id": r["id"],
        "session_id": r["session_id"],
        "speaker": r["speaker"],
        "text": r["text"],
        "ts": r["ts"],
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/api", route_class=ContractRoute)


@router.get("/appointments")
async def get_appointments(station: str):
    rows = q(
        """SELECT n.id AS node_id, v.patient_id AS patient_id, p.name AS patient_name,
                  n.sched_time AS time, n.station AS station, n.status AS status
           FROM journey_nodes n
           JOIN visits v ON v.id = n.visit_id
           JOIN patients p ON p.id = v.patient_id
           WHERE n.station=?
           ORDER BY n.sched_time, n.id""",
        (station,),
    )
    return {"appointments": rows}


@router.get("/patients/{patient_id}")
async def get_patient(patient_id: int, node_id: int):
    patient = one("SELECT * FROM patients WHERE id=?", (patient_id,))
    if patient is None:
        raise ApiError(404, "not_found", f"unknown patient {patient_id}")
    visit = one(
        "SELECT * FROM visits WHERE patient_id=? ORDER BY id DESC LIMIT 1", (patient_id,)
    )
    if visit is None:
        raise ApiError(404, "not_found", f"no visit for patient {patient_id}")

    briefs = q(
        "SELECT * FROM node_briefs WHERE node_id=? ORDER BY created_ts, id", (node_id,)
    )
    todos = q(
        "SELECT * FROM todos WHERE visit_id=? AND for_node_id=? AND status='open' ORDER BY id",
        (visit["id"], node_id),
    )
    chart = q(
        """SELECT c.*, n.station AS node_station
           FROM chart_entries c JOIN journey_nodes n ON n.id = c.node_id
           WHERE c.visit_id=? ORDER BY c.id""",
        (visit["id"],),
    )
    active = one(
        "SELECT id FROM sessions WHERE node_id=? AND ended_ts IS NULL ORDER BY id DESC LIMIT 1",
        (node_id,),
    )
    return {
        "patient": {
            "id": patient["id"],
            "name": patient["name"],
            "dob": patient["dob"],
            "summary_text": patient["summary_text"],
        },
        "visit": {
            "id": visit["id"],
            "patient_id": visit["patient_id"],
            "date": visit["date"],
            "intent_text": visit["intent_text"],
            "plan_confirmed": bool(visit["plan_confirmed"]),
        },
        "journey": journey(visit["id"]),
        "guardrails": [
            guardrail(r)
            for r in q("SELECT * FROM guardrails WHERE visit_id=? ORDER BY num", (visit["id"],))
        ],
        "briefs": [brief(r) for r in briefs],
        "todos": [todo(r) for r in todos],
        "chart": [chart_entry(r) for r in chart],
        "active_session_id": active["id"] if active else None,
    }


class PlanGenerateBody(BaseModel):
    intent_text: str


@router.post("/visits/{visit_id}/plan/generate")
async def plan_generate(visit_id: int, body: PlanGenerateBody):
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    if visit is None:
        raise ApiError(404, "not_found", f"unknown visit {visit_id}")
    ex("UPDATE visits SET intent_text=? WHERE id=?", (body.intent_text, visit_id))
    try:
        return await orchestrator.generate_plan(visit_id, body.intent_text)
    except NotImplementedError:
        raise ApiError(
            501, "not_implemented", "orchestrator.generate_plan is not implemented yet"
        )


class PlanNodeBody(BaseModel):
    id: int
    goals: list[str]


class PlanGuardrailBody(BaseModel):
    id: int
    condition_text: str
    action_text: str


class PlanConfirmBody(BaseModel):
    nodes: list[PlanNodeBody]
    guardrails: list[PlanGuardrailBody]


@router.post("/visits/{visit_id}/plan/confirm")
async def plan_confirm(visit_id: int, body: PlanConfirmBody):
    visit = one("SELECT * FROM visits WHERE id=?", (visit_id,))
    if visit is None:
        raise ApiError(404, "not_found", f"unknown visit {visit_id}")
    for n in body.nodes:
        ex(
            "UPDATE journey_nodes SET goals_json=? WHERE id=? AND visit_id=?",
            (json.dumps(n.goals), n.id, visit_id),
        )
    for g in body.guardrails:
        ex(
            "UPDATE guardrails SET condition_text=?, action_text=? WHERE id=? AND visit_id=?",
            (g.condition_text, g.action_text, g.id, visit_id),
        )
    ex("UPDATE visits SET plan_confirmed=1 WHERE id=?", (visit_id,))
    return {
        "journey": journey(visit_id),
        "guardrails": [
            guardrail(r)
            for r in q("SELECT * FROM guardrails WHERE visit_id=? ORDER BY num", (visit_id,))
        ],
    }
