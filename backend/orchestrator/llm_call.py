"""Orchestrator-local Claude call helper.

Why not llm.complete_json? Two orchestrator-specific needs on top of it:
- thinking is explicitly DISABLED on Sonnet 5 (claude-sonnet-5 runs adaptive
  thinking by default when the field is omitted, which would burn the tight
  512/768 per-worker max_tokens and the 3s first-card budget);
- callers here (compile_session) also need a full-failure Opus fallback, not
  just the NotFoundError one.
We reuse llm.py's shared AsyncAnthropic client + block helpers. No sampling
params are ever sent (claude-sonnet-5 / claude-fable-5 reject them).
"""

import json
import logging
import re

from anthropic import NotFoundError

from config import MODEL_FABLE, MODEL_FABLE_FALLBACK, MODEL_SONNET
from llm import client

log = logging.getLogger("doc.orchestrator")

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def extract_json(raw: str) -> dict:
    raw = _FENCE.sub("", raw.strip())
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in model output: {raw[:200]!r}")
    return json.loads(raw[start : end + 1])


def _request_kwargs(model: str) -> dict:
    kwargs: dict = {}
    if model == MODEL_SONNET:
        # Sonnet 5 defaults to adaptive thinking; disable for latency + budget.
        kwargs["thinking"] = {"type": "disabled"}
    # Haiku: no thinking by default. Fable: thinking always on, param must be omitted.
    return kwargs


async def _create(model: str, system: list[dict], messages: list[dict], max_tokens: int):
    return await client.messages.create(
        model=model, system=system, messages=messages,
        max_tokens=max_tokens, **_request_kwargs(model),
    )


async def complete_json(
    model: str, system: list[dict], user_text: str, max_tokens: int = 1024
) -> dict:
    """One call -> parsed JSON object. One reparse-retry; Fable->Opus fallback."""
    messages = [{"role": "user", "content": user_text}]
    try:
        resp = await _create(model, system, messages, max_tokens)
    except NotFoundError:
        if model != MODEL_FABLE:
            raise
        log.info("model %s unavailable, falling back to %s", model, MODEL_FABLE_FALLBACK)
        resp = await _create(MODEL_FABLE_FALLBACK, system, messages, max_tokens)
        model = MODEL_FABLE_FALLBACK
    raw = "".join(b.text for b in resp.content if b.type == "text")
    try:
        return extract_json(raw)
    except (ValueError, json.JSONDecodeError):
        if resp.stop_reason == "max_tokens":
            # Truncated mid-JSON: same prompt, double the budget.
            log.warning("JSON truncated at max_tokens=%s (model=%s) — retrying at 2x",
                        max_tokens, model)
            resp = await _create(model, system, messages, max_tokens * 2)
        else:
            log.warning("JSON parse failed (model=%s stop=%s len=%s) — reprompting",
                        model, resp.stop_reason, len(raw))
            retry = messages + [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": "That was not valid JSON. Reply with ONLY the JSON object, no prose, no fences."},
            ]
            resp = await _create(model, system, retry, max_tokens)
        raw = "".join(b.text for b in resp.content if b.type == "text")
        return extract_json(raw)
