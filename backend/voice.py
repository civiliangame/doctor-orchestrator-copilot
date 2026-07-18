"""Voice pipeline: /ws/audio?session_id= (upload-only) → Soniox STT →
speaker-role mapping → 900ms end-of-turn debounce → turns.ingest_turn().

Contract (API_CONTRACT.md § WebSocket 1): binary frames = webm/opus mic chunks,
text frame "stop" (or disconnect) = end of audio. The ONLY thing sent down this
socket is a fatal {"error": {code, message}} before closing. Transcript display
flows through the events socket: transcript.partial here, transcript.turn via
turns.ingest_turn (which also fires the orchestrator — never broadcast it here).

Role mapping (SPEC.md § Turn pipeline): first speaker = staff; thereafter roles
STRICTLY ALTERNATE. Soniox diarization labels are advisory — a label change
signals "new turn started", but the role each turn gets comes from alternation,
so phantom labels / label swaps cannot derail role assignment.

Hard-won Soniox detail (from the old relay, commit 84cf579): end-of-audio must
be an empty TEXT frame; an empty binary frame is silently ignored.
"""

import asyncio
import json
import logging
import time

import websockets
from fastapi import APIRouter, WebSocket

import events
import turns
from config import (
    PATIENT_TURN_DEBOUNCE_MS,
    SONIOX_API_KEY,
    SONIOX_MODEL,
    SONIOX_WS_URL,
)

log = logging.getLogger("voice")
router = APIRouter()

_PARTIAL_MIN_INTERVAL = 0.25  # seconds — throttle transcript.partial to ~4/sec
_MARKER_TOKENS = {"<end>", "<fin>"}  # Soniox endpoint/finished markers, not speech


def _clean(text: str) -> str:
    return " ".join(text.split())


class TurnAssembler:
    """Pure (async-free) turn logic: feed Soniox token batches, get completed
    turns back. Testable standalone — see the __main__ smoke test."""

    def __init__(self) -> None:
        self.turn_index = 0        # completed turns so far → drives alternation
        self.label = None          # Soniox speaker label of the current turn
        self.final_text = ""       # finalized text accumulated for current turn
        self.interim_text = ""     # unstable tail, REPLACED on every response

    @property
    def role(self) -> str:
        """Role of the turn currently being assembled. Pure alternation:
        turn 0 is staff (the scripted greeting anchors this)."""
        return "staff" if self.turn_index % 2 == 0 else "patient"

    @property
    def partial_text(self) -> str:
        return _clean(self.final_text + self.interim_text)

    def feed(self, tokens: list[dict]) -> tuple[list[tuple[str, str]], bool]:
        """Process one Soniox response's tokens.

        Returns (completed_turns, got_final): turns completed by a speaker-label
        change (list of (role, text)), and whether any final token landed in the
        current turn (caller restarts the debounce timer on True).

        Only FINAL tokens drive speaker-change detection — interim labels
        flicker, and a spurious turn split would flip every subsequent role.
        """
        completed: list[tuple[str, str]] = []
        got_final = False
        interim_parts: list[str] = []

        for tok in tokens:
            text = tok.get("text") or ""
            if text in _MARKER_TOKENS:
                continue
            if tok.get("is_final"):
                label = tok.get("speaker")
                if self.label is None:
                    self.label = label
                elif label is not None and label != self.label:
                    # Speaker change beats the timer: close the current turn.
                    turn = self.flush()
                    if turn:
                        completed.append(turn)
                    self.label = label
                self.final_text += text
                got_final = True
            else:
                interim_parts.append(text)

        self.interim_text = "".join(interim_parts)
        return completed, got_final

    def flush(self, include_interim: bool = False) -> tuple[str, str] | None:
        """Close the current turn. Returns (role, cleaned_text) or None if the
        buffer was empty (empty turns never consume an alternation slot).

        include_interim=True (H9 force / dead-stream salvage) also drains the
        unstable tail — those tokens may never finalize.
        """
        text = _clean(self.final_text + (self.interim_text if include_interim else ""))
        self.final_text = ""
        self.label = None
        if include_interim:
            self.interim_text = ""
        if not text:
            return None
        role = self.role
        self.turn_index += 1
        return role, text


class _SessionState:
    def __init__(self) -> None:
        self.assembler = TurnAssembler()
        self.debounce_task: asyncio.Task | None = None
        self.last_partial_ts = 0.0
        self.last_partial_text = ""

    def cancel_debounce(self) -> None:
        if self.debounce_task is not None and not self.debounce_task.done():
            self.debounce_task.cancel()
        self.debounce_task = None


_sessions: dict[int, _SessionState] = {}


async def _ingest(session_id: int, role: str, text: str) -> None:
    """ingest_turn handles persistence, transcript.turn, and the orchestrator."""
    try:
        await turns.ingest_turn(session_id, role, text, source="soniox")
    except Exception:
        log.exception("ingest_turn failed (session %s, role %s)", session_id, role)


def _restart_debounce(session_id: int, state: _SessionState) -> None:
    state.cancel_debounce()
    state.debounce_task = asyncio.create_task(_debounce_fire(session_id, state))


async def _debounce_fire(session_id: int, state: _SessionState) -> None:
    try:
        await asyncio.sleep(PATIENT_TURN_DEBOUNCE_MS / 1000)
    except asyncio.CancelledError:
        return
    turn = state.assembler.flush()
    if turn:
        await _ingest(session_id, *turn)


