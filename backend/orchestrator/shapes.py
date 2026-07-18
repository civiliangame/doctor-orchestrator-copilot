"""Row -> API_CONTRACT.md shape helpers + session context loading.

The routes package has its own serializers; we deliberately do not import from
routes (duplication is fine at hackathon scale, per SPEC).
"""

from db import jloads, one, q


def load_ctx(session_id: int) -> dict:
    """session + its node + visit + patient rows, as one dict."""
    session = one("SELECT * FROM sessions WHERE id=?", (session_id,))
    if session is None:
        raise ValueError(f"unknown session {session_id}")
    node = one("SELECT * FROM journey_nodes WHERE id=?", (session["node_id"],))
    if node is None:
        raise ValueError(f"session {session_id} has unknown node {session['node_id']}")
    visit = one("SELECT * FROM visits WHERE id=?", (node["visit_id"],))
    patient = one("SELECT * FROM patients WHERE id=?", (visit["patient_id"],))
    return {"session": session, "node": node, "visit": visit, "patient": patient}


# ---------------------------------------------------------------- shapes

def node_shape(row: dict) -> dict:
    return {
        "id": row["id"],
        "visit_id": row["visit_id"],
        "station": row["station"],
        "specialist_name": row["specialist_name"],
        "specialist_profile": row["specialist_profile"],
        "goals": jloads(row["goals_json"], []),
        "status": row["status"],
        "position": row["position"],
    }


def journey_shape(visit_id: int) -> dict:
    nodes = q(
        "SELECT * FROM journey_nodes WHERE visit_id=? ORDER BY position", (visit_id,)
    )
    edges = q("SELECT * FROM journey_edges WHERE visit_id=?", (visit_id,))
    return {
        "nodes": [node_shape(n) for n in nodes],
        "edges": [
            {"id": e["id"], "from_node_id": e["from_node_id"], "to_node_id": e["to_node_id"]}
            for e in edges
        ],
    }


def guardrail_shape(row: dict) -> dict:
    return {
        "id": row["id"],
        "num": row["num"],
        "condition_text": row["condition_text"],
        "action_text": row["action_text"],
    }


def suggestion_shape(row: dict) -> dict:
    return {
        "id": row["id"],
        "session_id": row["session_id"],
        "kind": row["kind"],
        "text": row["text"],
        "reason": row["reason"],
        "priority": row["priority"],
        "ts": row["ts"],
    }


def alert_shape(row: dict, guardrail: dict) -> dict:
    """GuardrailAlert shape — denormalized with guardrail num + condition."""
    return {
        "id": row["id"],
        "session_id": row["session_id"],
        "guardrail_id": row["guardrail_id"],
        "guardrail_num": guardrail["num"],
        "condition_text": guardrail["condition_text"],
        "triggered_by": row["triggered_by"],
        "action": row["action"],
        "ts": row["ts"],
    }


def contradiction_shape(row: dict) -> dict:
    return {
        "id": row["id"],
        "session_id": row["session_id"],
        "statement": row["statement"],
        "conflicts_with": row["conflicts_with"],
        "severity": row["severity"],
        "suggested_probe": row["suggested_probe"],
        "ts": row["ts"],
    }


def chart_entry_shape(row: dict, node_station: str) -> dict:
    return {
        "id": row["id"],
        "visit_id": row["visit_id"],
        "node_id": row["node_id"],
        "node_station": node_station,
        "category": row["category"],
        "text": row["text"],
        "ts": row["ts"],
    }


def todo_shape(row: dict) -> dict:
    return {
        "id": row["id"],
        "visit_id": row["visit_id"],
        "created_by_node_id": row["created_by_node_id"],
        "for_node_id": row["for_node_id"],
        "text": row["text"],
        "priority": row["priority"],
        "status": row["status"],
    }


def mutation_shape(row: dict) -> dict:
    return {
        "id": row["id"],
        "session_id": row["session_id"],
        "guardrail_id": row["guardrail_id"],
        "description": row["description"],
        "insert_station": row["insert_station"],
        "before_node_id": row["before_node_id"],
        "status": row["status"],
        "ts": row["ts"],
    }


def brief_shape(row: dict, from_station: str | None = None) -> dict:
    return {
        "id": row["id"],
        "node_id": row["node_id"],
        "from_node_id": row["from_node_id"],
        "from_station": from_station if from_station is not None else row["from_station"],
        "summary_md": row["summary_md"],
        "action_items": jloads(row["action_items_json"], []),
        "created_ts": row["created_ts"],
    }
