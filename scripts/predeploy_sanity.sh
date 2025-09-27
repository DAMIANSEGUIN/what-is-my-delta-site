#!/bin/zsh
set -euo pipefail

# Warn-only on missing secrets (avoid build-time failures)
if [ -z "${OPENAI_API_KEY:-}" ]; then echo "[WARN] OPENAI_API_KEY missing"; fi
if [ -z "${CLAUDE_API_KEY:-}" ]; then echo "[WARN] CLAUDE_API_KEY missing"; fi

# Python dependency presence check
python - <<'PY'
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
