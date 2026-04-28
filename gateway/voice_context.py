"""Helpers for voice-mode chat completion context handling."""

from __future__ import annotations

import os
from typing import Any

_VOICE_HISTORY_LIMIT_DEFAULT = 8


def _is_voice_mode_chat_request(messages: list[dict[str, Any]] | None) -> bool:
    if not isinstance(messages, list):
        return False
    for message in messages:
        if not isinstance(message, dict):
            continue
        content = message.get("content", "")
        if isinstance(content, str) and "HERMES_VOICE_MODE=1" in content:
            return True
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text") or part.get("content")
                    if isinstance(text, str) and "HERMES_VOICE_MODE=1" in text:
                        return True
                elif isinstance(part, str) and "HERMES_VOICE_MODE=1" in part:
                    return True
    return False


def _voice_history_limit() -> int:
    raw_limit = os.getenv("HERMES_VOICE_MAX_HISTORY_MESSAGES", str(_VOICE_HISTORY_LIMIT_DEFAULT))
    try:
        return max(0, int(raw_limit))
    except (TypeError, ValueError):
        return _VOICE_HISTORY_LIMIT_DEFAULT


def _limit_voice_history(
    history: list[dict[str, Any]], messages: list[dict[str, Any]] | None
) -> list[dict[str, Any]]:
    if not _is_voice_mode_chat_request(messages):
        return history
    limit = _voice_history_limit()
    if limit <= 0:
        return []
    return history[-limit:]
