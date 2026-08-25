from __future__ import annotations

import anthropic

from .config import Settings


def stream_reply(settings: Settings, system: str, messages: list[dict]) -> str:
    client = anthropic.Anthropic()
    parts: list[str] = []
    with client.messages.stream(
        model=settings.model,
        max_tokens=settings.max_tokens,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            parts.append(text)
    print()
    return "".join(parts)

