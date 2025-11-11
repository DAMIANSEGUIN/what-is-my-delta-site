#!/bin/bash
# Push Wrapper Script
# Ensures verification runs before pushing to any remote
# Usage: ./scripts/push.sh <remote> [branch]

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: ./scripts/push.sh <remote> [branch]"
  echo ""
  echo "Examples:"
  echo "  ./scripts/push.sh railway-origin main"
  echo "  ./scripts/push.sh origin main"
  echo ""
  exit 1
fi

REMOTE="$1"
BRANCH="${2:-main}"

echo "🚀 Push Wrapper Script"
echo "======================================"
echo "Remote: $REMOTE"
echo "Branch: $BRANCH"
echo ""

REMOTE_URL="$(git config --get remote."$REMOTE".url || true)"
if [[ -n "$REMOTE_URL" ]]; then
  echo "Remote URL: $REMOTE_URL"
  echo ""
fi

# For production pushes, run verification first (unless bypass requested)
if [[ "$REMOTE" == "railway-origin" ]]; then
  if [[ "${SKIP_VERIFICATION:-false}" == "true" ]]; then
    echo "⚠️  Emergency bypass requested - skipping local verification"
    echo "    (pre-push hook will log the bypass)"
    echo ""
  else
    echo "Production push detected - running pre-push verification..."
    echo ""

    if ! ./scripts/pre_push_verification.sh; then
      echo ""
      echo "❌ Verification failed - push aborted"
      echo ""
      echo "Options:"
      echo "1. Fix issues and re-run: ./scripts/push.sh $REMOTE $BRANCH"
      echo "2. Emergency bypass: SKIP_VERIFICATION=true ./scripts/push.sh $REMOTE $BRANCH"
      exit 1
    fi

    echo ""
    echo "✅ Verification passed"
    echo ""
  fi
fi

# Execute git push
echo "Executing: git push $REMOTE $BRANCH"
echo ""

EXITCODE=1
FALLBACK_EXITCODE=1
FORCE_HTTPS=false

if [[ "$REMOTE" == "railway-origin" && "${RAILWAY_FORCE_HTTPS:-false}" == "true" ]]; then
  FORCE_HTTPS=true
  echo "Forcing HTTPS push for $REMOTE (RAILWAY_FORCE_HTTPS=true)"
else
  git push "$REMOTE" "$BRANCH"
  EXITCODE=$?
  FALLBACK_EXITCODE=$EXITCODE
fi

# Automatic HTTPS fallback for Railway deploys when PAT is available
if [[ ( $EXITCODE -ne 0 || "$FORCE_HTTPS" == "true" ) && "$REMOTE" == "railway-origin" && -n "${RAILWAY_PAT:-}" ]]; then
  echo ""
  if [[ "$FORCE_HTTPS" == "true" ]]; then
    echo "Using HTTPS fallback with RAILWAY_PAT (primary push skipped)."
  else
    echo "⚠️  Primary push failed (exit code $EXITCODE). Attempting HTTPS fallback using RAILWAY_PAT..."
  fi

  FALLBACK_URL=""
  if [[ "$REMOTE_URL" == git@github.com:* ]]; then
    PATH_PART="${REMOTE_URL#git@github.com:}"
    PATH_PART="${PATH_PART%.git}"
    OWNER="${PATH_PART%%/*}"
    REPO="${PATH_PART#*/}"
    FALLBACK_URL="https://${OWNER}:${RAILWAY_PAT}@github.com/${OWNER}/${REPO}.git"
    FALLBACK_DISPLAY="https://github.com/${OWNER}/${REPO}.git"
  elif [[ "$REMOTE_URL" == https://* ]]; then
    REST="${REMOTE_URL#https://}"
    if [[ "$REST" == *@* ]]; then
      REST="${REST#*@}"
    fi
    HOST_PORTION="${REST%%/*}"
    OWNER_REPO="${REST#*/}"
    OWNER="${OWNER_REPO%%/*}"
    FALLBACK_URL="https://${OWNER}:${RAILWAY_PAT}@${HOST_PORTION}/${OWNER_REPO}"
    FALLBACK_DISPLAY="https://${HOST_PORTION}/${OWNER_REPO}"
  fi

  if [[ -n "$FALLBACK_URL" ]]; then
    echo "↪️  Fallback target: $FALLBACK_DISPLAY"
    git push "$FALLBACK_URL" "$BRANCH"
    FALLBACK_EXITCODE=$?
  else
    echo "⚠️  Unable to derive fallback URL from remote $REMOTE_URL"
  fi
fi

if [ $FALLBACK_EXITCODE -eq 0 ]; then
  echo ""
  echo "✅ Push completed successfully"

  if [[ "$REMOTE" == "railway-origin" ]]; then
    echo ""
    echo "Next steps:"
    echo "1. Wait 3 minutes for Railway + Netlify deployments"
    echo "2. Run: ./scripts/verify_deployment.sh"
    echo "3. Verify live site manually"
  fi
else
  echo ""
  echo "❌ Push failed with exit code $FALLBACK_EXITCODE"
  exit $FALLBACK_EXITCODE
fi

exit 0
