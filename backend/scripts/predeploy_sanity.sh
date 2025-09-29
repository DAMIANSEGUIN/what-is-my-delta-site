#!/bin/zsh
set -euo pipefail
[ -z "${OPENAI_API_KEY:-}" ] && { echo "OPENAI_API_KEY missing"; exit 1; }
[ -z "${CLAUDE_API_KEY:-}" ] && { echo "CLAUDE_API_KEY missing"; exit 1; }
[ -n "${PROMPTS_CSV_PATH:-}" ] && ./scripts/check_prompts.sh "$PROMPTS_CSV_PATH" || true
echo "[OK] predeploy sanity passed"
