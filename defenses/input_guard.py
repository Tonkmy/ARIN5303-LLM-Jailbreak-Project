"""Input defense scaffold."""

from __future__ import annotations

OVERRIDE_MARKERS = [
    "ignore previous instructions",
    "forget all prior rules",
    "system prompt",
    "developer message",
]


def check_input(prompt: str) -> dict:
    lowered = prompt.lower()
    for marker in OVERRIDE_MARKERS:
        if marker in lowered:
            return {"blocked": True, "reason": f"matched:{marker}"}
    return {"blocked": False, "reason": ""}
