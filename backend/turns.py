"""Turn ingestion — THE seam between voice and orchestrator (SPEC.md).

Both the voice pipeline (debounced, role-mapped Soniox finals) and
POST /api/dev/inject-turn call ingest_turn(). Voice owns end-of-turn detection;
by the time a turn reaches here it is final, and a patient turn always fires
an orchestrator tick.
"""

import asyncio

import events
import orchestrator
from db import ins, now_iso, one


async def ingest_turn(session_id: int, speaker: str, text: str, source: str = "inject") -> dict:
    assert speaker in ("staff", "patient"), speaker
    session = one("SELECT * FROM sessions WHERE id=?", (session_id,))
    if session is None:
        raise ValueError(f"unknown session {session_id}")
    if session["ended_ts"]:
        raise ValueError(f"session {session_id} already ended")

    ts = now_iso()
    turn_id = ins(
        "transcript_turns",
        session_id=session_id, speaker=speaker, text=text, ts=ts, source=source,
    )
    turn = {"id": turn_id, "session_id": session_id, "speaker": speaker, "text": text, "ts": ts}
    await events.broadcast(session_id, "transcript.turn", turn)

    if speaker == "patient":
        asyncio.create_task(orchestrator.on_patient_turn(session_id, turn_id))
    return turn
