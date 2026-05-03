#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 src/call_model.py \
  --prompt "Reply briefly that the local model smoke test succeeded."
