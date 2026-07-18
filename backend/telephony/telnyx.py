"""Telnyx Call Control: outbound dial + call actions (AHH pattern, raw httpx).

Stream params ride on the dial request — Telnyx opens the media WS to
wss://{PUBLIC_HOSTNAME}{STREAM_PATH}?call_id=...&run_id=... when the callee
answers; per-call context travels in those query params (the only way for
outbound calls). PCMU both directions, bidirectional rtp.
"""

import base64
import json
import logging
from urllib.parse import quote

import httpx

import events
import serialize
from config import (
    PUBLIC_HOSTNAME,
    STREAM_PATH,
    TELNYX_API_BASE,
    TELNYX_API_KEY,
    TELNYX_CONNECTION_ID,
    TELNYX_FROM_NUMBER,
)
from db import ex, one

log = logging.getLogger("doc.telnyx")

# call_control_id -> call_id, for webhook hangup routing
CCID_TO_CALL: dict[str, int] = {}
# call_id -> on_end callback, handed to the media-stream handler at dial time
ON_END: dict[int, object] = {}


async def dial(run_id: int, call_id: int, on_end) -> None:
    """Place the outbound call. The media WS 'start' event (routes.py) flips
    the call active and starts the InterviewSession."""
    if not TELNYX_API_KEY:
        raise RuntimeError("TELNYX_API_KEY missing from .env")
    run = one("SELECT * FROM runs WHERE id=?", (run_id,))
    patient = one("SELECT * FROM patients WHERE id=?", (run["patient_id"],))
    to_number = patient["phone"]

    stream_url = (
        f"wss://{PUBLIC_HOSTNAME}{STREAM_PATH}"
        f"?call_id={call_id}&run_id={run_id}"
    )
    body = {
        "connection_id": TELNYX_CONNECTION_ID,
        "to": to_number,
        "from": TELNYX_FROM_NUMBER,
        "stream_url": stream_url,
        "stream_track": "inbound_track",
        "stream_bidirectional_mode": "rtp",
        "stream_bidirectional_codec": "PCMU",
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            f"{TELNYX_API_BASE}/calls",
            headers={"Authorization": f"Bearer {TELNYX_API_KEY}"},
            json=body,
        )
    resp.raise_for_status()
    ccid = resp.json()["data"]["call_control_id"]
    ex("UPDATE calls SET telnyx_call_control_id=? WHERE id=?", (ccid, call_id))
    CCID_TO_CALL[ccid] = call_id
    ON_END[call_id] = on_end
    log.info("dialing %s (call=%s ccid=%s)", to_number, call_id, ccid)


async def call_action(ccid: str, action: str, payload: dict | None = None) -> None:
    """Generic Call Control action: POST /calls/{ccid}/actions/{action}."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                f"{TELNYX_API_BASE}/calls/{quote(ccid, safe='')}/actions/{action}",
                headers={"Authorization": f"Bearer {TELNYX_API_KEY}"},
                json=payload or {},
            )
        if resp.status_code >= 400:
            log.warning("telnyx %s -> %s: %s", action, resp.status_code, resp.text[:200])
    except httpx.HTTPError as e:
        log.warning("telnyx %s failed: %s", action, e)


class TelnyxTransport:
    """Speaks over the live media WS; hangs up via Call Control."""

    def __init__(self, ws, call_id: int) -> None:
        self.ws = ws
        self.call_id = call_id

    async def speak(self, text: str) -> None:
        from telephony import tts
        try:
            async for ulaw in tts.speak_ulaw(text):
                await self.ws.send_text(json.dumps({
                    "event": "media",
                    "media": {"payload": base64.b64encode(ulaw).decode()},
                }))
        except Exception:
            log.exception("TTS/send failed (call=%s)", self.call_id)

    async def clear(self) -> None:
        """Barge-in: flush Telnyx's queued outbound audio."""
        try:
            await self.ws.send_text(json.dumps({"event": "clear"}))
        except Exception:
            pass

    async def hangup(self) -> None:
        row = one("SELECT telnyx_call_control_id FROM calls WHERE id=?", (self.call_id,))
        ccid = row and row["telnyx_call_control_id"]
        if ccid:
            await call_action(ccid, "hangup")
            CCID_TO_CALL.pop(ccid, None)
        ON_END.pop(self.call_id, None)


async def mark_call_active(run_id: int, call_id: int) -> None:
    ex("UPDATE calls SET status='active' WHERE id=?", (call_id,))
    row = one("SELECT * FROM calls WHERE id=?", (call_id,))
    await events.broadcast(run_id, "call.status", serialize.call(row))
