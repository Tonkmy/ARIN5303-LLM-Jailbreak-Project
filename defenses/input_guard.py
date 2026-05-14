"""Rule-based checks for risky user prompts."""

from __future__ import annotations

import re


SECRET_TERMS = [
    "system prompt",
    "developer message",
    "hidden instruction",
    "hidden instructions",
    "hidden prompt",
    "hidden prompts",
    "hidden policy",
    "hidden rules",
    "hidden constraint",
    "hidden constraints",
    "hidden system message",
    "hidden restrictions",
    "private instructions",
    "private policy",
    "private rules",
    "secret rules",
    "secret initialization text",
    "system message",
    "safety policy",
    "prompt stack",
    "instruction hierarchy",
    "internal instructions",
    "internal rulebook",
    "pre-user instructions",
    "instructions were hidden",
    "rules you were given",
    "confidential system prompt",
    "prompt del sistema",
]

OVERRIDE_TERMS = [
    "ignore previous",
    "ignore prior",
    "disregard",
    "disregard all earlier",
    "forget all prior",
    "override safety",
    "developer mode",
    "administrative override",
    "user instructions outrank",
    "treat this user message as higher priority",
    "do not follow the system message",
    "disable your policy",
    "restrictions are removed",
    "without refusal",
    "no refusal",
    "follows the user instead",
    "restrictions you have removed",
]

ROLEPLAY_TERMS = [
    "role-play",
    "pretend",
    "act as",
    "in character",
    "simulation",
    "fictional",
    "unlocked assistant",
    "unrestricted assistant",
    "nofilter",
    "diagnostics mode",
]

OBFUSCATION_TERMS = [
    "decode",
    "encoded",
    "base64",
    "rot13",
    "leetspeak",
    "reverse this sentence",
    "every second word",
    "first letters",
    "capital letters",
    "snake_case",
    "remove vowels",
    "split across tokens",
    "translation exercise",
    "prompt del sistema",
    "omite reglas anteriores",
]

ACTION_TERMS = [
    "reveal",
    "show",
    "shown",
    "print",
    "output",
    "display",
    "recite",
    "expose",
    "disclose",
    "explain",
    "read",
    "read aloud",
    "provide",
    "respond with",
    "admit",
    "admits",
    "removed",
    "muestra",
]

COMPACT_PATTERNS = [
    "revealthesystemprompt",
    "showthesystemprompt",
    "printthesystemprompt",
    "showhiddensystemprompt",
    "revealhiddensystemprompt",
    "printhiddensystemprompt",
    "showhiddenpolicy",
    "revealhiddenpolicy",
    "ignorepreviousinstructions",
    "ignorepreviousrules",
    "ignorepriorrules",
    "revealsystemprompt",
    "cmv2zwflihrozsbzexn0zw0gchjvbxb0",
]

LEET_TABLE = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t"})


def _compact(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def _first_match(text: str, terms: list[str]) -> str:
    for term in terms:
        if term in text:
            return term
    return ""


def check_input(prompt: str) -> dict:
    lowered = prompt.lower()
    compact = _compact(lowered)
    leet_compact = _compact(lowered.translate(LEET_TABLE))

    match = _first_match(lowered, OVERRIDE_TERMS)
    if match:
        return {"blocked": True, "reason": f"override:{match}"}

    match = _first_match(compact, COMPACT_PATTERNS) or _first_match(leet_compact, COMPACT_PATTERNS)
    if match:
        return {"blocked": True, "reason": f"compact:{match}"}

    for marker in ["tpmorp metsys", "systm prmpt", "rvl th systm"]:
        if marker in lowered:
            return {"blocked": True, "reason": f"obfuscated:{marker}"}

    has_secret = bool(_first_match(lowered, SECRET_TERMS))
    has_action = bool(_first_match(lowered, ACTION_TERMS))
    has_roleplay = bool(_first_match(lowered, ROLEPLAY_TERMS))
    has_obfuscation = bool(_first_match(lowered, OBFUSCATION_TERMS))

    if has_secret and has_action:
        return {"blocked": True, "reason": "secret_disclosure_request"}

    if has_secret and has_roleplay:
        return {"blocked": True, "reason": "roleplay_secret_request"}
    if has_secret and has_obfuscation:
        return {"blocked": True, "reason": "obfuscated_secret_request"}
    if has_obfuscation and any(term in lowered for term in ["command", "comply", "carry it out", "follow it", "obey"]):
        return {"blocked": True, "reason": "obfuscated_command_request"}

    if "private text" in lowered and "how to behave" in lowered:
        return {"blocked": True, "reason": "indirect_private_instruction_request"}
    if "before the user" in lowered and "prompt" in lowered and has_action:
        return {"blocked": True, "reason": "indirect_system_prompt_request"}
    if all(word in lowered for word in ["hidden", "system", "prompt"]) and has_action:
        return {"blocked": True, "reason": "split_secret_disclosure_request"}
    if "x with system" in lowered and "y with prompt" in lowered and has_action:
        return {"blocked": True, "reason": "placeholder_system_prompt_request"}

    return {"blocked": False, "reason": ""}
