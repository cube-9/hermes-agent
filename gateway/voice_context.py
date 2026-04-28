"""Helpers for voice-mode chat completion context handling."""

from __future__ import annotations

from typing import Any


def _is_voice_mode_chat_request(messages: list[dict[str, Any]] | None) -> bool:
    if not isinstance(messages, list):
        return False
    for message in messages:
        if not isinstance(message, dict):
            continue
        if message.get("role") != "system":
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
