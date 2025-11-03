#!/bin/bash
# Deployment Wrapper Script
# Orchestrates deployment with pre/post verification
# Usage: ./scripts/deploy.sh <railway|netlify|all>

set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: ./scripts/deploy.sh <railway|netlify|all>"
  echo ""
  echo "Examples:"
  echo "  ./scripts/deploy.sh netlify   # Deploy frontend only"
  echo "  ./scripts/deploy.sh railway   # Deploy backend only"
  echo "  ./scripts/deploy.sh all       # Deploy both"
  echo ""
  exit 1
fi

TARGET="$1"

echo "🚀 Deployment Wrapper Script"
echo "======================================"
echo "Target: $TARGET"
echo ""

# Pre-deployment verification
echo "Step 1: Pre-deployment verification..."
echo ""

if ! ./scripts/pre_push_verification.sh; then
  echo ""
  echo "❌ Pre-deployment verification failed"
  echo "Fix issues before deploying"
  exit 1
fi

echo ""
echo "✅ Pre-deployment verification passed"
echo ""

# Deploy based on target
case "$TARGET" in
  netlify)
    echo "Step 2: Deploying to Netlify..."
    echo ""

    # Use existing Netlify deployment script per Cursor recommendation
    if [ -f "./scripts/deploy_frontend_netlify.sh" ]; then
      ./scripts/deploy_frontend_netlify.sh
    else
      echo "⚠️  deploy_frontend_netlify.sh not found, using netlify deploy directly"
      netlify deploy --prod --dir=mosaic_ui
    fi

    DEPLOY_EXIT=$?

    if [ $DEPLOY_EXIT -ne 0 ]; then
      echo ""
      echo "❌ Netlify deployment failed"
      exit $DEPLOY_EXIT
    fi

    echo ""
    echo "✅ Netlify deployment command completed"
    echo ""

    # Wait for propagation
    echo "Step 3: Waiting 60 seconds for CDN propagation..."
    sleep 60
    echo ""

    # Post-deployment verification
    echo "Step 4: Verifying live deployment..."
    echo ""

    if [ -f "./scripts/verify_deployment.sh" ]; then
      ./scripts/verify_deployment.sh
    else
      echo "⚠️  verify_deployment.sh not found - manual verification required"
    fi

    echo ""
    echo "======================================"
    echo "✅ NETLIFY DEPLOYMENT COMPLETE"
    echo "======================================"
    echo ""
    echo "Live URL: https://whatismydelta.com/"
    ;;

  railway)
    echo "Step 2: Deploying to Railway..."
    echo ""
    echo "Railway deployment uses git push to railway-origin"
    echo ""

    # Use push wrapper which will trigger pre-push hook
    ./scripts/push.sh railway-origin main

    echo ""
    echo "======================================"
    echo "✅ RAILWAY DEPLOYMENT INITIATED"
    echo "======================================"
    echo ""
    echo "Railway will rebuild backend (~2 minutes)"
    echo ""
    echo "Monitor at: https://railway.app/dashboard"
    ;;

  all)
    echo "Deploying both Railway and Netlify..."
    echo ""

    # Deploy Railway first (backend)
    ./scripts/deploy.sh railway

    echo ""
    echo "Waiting 2 minutes for Railway backend rebuild..."
    sleep 120
    echo ""

    # Then deploy Netlify (frontend)
    ./scripts/deploy.sh netlify

    echo ""
    echo "======================================"
    echo "✅ FULL DEPLOYMENT COMPLETE"
    echo "======================================"
    ;;

  *)
    echo "❌ Invalid target: $TARGET"
    echo "Valid options: railway, netlify, all"
    exit 1
    ;;
esac

echo ""
echo "Deployment logs available in .verification_audit.log"
