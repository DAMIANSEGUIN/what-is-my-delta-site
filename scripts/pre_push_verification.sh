#!/bin/bash
# Pre-Push Verification Script
# Called by pre-push hook to verify deployment readiness
# Integrates with existing verification scripts per Cursor recommendation

set -euo pipefail

echo "🔍 Running pre-push verification..."
echo ""

ERRORS=0

# Step 1: Run existing predeploy sanity checks
echo "Step 1: Pre-deployment sanity checks..."
if [ -f "./scripts/predeploy_sanity.sh" ]; then
  if ! ./scripts/predeploy_sanity.sh; then
    echo "❌ Pre-deployment sanity checks failed"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Pre-deployment sanity checks passed"
  fi
else
  echo "⚠️  Warning: predeploy_sanity.sh not found, skipping"
fi
echo ""

# Step 2: Verify critical features locally
echo "Step 2: Critical features verification..."
if [ -f "./scripts/verify_critical_features.sh" ]; then
  if ! ./scripts/verify_critical_features.sh; then
    echo "❌ Critical features verification failed"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Critical features verified"
  fi
else
  echo "❌ verify_critical_features.sh not found"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Step 3: Check git status is clean
echo "Step 3: Git status check..."
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Uncommitted changes detected"
  echo "Run: git status"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ Git working tree clean"
fi
echo ""

# Step 4: Verify expected content (mosaic_ui/index.html)
echo "Step 4: Content verification..."
if [ -f "mosaic_ui/index.html" ]; then
  ACTUAL_LINES=$(wc -l mosaic_ui/index.html | awk '{print $1}')
  EXPECTED_LINES=3427

  if [ "$ACTUAL_LINES" != "$EXPECTED_LINES" ]; then
    echo "⚠️  Warning: Line count mismatch"
    echo "   Expected: $EXPECTED_LINES"
    echo "   Actual:   $ACTUAL_LINES"
    echo "   This may indicate missing content"
    # Don't fail on this - just warn
  else
    echo "✅ Content line count matches expected ($EXPECTED_LINES lines)"
  fi

  # Check for critical features in content
  if ! grep -q "authModal" mosaic_ui/index.html; then
    echo "❌ Authentication UI missing from mosaic_ui/index.html"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ Authentication UI present"
  fi

  if ! grep -q "PS101State" mosaic_ui/index.html; then
    echo "❌ PS101 flow missing from mosaic_ui/index.html"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ PS101 flow present"
  fi
else
  echo "❌ mosaic_ui/index.html not found"
  ERRORS=$((ERRORS + 1))
fi
echo ""

# Summary
echo "======================================"
if [ $ERRORS -eq 0 ]; then
  echo "✅ PRE-PUSH VERIFICATION PASSED"
  echo "======================================"
  echo ""
  echo "Safe to push to production"
  exit 0
else
  echo "❌ PRE-PUSH VERIFICATION FAILED"
  echo "======================================"
  echo ""
  echo "Found $ERRORS error(s)"
  echo ""
  echo "Fix the issues above before pushing to production"
  echo "Or use emergency bypass: SKIP_VERIFICATION=true git push ..."
  echo "(Bypass will be logged to .verification_audit.log)"
  exit 1
fi
