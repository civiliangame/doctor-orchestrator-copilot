"""Central config. Every module reads env + constants from here, nowhere else."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
BACKEND = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
SONIOX_API_KEY = os.environ.get("SONIOX_API_KEY", "")

LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "")

# Telnyx transport (SPEC.md § Telnyx transport)
TELNYX_API_KEY = os.environ.get("TELNYX_API_KEY", "")
TELNYX_API_BASE = os.environ.get("TELNYX_API_BASE", "https://api.telnyx.com/v2")
TELNYX_CONNECTION_ID = os.environ.get("TELNYX_CONNECTION_ID", "")
TELNYX_FROM_NUMBER = os.environ.get("TELNYX_FROM_NUMBER", "")
PATIENT_PHONE = os.environ.get("PATIENT_PHONE", "")  # role-player's phone; seeded as patients.phone

# Public route for Telnyx webhook + media WS. stream_url must be wss://, so any
# scheme on PUBLIC_HOSTNAME is stripped here (AHH gotcha).
PUBLIC_HOSTNAME = os.environ.get("PUBLIC_HOSTNAME", "")
if "://" in PUBLIC_HOSTNAME:
    PUBLIC_HOSTNAME = PUBLIC_HOSTNAME.split("://", 1)[1]
PUBLIC_HOSTNAME = PUBLIC_HOSTNAME.strip("/")
STREAM_PATH = os.environ.get("STREAM_PATH", "/media-stream")

PORT = int(os.environ.get("PORT", "5000"))  # ngrok forwards to this port

SONIOX_WS_URL = "wss://stt-rt.soniox.com/transcribe-websocket"
SONIOX_MODEL = "stt-rt-v5"

# Model tiers per SPEC.md § Pipeline
MODEL_SONNET = "claude-sonnet-5"           # triage, specialists, interview loop
MODEL_FABLE = "claude-fable-5"             # orchestrator plan + intake compiler
MODEL_FABLE_FALLBACK = "claude-opus-4-8"   # if the account lacks Fable access

DB_PATH = BACKEND / "doc.sqlite3"

# Pipeline pacing (SPEC.md § Latency budgets, DEMO_SCRIPT.md § Timing tuning)
MAX_INTERVIEW_QUESTIONS = 8    # orchestrator keeps the highest-severity questions
PROBE_CAP = 3                  # follow-ups per question before moving on
SPECIALIST_TIMEOUT_S = 25      # skip specialist stragglers, log it
UTTERANCE_DEBOUNCE_MS = 900    # phone: silence after a Soniox final = end of utterance
