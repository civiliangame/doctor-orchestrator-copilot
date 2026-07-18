"""TTS via LiveKit Inference (SPEC.md decision 7) — uses the LiveKit Cloud
creds already in .env; no separate TTS vendor key.

speak_ulaw() yields base64-ready μ-law 8 kHz chunks for Telnyx media frames.
"""

import logging

import aiohttp
from livekit.agents import inference

from config import LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_URL

from telephony.audio import UlawEncoder

log = logging.getLogger("doc.tts")

TTS_MODEL = "cartesia/sonic-3"
TTS_VOICE = "9626c31c-bec5-4cca-baa8-f8ba9e84c8bc"  # warm female (LiveKit docs demo voice)
TTS_SAMPLE_RATE = 16000

_tts: inference.TTS | None = None


def _get_tts() -> inference.TTS:
    global _tts
    if _tts is None:
        # We run outside a LiveKit agent worker, so the plugin needs its own
        # aiohttp session (must be created inside a running event loop).
        _tts = inference.TTS(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            language="en",
            sample_rate=TTS_SAMPLE_RATE,
            # base_url deliberately omitted: the default is LiveKit's inference
            # gateway (agent-gateway.livekit.cloud), NOT the room server URL.
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
            http_session=aiohttp.ClientSession(),
        )
    return _tts


async def speak_ulaw(text: str):
    """Synthesize text -> async generator of μ-law 8 kHz byte chunks."""
    tts = _get_tts()
    encoder = UlawEncoder(source_rate=TTS_SAMPLE_RATE)
    stream = tts.synthesize(text)
    async for chunk in stream:
        frame = chunk.frame
        if frame is None:
            continue
        pcm = bytes(frame.data)
        if frame.sample_rate != TTS_SAMPLE_RATE:
            # trust the frame header over our request
            encoder = UlawEncoder(source_rate=frame.sample_rate)
        ulaw = encoder.encode(pcm)
        if ulaw:
            yield ulaw
