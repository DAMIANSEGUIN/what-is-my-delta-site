#!/bin/zsh
set -euo pipefail
NOTE="DEPLOY_STATUS_NOTE.md"
APP_URL="${1:-}"
TS="$(date '+%Y-%m-%d %H:%M:%S')" 
echo "=== Updating status note ($TS) ==="
{
  echo ""
  echo "## Status Log – $TS"
  echo ""
  if [ -x ./scripts/predeploy_sanity.sh ]; then
    echo "### Predeploy Sanity"
    ./scripts/predeploy_sanity.sh || echo "❌ Predeploy sanity failed"
    echo ""
  else
    echo "⚠️ predeploy_sanity.sh missing"
  fi
  if [ -n "$APP_URL" ] && [ -x ./scripts/verify_deploy.sh ]; then
    echo "### Deploy Smoke ($APP_URL)"
    ./scripts/verify_deploy.sh "$APP_URL" || echo "❌ Smoke test failed"
    echo ""
  else
    echo "ℹ️ Skipped smoke test (no APP_URL provided)"
  fi
  echo "---"
}
echo "✅ Status appended to $NOTE"
echo "=== Last 10 lines of $NOTE ==="
tail -n 10 "$NOTE"