async def _maybe_broadcast_partial(session_id: int, state: _SessionState) -> None:
    text = state.assembler.partial_text
    now = time.monotonic()
    if not text or text == state.last_partial_text:
        return
    if now - state.last_partial_ts < _PARTIAL_MIN_INTERVAL:
        return  # throttled; superseded by the next update or the final turn
    state.last_partial_ts = now
    state.last_partial_text = text
    await events.broadcast(
        session_id,
        "transcript.partial",
        {"speaker": state.assembler.role, "text": text},
    )


async def force_end_patient_turn(session_id: int) -> bool:
    """H9 operator fallback: immediately finalize the pending turn buffer
    (whatever its role). Returns True if something was flushed."""
    state = _sessions.get(session_id)
    if state is None:
        return False
    state.cancel_debounce()
    turn = state.assembler.flush(include_interim=True)
    if turn is None:
        return False
    await _ingest(session_id, *turn)
    return True


async def _send_fatal(ws: WebSocket, code: str, message: str) -> None:
    try:
        await ws.send_text(json.dumps({"error": {"code": code, "message": message}}))
    except Exception:
        pass


async def _pump_up(browser: WebSocket, soniox) -> None:
    """Mic chunks up; on "stop"/disconnect, send the empty TEXT frame that
    tells Soniox the audio is done so it flushes its finals."""
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
        try:
            await soniox.send("")  # MUST be an empty TEXT frame (see module doc)
        except Exception:
            pass


async def _pump_down(session_id: int, state: _SessionState, browser: WebSocket, soniox) -> None:
    """Consume Soniox responses until finished/error; drive the assembler."""
    async for raw in soniox:
        if isinstance(raw, (bytes, bytearray)):
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if payload.get("error_code"):
            log.error("soniox error %s: %s", payload["error_code"], payload.get("error_message"))
            await _send_fatal(
                browser, "soniox_error",
                f"Soniox: {payload.get('error_message', payload['error_code'])}",
            )
            return
        completed, got_final = state.assembler.feed(payload.get("tokens") or [])
        for role, text in completed:
            state.cancel_debounce()
            await _ingest(session_id, role, text)
        if got_final:
            _restart_debounce(session_id, state)
        await _maybe_broadcast_partial(session_id, state)
        if payload.get("finished"):
            return


async def _finish_task(task: asyncio.Task) -> None:
    task.cancel()
    try:
        await task
    except (asyncio.CancelledError, Exception):
        pass


@router.websocket("/ws/audio")
async def ws_audio(ws: WebSocket, session_id: int):
    await ws.accept()

    if not SONIOX_API_KEY:
        await _send_fatal(ws, "config", "SONIOX_API_KEY missing from .env")
        await ws.close()
        return

    state = _SessionState()
    _sessions[session_id] = state
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

            up = asyncio.create_task(_pump_up(ws, soniox))
            down = asyncio.create_task(_pump_down(session_id, state, ws, soniox))
            await asyncio.wait({up, down}, return_when=asyncio.FIRST_COMPLETED)

            if up.done() and not down.done():
                # Audio ended; give Soniox a moment to flush final tokens.
                try:
                    await asyncio.wait_for(down, timeout=5)
                except asyncio.TimeoutError:
                    pass
            await _finish_task(up)
            await _finish_task(down)
    except (websockets.exceptions.WebSocketException, OSError) as exc:
        log.error("soniox connection failed: %s", exc)
        await _send_fatal(ws, "soniox_connect_failed", f"Soniox connection failed: {exc}")
    finally:
        state.cancel_debounce()
        if _sessions.get(session_id) is state:
            _sessions.pop(session_id, None)
        # Stream is over — flush whatever is pending (salvage interim too;
        # a dead stream means those tokens will never finalize).
        turn = state.assembler.flush(include_interim=True)
        if turn:
            await _ingest(session_id, *turn)
        try:
            await ws.close()
        except Exception:
            pass


if __name__ == "__main__":
    # Smoke test for the pure role-mapping/turn logic (no sockets, no DB).
    def tok(text, final=True, speaker=None):
        return {"text": text, "is_final": final, "speaker": speaker}

    a = TurnAssembler()

    # 1. First speaker is staff, whatever their diarization label.
    done, got = a.feed([tok("Hi ", speaker="2"), tok("Maria.", speaker="2")])
    assert done == [] and got and a.role == "staff" and a.partial_text == "Hi Maria."

    # 2. Label change closes the turn; next turn is patient by alternation.
    done, _ = a.feed([tok("Hello ", speaker="1")])
    assert done == [("staff", "Hi Maria.")], done
    assert a.role == "patient"

    # 3. Phantom third label: closes patient turn, next role is staff (not a
    #    third role) — alternation is authoritative.
    done, _ = a.feed([tok("doctor.", speaker="1"), tok("Okay.", speaker="7")])
    assert done == [("patient", "Hello doctor.")], done
    assert a.role == "staff"

    # 4. Interim tokens show in partials but never finalize a turn.
    done, got = a.feed([tok(" so", final=False, speaker="7")])
    assert done == [] and not got and a.partial_text == "Okay. so"
    assert a.flush() == ("staff", "Okay.")  # debounce-style flush drops interim

    # 5. Empty debounce flush consumes no alternation slot.
    assert a.role == "patient" and a.flush() is None and a.role == "patient"

    # 6. Same label resuming after a debounce flush still alternates
    #    (alternation wins over label continuity, per SPEC).
    a.feed([tok("Chest pain.", speaker="7")])
    assert a.role == "patient" and a.flush() == ("patient", "Chest pain.")

    # 7. H9 force-flush salvages interim text.
    a.feed([tok("Take ", speaker="1"), tok("aspirin", final=False, speaker="1")])
    assert a.flush(include_interim=True) == ("staff", "Take aspirin")

    print("TurnAssembler smoke test: ok")
