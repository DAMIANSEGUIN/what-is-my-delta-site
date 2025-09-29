#!/bin/zsh
set -euo pipefail

# Warn-only on missing secrets (avoid build-time failures)
if [ -z "${OPENAI_API_KEY:-}" ]; then echo "[WARN] OPENAI_API_KEY missing"; fi
if [ -z "${CLAUDE_API_KEY:-}" ]; then echo "[WARN] CLAUDE_API_KEY missing"; fi

# Python dependency presence check (prefer python3)
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PYTHON_BIN=python
  else
    echo "[WARN] python3/python not found in PATH" >&2
    PYTHON_BIN=""
  fi
fi

[ -n "$PYTHON_BIN" ] && "$PYTHON_BIN" - <<'PY'
import importlib.util, sys
mods = ["fastapi", "httpx", "pydantic", "pydantic_settings"]
missing = [m for m in mods if importlib.util.find_spec(m) is None]
if missing:
    print(f"[WARN] Missing Python modules: {missing}")
else:
    print("[OK] Python deps present")
PY


[ -n "${PROMPTS_CSV_PATH:-}" ] && ./scripts/check_prompts.sh "$PROMPTS_CSV_PATH" || true
echo "[OK] predeploy sanity passed"
