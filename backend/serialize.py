"""DB row -> API_CONTRACT.md shape serializers.

Shared by the REST routes and by orchestrator broadcasts so the WebSocket
events carry exactly the contract shapes.
"""

from db import jloads


def patient(r: dict) -> dict:
    return {"id": r["id"], "name": r["name"], "dob": r["dob"], "phone": r["phone"]}


def document(r: dict) -> dict:
    return {
        "id": r["id"], "patient_id": r["patient_id"], "title": r["title"],
        "doc_type": r["doc_type"], "author": r["author"], "date": r["date"],
        "content_md": r["content_md"],
    }


def run(r: dict) -> dict:
    return {
        "id": r["id"], "patient_id": r["patient_id"], "status": r["status"],
        "transport": r["transport"], "started_ts": r["started_ts"],
        "ended_ts": r["ended_ts"],
    }


def specialist(r: dict) -> dict:
    return {
        "id": r["id"], "run_id": r["run_id"], "key": r["key"],
        "display_name": r["display_name"], "rationale": r["rationale"],
        "status": r["status"],
    }


def finding(r: dict) -> dict:
    return {
        "id": r["id"], "run_id": r["run_id"], "specialist_id": r["specialist_id"],
        "kind": r["kind"], "severity": r["severity"], "title": r["title"],
        "detail": r["detail"], "quotes": jloads(r["quotes_json"], []),
        "patient_answerable": bool(r["patient_answerable"]),
    }


def question(r: dict) -> dict:
    return {
        "id": r["id"], "run_id": r["run_id"],
        "finding_ids": jloads(r["finding_ids_json"], []),
        "order": r["ord"], "question": r["question"],
        "sub_questions": jloads(r["sub_questions_json"], []),
        "completeness_criteria": r["completeness_criteria"], "status": r["status"],
    }


def specialist_task(r: dict) -> dict:
    return {
        "id": r["id"], "run_id": r["run_id"], "finding_id": r["finding_id"],
        "for_specialist": r["for_specialist"], "instruction": r["instruction"],
        "why": r["why"],
    }


def call(r: dict) -> dict:
    return {
        "id": r["id"], "run_id": r["run_id"], "transport": r["transport"],
        "status": r["status"], "started_ts": r["started_ts"],
        "ended_ts": r["ended_ts"],
    }


def call_turn(r: dict) -> dict:
    return {
        "id": r["id"], "call_id": r["call_id"], "speaker": r["speaker"],
        "text": r["text"], "ts": r["ts"],
    }


def answer(r: dict) -> dict:
    return {
        "id": r["id"], "question_id": r["question_id"],
        "summary_text": r["summary_text"], "complete": bool(r["complete"]),
        "ts": r["ts"],
    }


def intake(r: dict) -> dict:
    return {
        "id": r["id"], "run_id": r["run_id"],
        "chief_complaint": r["chief_complaint"], "hpi_md": r["hpi_md"],
        "meds_reconciliation_md": r["meds_reconciliation_md"],
        "resolved_contradictions_md": r["resolved_contradictions_md"],
        "open_items_md": r["open_items_md"], "created_ts": r["created_ts"],
    }
