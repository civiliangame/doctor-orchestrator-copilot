"""Soniox realtime STT for the phone leg (single speaker — no diarization).

Feed PCM16 @ 16 kHz; get whole patient utterances back via on_utterance.
End-of-utterance = Soniox <end> endpoint marker with buffered text, with a
UTTERANCE_DEBOUNCE_MS timer after the last final token as the fallback
(same debounce the v1 mic pipeline used; Soniox protocol notes from voice.py:
end-of-audio must be an empty TEXT frame — an empty binary frame is ignored).
"""

import asyncio
import json
import logging

import websockets

from config import SONIOX_API_KEY, SONIOX_MODEL, SONIOX_WS_URL, UTTERANCE_DEBOUNCE_MS

log = logging.getLogger("doc.stt")

_MARKER_TOKENS = {"<end>", "<fin>"}


class SonioxStream:
    """One Soniox connection per phone call."""

    def __init__(self, on_utterance) -> None:
        self.on_utterance = on_utterance  # async callback(text)
        self._ws = None
        self._recv_task: asyncio.Task | None = None
        self._debounce: asyncio.Task | None = None
        self._buffer = ""
        self._closed = False

    async def start(self) -> None:
        self._ws = await websockets.connect(SONIOX_WS_URL, max_size=None)
        await self._ws.send(json.dumps({
            "api_key": SONIOX_API_KEY,
            "model": SONIOX_MODEL,
            "audio_format": "pcm_s16le",
            "sample_rate": 16000,
            "num_channels": 1,
            "language_hints": ["en"],
            "enable_endpoint_detection": True,
        }))
        self._recv_task = asyncio.create_task(self._recv_loop())

    async def feed(self, pcm16: bytes) -> None:
        if self._ws is None or self._closed:
            return
        try:
            await self._ws.send(pcm16)
        except websockets.exceptions.WebSocketException:
            pass

    async def stop(self) -> None:
        self._closed = True
        self._cancel_debounce()
        if self._ws is not None:
            try:
                await self._ws.send("")  # empty TEXT frame = end of audio
            except Exception:
                pass
            try:
                await self._ws.close()
            except Exception:
                pass
        if self._recv_task:
            self._recv_task.cancel()

    # ------------------------------------------------------------- internals

    async def _recv_loop(self) -> None:
        try:
            async for raw in self._ws:
                if isinstance(raw, (bytes, bytearray)):
                    continue
                try:
                    payload = json.loads(raw)
                except json.JSONDecodeError:
                    continue
                if payload.get("error_code"):
                    log.error("soniox error %s: %s", payload["error_code"],
                              payload.get("error_message"))
                    return
                await self._feed_tokens(payload.get("tokens") or [])
                if payload.get("finished"):
                    return
        except websockets.exceptions.WebSocketException as e:
            log.warning("soniox connection dropped: %s", e)
        except asyncio.CancelledError:
            pass

    async def _feed_tokens(self, tokens: list[dict]) -> None:
        got_final = False
        endpoint = False
        for tok in tokens:
            text = tok.get("text") or ""
            if text in _MARKER_TOKENS:
                endpoint = True
                continue
            if tok.get("is_final"):
                self._buffer += text
                got_final = True
        if endpoint and self._buffer.strip():
            self._cancel_debounce()
            await self._flush()
        elif got_final:
            self._restart_debounce()

    def _restart_debounce(self) -> None:
        self._cancel_debounce()
        self._debounce = asyncio.create_task(self._debounce_fire())

    def _cancel_debounce(self) -> None:
        if self._debounce is not None and not self._debounce.done():
            self._debounce.cancel()
        self._debounce = None

    async def _debounce_fire(self) -> None:
        try:
            await asyncio.sleep(UTTERANCE_DEBOUNCE_MS / 1000)
        except asyncio.CancelledError:
            return
        if self._buffer.strip():
            await self._flush()

    async def _flush(self) -> None:
        text = " ".join(self._buffer.split())
        self._buffer = ""
        if text:
            try:
                await self.on_utterance(text)
            except Exception:
                log.exception("on_utterance failed")
