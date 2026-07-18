"""DOC backend — FastAPI app assembly (context-rot pivot).

Run: uvicorn main:app --port 5000    (ngrok forwards the same port to Telnyx)
Contract: API_CONTRACT.md at repo root. System design: SPEC.md.

NEVER run --reload during a live phone call — a mid-call reload kills it.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CLAUDE_API_KEY, SONIOX_API_KEY, TELNYX_API_KEY, LIVEKIT_API_KEY
from db import init_db
from routes import core, dev
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
        "claude_key_loaded": bool(CLAUDE_API_KEY),
        "soniox_key_loaded": bool(SONIOX_API_KEY),
        "telnyx_key_loaded": bool(TELNYX_API_KEY),
        "livekit_key_loaded": bool(LIVEKIT_API_KEY),
    }


app.include_router(core.router)
app.include_router(dev.router)

# Telnyx-facing routes (/webhook + /media-stream) — optional so the sim path
# works before/without the telephony layer.
try:
    from telephony import routes as telephony_routes
    app.include_router(telephony_routes.router)
except ImportError:
    pass
