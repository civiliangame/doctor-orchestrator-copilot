"""Telnyx-facing HTTP surface: POST /webhook (ACK + hangup detection) and the
media-stream WebSocket at STREAM_PATH (Telnyx connects to US as a WS client).

Wire protocol (AHH, verified against Telnyx docs): JSON text frames.
In:  {"event": "start"|"media"|"stop"|"dtmf", ...}; media payloads are ~20ms
     of base64 G.711 μ-law 8 kHz mono; FILTER track=="inbound" or you echo
     the agent's own audio back into STT.
Out: {"event":"media","media":{"payload":<b64 μ-law>}} and {"event":"clear"}.
"""

import asyncio
import base64
import json
import logging

from fastapi import APIRouter, Request, Response, WebSocket, WebSocketDisconnect

from config import STREAM_PATH
from orchestrator import interview
from orchestrator.run import finish_run

from telephony import telnyx
from telephony.audio import UlawDecoder
from telephony.stt import SonioxStream

log = logging.getLogger("doc.telephony")
router = APIRouter()


@router.post("/webhook")
@router.post("/")
async def webhook(request: Request):
    """ACK everything with 200; hangup is our only real signal here (the media
    WS 'stop' usually beats it — force_end is idempotent)."""
    try:
        body = await request.json()
        data = body.get("data", {})
        event_type = data.get("event_type", "")
        payload = data.get("payload", {})
        if event_type == "call.hangup":
            ccid = payload.get("call_control_id", "")
            call_id = telnyx.CCID_TO_CALL.get(ccid)
            session = interview.SESSIONS.get(call_id) if call_id else None
            if session is not None:
                asyncio.create_task(session.force_end())
        if event_type:
            log.info("telnyx webhook: %s", event_type)
    except Exception:
        log.exception("webhook parse failed")
    return Response(status_code=200)


@router.websocket(STREAM_PATH)
async def media_stream(ws: WebSocket):
    await ws.accept()
    try:
        call_id = int(ws.query_params["call_id"])
        run_id = int(ws.query_params["run_id"])
    except (KeyError, ValueError):
        log.error("media stream connected without call_id/run_id query params")
        await ws.close()
        return

    log.info("media stream connected (call=%s run=%s)", call_id, run_id)
    decoder = UlawDecoder(target_rate=16000)
    transport = telnyx.TelnyxTransport(ws, call_id)
    session: interview.InterviewSession | None = None
    stt: SonioxStream | None = None

    async def on_utterance(text: str) -> None:
        # Patient finished speaking: flush any queued agent audio (barge-in)
        # and feed the interview loop.
        await transport.clear()
        if session is not None:
            # Task, not await: a model turn takes seconds and must not block
            # the STT token loop. The session's lock + pending buffer keep
            # utterance ordering safe.
            asyncio.create_task(session.on_patient_utterance(text))

    try:
        while True:
            msg = await ws.receive()
            if msg.get("type") == "websocket.disconnect":
                break
            raw = msg.get("text")
            if not raw:
                continue
            try:
                frame = json.loads(raw)
            except json.JSONDecodeError:
                continue
            event = frame.get("event")

            if event == "start":
                # Callee answered and the stream is live. Greeting fires only
                # now — both Telnyx and the pipeline are ready (AHH gotcha).
                await telnyx.mark_call_active(run_id, call_id)
                stt = SonioxStream(on_utterance)
                await stt.start()
                on_end = telnyx.ON_END.get(call_id) or finish_run
                session = interview.InterviewSession(
                    run_id, call_id, transport, on_end=on_end
                )
                asyncio.create_task(session.start())

            elif event == "media":
                media = frame.get("media", {})
                if media.get("track", "inbound") != "inbound":
                    continue  # never feed our own audio back into STT
                payload = media.get("payload")
                if payload and stt is not None:
                    try:
                        ulaw = base64.b64decode(payload)
                    except Exception:
                        continue  # phones drop frames all the time
                    await stt.feed(decoder.decode(ulaw))

            elif event == "stop":
                break
            # dtmf and everything else: ignore
    except WebSocketDisconnect:
        pass
    except Exception:
        log.exception("media stream failed (call=%s)", call_id)
    finally:
        log.info("media stream closed (call=%s)", call_id)
        if stt is not None:
            await stt.stop()
        if session is not None and not session.ended:
            await session.force_end()
