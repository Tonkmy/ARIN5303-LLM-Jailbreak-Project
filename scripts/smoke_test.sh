#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
python3 src/call_model.py >/dev/null 2>&1 || true
echo "Use this script as a placeholder for lead-side smoke tests."
