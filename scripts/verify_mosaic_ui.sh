#!/bin/bash
# Mosaic Deploy Safeguard – live site verification helper
# Usage: ./scripts/verify_mosaic_ui.sh [url]

set -euo pipefail

URL="${1:-https://whatismydelta.com/}"
EXPECTED_LINES=3875
TMP_FILE="$(mktemp)"

echo "=== Mosaic UI Verification ==="
echo "Target URL: $URL"
echo ""

echo "Fetching live HTML..."
if ! curl -sS "$URL" -o "$TMP_FILE"; then
  echo "❌ Failed to fetch $URL"
  rm -f "$TMP_FILE"
  exit 1
fi

LINE_COUNT="$(wc -l < "$TMP_FILE" | tr -d ' ')"
echo "Line count: $LINE_COUNT"
if [ "$LINE_COUNT" != "$EXPECTED_LINES" ]; then
  echo "⚠️  Expected $EXPECTED_LINES lines; investigate potential mismatch."
else
  echo "✅ Line count matches expected Mosaic UI footprint."
fi

if grep -q "authModal" "$TMP_FILE"; then
  echo "✅ Authentication modal markup detected."
else
  echo "❌ Authentication modal missing – legacy UI likely served."
fi

if grep -q "PS101State" "$TMP_FILE"; then
  echo "✅ PS101 state manager detected."
else
  echo "❌ PS101 state manager missing – legacy UI likely served."
fi

if FOOTER=$(grep -o "<!-- BUILD_ID:[^>]* -->" "$TMP_FILE"); then
  echo "Live BUILD_ID: $FOOTER"
else
  echo "⚠️  BUILD_ID comment not found."
fi

rm -f "$TMP_FILE"
echo ""
echo "Run complete."
