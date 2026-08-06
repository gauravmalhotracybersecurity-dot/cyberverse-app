"""
Thin wrapper around the Anthropic Messages API.

All AI Mentor features (chat, daily learning generation, resume review,
interview coach) go through the two functions below so there is exactly
one place that talks to the model.
"""
import json
import re
from typing import Optional

import httpx

from config import settings

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"


class ClaudeClientError(RuntimeError):
    pass


async def call_claude(
    system: str,
    messages: list[dict],
    max_tokens: int = 1024,
    temperature: float = 0.7,
) -> str:
    """Call Claude with a system prompt + message list, return the text reply."""
    if not settings.anthropic_api_key:
        raise ClaudeClientError(
            "ANTHROPIC_API_KEY is not set. Add it to backend/.env (see .env.example)."
        )

    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    body = {
        "model": settings.anthropic_model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system,
        "messages": messages,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(ANTHROPIC_URL, headers=headers, json=body)

    if resp.status_code != 200:
        raise ClaudeClientError(f"Anthropic API error {resp.status_code}: {resp.text}")

    data = resp.json()
    text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
    return "\n".join(text_blocks).strip()


def _strip_json_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


async def call_claude_json(
    system: str,
    messages: list[dict],
    max_tokens: int = 1500,
    temperature: float = 0.7,
) -> dict:
    """Call Claude and parse a strict-JSON reply. System prompt must instruct
    the model to reply with JSON only, no prose, no markdown fences."""
    raw = await call_claude(system, messages, max_tokens=max_tokens, temperature=temperature)
    cleaned = _strip_json_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ClaudeClientError(f"Model did not return valid JSON: {e}\nRaw reply: {raw[:500]}")
