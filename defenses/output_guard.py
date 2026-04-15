"""Output defense scaffold."""

from __future__ import annotations

UNSAFE_MARKERS = [
    "step-by-step instructions",
    "here is how to",
    "first, gather",
]


def check_output(response: str) -> dict:
    lowered = response.lower()
    for marker in UNSAFE_MARKERS:
        if marker in lowered:
            return {"blocked": True, "reason": f"matched:{marker}"}
    return {"blocked": False, "reason": ""}
