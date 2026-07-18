"""Beat C: POST /api/nodes/{node_id}/images — multimodal read -> chart entries.

An imaging tech uploads a (synthetic, demo) medical image. We make ONE Claude
multimodal call, get 1-3 findings STRICTLY framed as observations "Flagged for
Dr. Zhang's review" (never a diagnosis, never treatment advice), append each to
the append-only chart_entries table, and broadcast each as a chart.entry event
to every session of the visit. Returns {"findings": ChartEntry[]}.

Contract: API_CONTRACT.md § Beat C. Framing rule: DEMO_SCRIPT.md § Beat C.
"""

import base64
import json

from fastapi import APIRouter, File, UploadFile

import db
import events
import llm
from config import MODEL_SONNET
from routes.core import ApiError, ContractRoute, chart_entry

router = APIRouter(prefix="/api", route_class=ContractRoute)

MAX_BYTES = 10 * 1024 * 1024
ALLOWED = {"image/jpeg": "image/jpeg", "image/png": "image/png", "image/jpg": "image/jpeg"}

SYSTEM_PROMPT = (
    "You assist an imaging technician by flagging observations on a SYNTHETIC "
    "demo medical image for the attending physician, Dr. Zhang. This is a "
    "hackathon demo with fabricated data, not real patient care.\n\n"
    "Rules — follow exactly:\n"
    "- Return 1 to 3 findings.\n"
    "- Each finding is an OBSERVATION flagged for review, phrased to begin with "
    "\"Flagged for Dr. Zhang's review: \".\n"
    "- NEVER state or imply a diagnosis. NEVER give treatment advice.\n"
    "- If the image is a lab panel, cite the abnormal values with their exact "
    "numbers and reference ranges; do not flag values that are within range.\n"
    "- If the image is a scan (e.g. a CT slice) and there is a stated priority "
    "region, attend to it and report what is or is not visible there; it is fine "
    "to note the study looks broadly unremarkable.\n\n"
    "Respond with STRICT JSON and nothing else, in exactly this shape:\n"
    '{"findings": [{"category": "finding", "text": "Flagged for Dr. Zhang\'s review: ..."}]}'
)

USER_TEXT = (
    "Read the attached synthetic demo image. The standing imaging priority for "
    "this patient is the upper-left thoracic region (radiating-pain escalation in "
    "effect). Return the strict JSON object of findings as instructed."
)


async def _call_claude(messages: list[dict]) -> str:
    """One multimodal messages.create via the shared client. We call llm.client
    directly (not llm.complete) because complete() sends temperature=0.0, which
    the sonnet-5 model rejects as deprecated."""
    resp = await llm.client.messages.create(
        model=MODEL_SONNET,
        system=[llm.block(SYSTEM_PROMPT)],
        messages=messages,
        max_tokens=600,
    )
    return "".join(b.text for b in resp.content if b.type == "text")


async def _read_findings(media_type: str, b64: str) -> list[dict]:
    """One multimodal Claude call -> list of {category, text}. One JSON reparse retry."""
    user_msg = {
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {"type": "base64", "media_type": media_type, "data": b64},
            },
            {"type": "text", "text": USER_TEXT},
        ],
    }
    raw = await _call_claude([user_msg])
    try:
        parsed = llm._extract_json(raw)
    except (ValueError, json.JSONDecodeError):
        retry = [
            user_msg,
            {"role": "assistant", "content": raw},
            {"role": "user", "content": "That was not valid JSON. Reply with ONLY the JSON object, no prose, no fences."},
        ]
        raw = await _call_claude(retry)
        parsed = llm._extract_json(raw)

    findings = parsed.get("findings", [])
    if not isinstance(findings, list) or not findings:
        raise ValueError("model returned no findings")
    return findings[:3]


@router.post("/nodes/{node_id}/images")
async def upload_image(node_id: int, image: UploadFile = File(...)):
    node = db.one("SELECT * FROM journey_nodes WHERE id=?", (node_id,))
    if node is None:
        raise ApiError(404, "not_found", f"unknown node {node_id}")

    media_type = ALLOWED.get((image.content_type or "").lower())
    if media_type is None:
        raise ApiError(
            400, "bad_request",
            f"unsupported content type {image.content_type!r}; expected image/jpeg or image/png",
        )

    data = await image.read()
    if not data:
        raise ApiError(400, "bad_request", "empty image upload")
    if len(data) > MAX_BYTES:
        raise ApiError(400, "bad_request", f"image exceeds 10MB limit ({len(data)} bytes)")

    b64 = base64.b64encode(data).decode("ascii")

    try:
        raw_findings = await _read_findings(media_type, b64)
    except Exception as e:  # noqa: BLE001 — any vision/parse failure -> 502 per contract
        raise ApiError(502, "vision_failed", f"multimodal read failed: {e}")

    visit_id = node["visit_id"]
    station = node["station"]

    # Persist (append-only) and build the full ChartEntry contract shape.
    out: list[dict] = []
    for f in raw_findings:
        text = (f.get("text") or "").strip() if isinstance(f, dict) else str(f).strip()
        if not text:
            continue
        category = (f.get("category") if isinstance(f, dict) else None) or "finding"
        ts = db.now_iso()
        entry_id = db.ins(
            "chart_entries",
            visit_id=visit_id, node_id=node_id, ts=ts, category=category, text=text,
        )
        out.append(chart_entry({
            "id": entry_id, "visit_id": visit_id, "node_id": node_id,
            "node_station": station, "category": category, "text": text, "ts": ts,
        }))

    if not out:
        raise ApiError(502, "vision_failed", "model returned no usable findings")

    # Broadcast each as chart.entry to every session of ANY node in this visit.
    session_rows = db.q(
        """SELECT s.id FROM sessions s
           JOIN journey_nodes n ON n.id = s.node_id
           WHERE n.visit_id=?""",
        (visit_id,),
    )
    for entry in out:
        for s in session_rows:
            await events.broadcast(s["id"], "chart.entry", entry)

    return {"findings": out}
