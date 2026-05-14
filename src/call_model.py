from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def load_config(path: str = "configs/model_api.json") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file: {config_path}")
    return json.loads(config_path.read_text())


def build_messages(prompt: str, system_prompt: str) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]


def call_model(
    prompt: str,
    config_path: str = "configs/model_api.json",
    max_tokens: int | None = None,
) -> str:
    cfg = load_config(config_path)

    endpoint = cfg["base_url"].rstrip("/") + "/chat/completions"
    payload = {
        "model": cfg["model"],
        "messages": build_messages(prompt, cfg["system_prompt"]),
        "temperature": cfg["temperature"],
        "max_tokens": max_tokens or cfg["max_tokens"],
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {cfg['api_key']}",
    }

    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=cfg["timeout_seconds"]) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Model API returned HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach model API at {endpoint}: {exc}") from exc

    return data["choices"][0]["message"].get("content", "")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", default="Reply with a short smoke-test confirmation.")
    parser.add_argument("--config", default="configs/model_api.json")
    parser.add_argument("--max-tokens", type=int)
    args = parser.parse_args()

    print(call_model(args.prompt, args.config, args.max_tokens).strip())


if __name__ == "__main__":
    main()
