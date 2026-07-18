"""Telnyx phone transport: outbound dial, media-stream bridge, STT→LLM→TTS.

Ported from the AHH pattern (SPEC.md § Telnyx transport). The interview loop
itself lives in orchestrator/interview.py — this package only moves audio and
utterances across the phone boundary.
"""
