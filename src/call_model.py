"""Minimal local API caller scaffold.

The project lead should adapt this file to the exact local API settings.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


def load_config(path: str = "configs/model_api.json") -> Dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        config_path = Path("configs/model_api.example.json")
    return json.loads(config_path.read_text())


def build_messages(user_prompt: str, system_prompt: str) -> List[Dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def call_model(user_prompt: str) -> str:
    cfg = load_config()
    if OpenAI is None:
        raise RuntimeError("Install the openai package before using call_model.py")

    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])
    response = client.chat.completions.create(
        model=cfg["model"],
        messages=build_messages(user_prompt, cfg["system_prompt"]),
        temperature=cfg["temperature"],
        max_tokens=cfg["max_tokens"],
    )
    return response.choices[0].message.content or ""
