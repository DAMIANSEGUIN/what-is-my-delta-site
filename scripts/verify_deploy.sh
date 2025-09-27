#!/bin/zsh
set -euo pipefail
API_BASE="${1:?Usage: $0 https://your-api-domain}"
fail(){ echo "[FAIL] $1"; exit 1; }
pass(){ echo "[OK] $1"; }

curl -fsS "$API_BASE/health" >/dev/null || fail "/health not 200"
pass "/health 200"

cfg=$(curl -fsS "$API_BASE/config")
echo "$cfg" | grep -E '"apiBase"|"schemaVersion"' >/dev/null || fail "/config missing fields"
pass "/config ok"

# prompts active endpoint (field existence)
act=$(curl -fsS "$API_BASE/prompts/active")
echo "$act" | grep -E '"active"' >/dev/null || fail "/prompts/active missing field"
pass "/prompts/active ok"
