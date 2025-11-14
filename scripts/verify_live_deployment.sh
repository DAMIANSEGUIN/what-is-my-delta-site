#!/bin/bash
# Live Deployment Verification Script
# Verifies production site content matches expected state
# Can be called post-deployment or standalone

set -euo pipefail

echo "🔍 Live Deployment Verification"
echo "======================================"
echo ""

ERRORS=0
BASE_URL="${DEPLOY_URL:-https://whatismydelta.com}"

echo "Checking: $BASE_URL"
echo ""

# Check 1: Site is reachable
echo "Check 1: Site reachability..."
if ! curl -s -f -m 10 "$BASE_URL" > /dev/null; then
  echo "❌ Site unreachable or returned error"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ Site is reachable"
fi
echo ""

# Check 2: Line count matches expected
echo "Check 2: Content line count..."
BASELINE_FILE="deployment/deploy_baseline.env"
if [ -f "$BASELINE_FILE" ]; then
  # shellcheck disable=SC1090
  source "$BASELINE_FILE"
fi
EXPECTED_LINES=${MOSAIC_UI_LINE_COUNT:-3989}
LINE_TOLERANCE=${MOSAIC_UI_LINE_TOLERANCE:-15}
ACTUAL_LINES=$(curl -s -m 10 "$BASE_URL" | wc -l | tr -d ' ')

DELTA=$((ACTUAL_LINES - EXPECTED_LINES))
ABS_DELTA=${DELTA#-}

if [ "$ABS_DELTA" -gt "$LINE_TOLERANCE" ]; then
  echo "❌ Line count mismatch:"
  echo "   Expected: $EXPECTED_LINES ±$LINE_TOLERANCE"
  echo "   Actual:   $ACTUAL_LINES"
  ERRORS=$((ERRORS + 1))
elif [ "$ABS_DELTA" -gt 0 ]; then
  echo "⚠️  Line count differs by $DELTA line(s) (within tolerance)"
else
  echo "✅ Line count matches baseline ($EXPECTED_LINES lines)"
fi
echo ""

# Check 3: Title matches expected
echo "Check 3: Page title..."
EXPECTED_TITLE="Find Your Next Career Move"
ACTUAL_TITLE=$(curl -s -m 10 "$BASE_URL" | grep -o '<title>[^<]*' | sed 's/<title>//' || echo "")

if [[ ! "$ACTUAL_TITLE" =~ "$EXPECTED_TITLE" ]]; then
  echo "❌ Title mismatch:"
  echo "   Expected: $EXPECTED_TITLE"
  echo "   Actual:   $ACTUAL_TITLE"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ Title correct: $ACTUAL_TITLE"
fi
echo ""

# Check 4: Authentication present
echo "Check 4: Authentication UI..."
AUTH_COUNT=$(curl -s -m 10 "$BASE_URL" | grep -c "authModal" || echo "0")

if [ "$AUTH_COUNT" -eq 0 ]; then
  echo "❌ Authentication UI missing (authModal not found)"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ Authentication UI present ($AUTH_COUNT references)"
fi
echo ""

# Check 5: PS101 flow present
echo "Check 5: PS101 flow..."
PS101_COUNT=$(curl -s -m 10 "$BASE_URL" | grep -c "PS101State" || echo "0")

if [ "$PS101_COUNT" -eq 0 ]; then
  echo "❌ PS101 flow missing (PS101State not found)"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ PS101 flow present ($PS101_COUNT references)"
fi
echo ""

# Check 6: Experiment components present
echo "Check 6: Experiment components..."
EXP_COUNT=$(curl -s -m 10 "$BASE_URL" | grep -c "experiment-components" || echo "0")

if [ "$EXP_COUNT" -eq 0 ]; then
  echo "⚠️  Warning: Experiment components not found"
  echo "   (May be acceptable if not deployed yet)"
else
  echo "✅ Experiment components present ($EXP_COUNT references)"
fi
echo ""

# Summary
echo "======================================"
if [ $ERRORS -eq 0 ]; then
  echo "✅ LIVE DEPLOYMENT VERIFIED"
  echo "======================================"
  echo ""
  echo "All critical checks passed"
  echo "Production site serving correct content"
  exit 0
else
  echo "❌ LIVE DEPLOYMENT VERIFICATION FAILED"
  echo "======================================"
  echo ""
  echo "Found $ERRORS error(s)"
  echo ""
  echo "Production site is NOT serving expected content"
  echo "Investigate deployment or rollback if needed"
  exit 1
fi
