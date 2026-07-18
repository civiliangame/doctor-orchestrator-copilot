"""DOC backend — FastAPI app assembly.

Run: uvicorn main:app --reload  (port 8000)
Contract: API_CONTRACT.md at repo root. System design: SPEC.md.

The old raw Soniox relay (/ws/transcribe) is replaced per the contract's
migration note: voice.py owns /ws/audio (upload-only) and translates Soniox
tokens into events on /ws/session/{id}/events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import voice
from config import CLAUDE_API_KEY, SONIOX_API_KEY
from db import init_db
from routes import core, dev, images, sessions
from seed import seed_all

app = FastAPI(title="DOC backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    init_db()
    seed_all()


@app.get("/health")
async def health():
    return {
        "ok": True,
        "soniox_key_loaded": bool(SONIOX_API_KEY),
        "claude_key_loaded": bool(CLAUDE_API_KEY),
    }


app.include_router(core.router)
app.include_router(sessions.router)
app.include_router(dev.router)
app.include_router(images.router)
app.include_router(voice.router)
