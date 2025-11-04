#!/bin/zsh
set -euo pipefail
SITE="https://whatismydelta.com"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$SITE")
if [ "$STATUS" != "200" ]; then echo "ERROR: $SITE returned $STATUS"; exit 1; fi
HTML=$(curl -s "$SITE")
if ! echo "$HTML" | grep -q "BUILD_ID"; then echo "WARN: BUILD_ID comment not found in HTML"; fi
if echo "$HTML" | grep -qi "id=\"authModal\"" && echo "$HTML" | grep -qi "ps101_trial_started_at"; then echo "OK: Trial snippet present and authModal referenced"; else echo "WARN: Could not confirm trial snippet or authModal"; fi
if echo "$HTML" | grep -qi "Service-Worker"; then echo "NOTE: Service worker references detected; consider version-bump"; fi
echo "Verification completed. Manually confirm no login wall in Incognito and that ?forceLogin=1 toggles it."
