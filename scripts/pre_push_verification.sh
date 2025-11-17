#!/bin/bash
# Pre-Push Verification Script
# Called by pre-push hook to verify deployment readiness
# Integrates with existing verification scripts per Cursor recommendation

set -euo pipefail

echo "🔍 Running pre-push verification..."
echo ""

ERRORS=0

# Step 0: CRITICAL - Verify recent backup exists (within 1 hour)
echo "Step 0: Backup verification (rollback protection)..."
ONE_HOUR_AGO=$(date -u -v-1H +%Y%m%d_%H%M%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y%m%d_%H%M%SZ 2>/dev/null)
BACKUP_FOUND=0

if [ -d "backups" ]; then
  # Find backups from the last hour
  while IFS= read -r backup; do
    BACKUP_TIME=$(basename "$backup" | sed 's/site-backup_//' | sed 's/.zip//')
    if [[ "$BACKUP_TIME" > "$ONE_HOUR_AGO" ]]; then
      LATEST_BACKUP="$backup"
      BACKUP_FOUND=1
      break
    fi
  done < <(ls -t backups/site-backup_*.zip 2>/dev/null || true)
fi

if [ $BACKUP_FOUND -eq 0 ]; then
  echo "❌ NO RECENT BACKUP FOUND (required within last hour)"
  echo ""
  echo "CRITICAL: Create backup before deployment for rollback capability"
  echo ""
  echo "Run: ./scripts/create_site_backup.sh"
  echo ""
  echo "Why this matters:"
  echo "  - Provides rollback point if deployment fails"
  echo "  - Preserves working state before changes"
  echo "  - Required by deployment safety protocol"
  echo ""
  ERRORS=$((ERRORS + 1))
else
  BACKUP_SIZE=$(ls -lh "$LATEST_BACKUP" | awk '{print $5}')
  BACKUP_AGE=$(basename "$LATEST_BACKUP" | sed 's/site-backup_//' | sed 's/.zip//')
  echo "✅ Recent backup found: $(basename $LATEST_BACKUP) ($BACKUP_SIZE)"
  echo "   Created: $BACKUP_AGE"
fi
echo ""

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
  BASELINE_FILE="deployment/deploy_baseline.env"
  if [ -f "$BASELINE_FILE" ]; then
    # shellcheck disable=SC1090
    source "$BASELINE_FILE"
  fi
  EXPECTED_LINES=${MOSAIC_UI_LINE_COUNT:-3989}
  LINE_TOLERANCE=${MOSAIC_UI_LINE_TOLERANCE:-15}
  DELTA=$((ACTUAL_LINES - EXPECTED_LINES))
  ABS_DELTA=${DELTA#-}

  if [ "$ABS_DELTA" -gt "$LINE_TOLERANCE" ]; then
    echo "❌ Content line count outside expected bounds"
    echo "   Expected: $EXPECTED_LINES ±$LINE_TOLERANCE"
    echo "   Actual:   $ACTUAL_LINES"
    echo "   Update deployment/deploy_baseline.env if the change is intentional."
    ERRORS=$((ERRORS + 1))
  elif [ "$ABS_DELTA" -gt 0 ]; then
    echo "⚠️  Line count differs by $DELTA line(s) (within tolerance)"
  else
    echo "✅ Content line count within expected bounds ($EXPECTED_LINES lines)"
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
