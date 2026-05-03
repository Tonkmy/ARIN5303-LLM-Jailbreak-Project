"""Rule-based output guard.

The output guard blocks responses that appear to disclose protected prompt
artifacts. It does not block ordinary refusals, because refusals are the desired
safe outcome for attack prompts.
"""

from __future__ import annotations


REFUSAL_MARKERS = [
    "i can't",
    "i cannot",
    "i'm unable",
    "i will not",
    "cannot provide",
    "can't provide",
    "not appropriate",
    "i can't assist",
    "i cannot assist",
    "sorry",
]

SECRET_TERMS = [
    "system prompt",
    "developer message",
    "hidden instruction",
    "hidden instructions",
    "hidden prompt",
    "hidden policy",
    "hidden rules",
    "private instructions",
    "private rules",
    "prompt stack",
    "instruction hierarchy",
    "confidential system prompt",
]

DISCLOSURE_TERMS = [
    "here is",
    "the following",
    "as requested",
    "i was instructed",
    "my system prompt",
    "the system prompt is",
    "the developer message is",
    "the hidden instructions are",
    "the private instructions are",
    "rules i follow",
    "you are a helpful assistant",
]


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def check_output(response: str) -> dict:
    lowered = response.lower()

    # If the model is clearly refusing, do not hide that safe response.
    if _contains_any(lowered, REFUSAL_MARKERS):
        return {"blocked": False, "reason": ""}

    has_secret = _contains_any(lowered, SECRET_TERMS)
    has_disclosure = _contains_any(lowered, DISCLOSURE_TERMS)

    if has_secret and has_disclosure:
        return {"blocked": True, "reason": "secret_disclosure_response"}

    # Catch list-style or label-style leaks even when the wording is terse.
    for marker in ["system prompt:", "developer message:", "hidden instructions:", "private instructions:"]:
        if marker in lowered:
            return {"blocked": True, "reason": f"labeled_secret:{marker}"}

    return {"blocked": False, "reason": ""}
