"""Claude client wrapper.

- Reads CLAUDE_API_KEY (the var name in this project's .env).
- complete_json(): one call → parsed JSON dict, with fence-stripping and one
  reparse-retry. Fable falls back to Opus if the account lacks access.
- System prompts are lists of blocks so the SHARED context block can carry
  cache_control and be reused across the five per-turn workers (SPEC.md:
  identical first block ⇒ prefix cache hit for every worker).
"""

import json
import re

from anthropic import AsyncAnthropic, NotFoundError

from config import CLAUDE_API_KEY, MODEL_FABLE, MODEL_FABLE_FALLBACK

client = AsyncAnthropic(api_key=CLAUDE_API_KEY)

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)


def cached_block(text: str) -> dict:
    return {"type": "text", "text": text, "cache_control": {"type": "ephemeral"}}


def block(text: str) -> dict:
    return {"type": "text", "text": text}


def _extract_json(raw: str) -> dict:
    raw = _FENCE.sub("", raw.strip())
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"no JSON object in model output: {raw[:200]!r}")
    return json.loads(raw[start : end + 1])


async def complete(
    model: str,
    system: list[dict],
    messages: list[dict],
    max_tokens: int = 1024,
) -> str:
    """Raw text completion. messages: [{'role': 'user'|'assistant', 'content': ...}].

    No temperature param: claude-sonnet-5 rejects it with a 400 (deprecated for
    the Claude 5 family), and API default temperature is fine for every call here.
    """
    try:
        resp = await client.messages.create(
            model=model, system=system, messages=messages, max_tokens=max_tokens,
        )
    except NotFoundError:
        if model != MODEL_FABLE:
            raise
        resp = await client.messages.create(
            model=MODEL_FABLE_FALLBACK, system=system, messages=messages,
            max_tokens=max_tokens,
        )
    return "".join(b.text for b in resp.content if b.type == "text")


async def complete_json(
    model: str,
    system: list[dict],
    user_text: str,
    max_tokens: int = 1024,
) -> dict:
    """Completion that must return a JSON object. One retry on parse failure."""
    messages = [{"role": "user", "content": user_text}]
    raw = await complete(model, system, messages, max_tokens=max_tokens)
    try:
        return _extract_json(raw)
    except (ValueError, json.JSONDecodeError):
        retry = messages + [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": "That was not valid JSON. Reply with ONLY the JSON object, no prose, no fences."},
        ]
        raw = await complete(model, system, retry, max_tokens=max_tokens)
        return _extract_json(raw)
