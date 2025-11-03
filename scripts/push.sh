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

git push "$REMOTE" "$BRANCH"

EXITCODE=$?

if [ $EXITCODE -eq 0 ]; then
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
  echo "❌ Push failed with exit code $EXITCODE"
fi

exit $EXITCODE
