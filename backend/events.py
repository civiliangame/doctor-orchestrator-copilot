"""Per-session event bus → /ws/session/{id}/events.

Every UI-visible thing goes through broadcast(): envelope {seq, ts, type, data}
per API_CONTRACT.md. seq is monotonic per session, in-memory (contract says
clients dedupe by (type, data.id) and rehydrate via REST, so restarts are fine).
"""

import asyncio
import json
from collections import defaultdict

from fastapi import WebSocket

from db import now_iso

_seq: dict[int, int] = defaultdict(int)
_sockets: dict[int, set[WebSocket]] = defaultdict(set)


def register(session_id: int, ws: WebSocket) -> None:
    _sockets[session_id].add(ws)


def unregister(session_id: int, ws: WebSocket) -> None:
    _sockets[session_id].discard(ws)


def last_seq(session_id: int) -> int:
    return _seq[session_id]


async def broadcast(session_id: int, type_: str, data: dict) -> None:
    _seq[session_id] += 1
    frame = json.dumps(
        {"seq": _seq[session_id], "ts": now_iso(), "type": type_, "data": data}
    )
    dead = []
    for ws in list(_sockets[session_id]):
        try:
            await ws.send_text(frame)
        except Exception:
            dead.append(ws)
    for ws in dead:
        _sockets[session_id].discard(ws)


def broadcast_soon(session_id: int, type_: str, data: dict) -> None:
    """Fire-and-forget variant for sync code paths."""
    asyncio.get_event_loop().create_task(broadcast(session_id, type_, data))
