"""Central config. Every module reads env + constants from here, nowhere else."""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
BACKEND = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
SONIOX_API_KEY = os.environ.get("SONIOX_API_KEY", "")

SONIOX_WS_URL = "wss://stt-rt.soniox.com/transcribe-websocket"
SONIOX_MODEL = "stt-rt-v5"

# Model tiers per SPEC.md § Per-turn workers
MODEL_SONNET = "claude-sonnet-5"          # contradictions, suggestions (latency-critical)
MODEL_HAIKU = "claude-haiku-4-5-20251001" # guardrails, chart, todos (mechanical)
MODEL_FABLE = "claude-fable-5"            # end-of-session compile
MODEL_FABLE_FALLBACK = "claude-opus-4-8"  # if the account lacks Fable access

DB_PATH = BACKEND / "doc.sqlite3"
SEED_IMAGES_DIR = BACKEND / "seed" / "images"

PATIENT_TURN_DEBOUNCE_MS = 900   # SPEC.md § Turn pipeline
TRANSCRIPT_CONTEXT_TURNS = 20    # trim to 10 if the 3s budget is blown
MAX_SUGGESTIONS_PER_TURN = 2
