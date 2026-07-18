"""DOC backend — FastAPI orchestrator.

Step 1: real-time transcription relay.
Browser mic audio (webm/opus chunks) -> /ws/transcribe -> Soniox STT
(diarized) -> transcript token events -> browser.

All transcript traffic flows through this backend on purpose: the
orchestrator (per-patient-turn Claude calls) hooks in here later.
"""

import asyncio
import json
import os
from pathlib import Path

import websockets
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

SONIOX_WS_URL = "wss://stt-rt.soniox.com/transcribe-websocket"
SONIOX_MODEL = "stt-rt-v5"
SONIOX_API_KEY = os.environ.get("SONIOX_API_KEY", "")

app = FastAPI(title="DOC backend")


@app.get("/health")
async def health():
    return {"ok": True, "soniox_key_loaded": bool(SONIOX_API_KEY)}


@app.websocket("/ws/transcribe")
async def ws_transcribe(browser: WebSocket):
    await browser.accept()

    if not SONIOX_API_KEY:
        await browser.send_text(json.dumps(
            {"error_code": 500, "error_message": "SONIOX_API_KEY missing from .env"}
        ))
        await browser.close()
        return

    try:
        async with websockets.connect(SONIOX_WS_URL, max_size=None) as soniox:
            await soniox.send(json.dumps({
                "api_key": SONIOX_API_KEY,
                "model": SONIOX_MODEL,
                "audio_format": "auto",  # browser sends containerized webm/opus
                "language_hints": ["en"],
                "enable_speaker_diarization": True,
                "enable_endpoint_detection": True,
            }))

            async def browser_to_soniox():
                """Pump mic chunks up; on stop/disconnect, send the empty
                frame that tells Soniox the audio is done."""
                try:
                    while True:
                        msg = await browser.receive()
                        if msg["type"] == "websocket.disconnect":
                            break
                        if msg.get("bytes"):
                            await soniox.send(msg["bytes"])
                        elif msg.get("text") == "stop":
                            break
                finally:
                    # Empty TEXT frame = end-of-audio. An empty binary frame
                    # is ignored by Soniox (verified 2026-07-18); it must be text.
                    try:
                        await soniox.send("")
                    except Exception:
                        pass

            async def soniox_to_browser():
                """Relay Soniox token/error messages down verbatim until the
                finished/error message."""
                async for raw in soniox:
                    if isinstance(raw, (bytes, bytearray)):
                        continue
                    await browser.send_text(raw)
                    try:
                        payload = json.loads(raw)
                    except json.JSONDecodeError:
                        continue
                    if payload.get("finished") or payload.get("error_code"):
                        break

            up = asyncio.create_task(browser_to_soniox())
            down = asyncio.create_task(soniox_to_browser())
            await asyncio.wait({up, down}, return_when=asyncio.FIRST_COMPLETED)

            if up.done() and not down.done():
                # audio ended; give Soniox a moment to flush final tokens
                try:
                    await asyncio.wait_for(down, timeout=5)
                except asyncio.TimeoutError:
                    down.cancel()
            else:
                up.cancel()
    except websockets.exceptions.WebSocketException as exc:
        try:
            await browser.send_text(json.dumps(
                {"error_code": 502, "error_message": f"Soniox connection failed: {exc}"}
            ))
        except Exception:
            pass
    finally:
        try:
            await browser.close()
        except Exception:
            pass
