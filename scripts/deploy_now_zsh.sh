#!/bin/zsh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "🚀 Deploy Now - One-Step Deploy Script"
echo "========================================"
echo ""

# Add files
echo "📦 Staging files..."
git add docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md \
        scripts/verify_mosaic_ui.sh \
        frontend/index.html \
        mosaic_ui/index.html \
        netlify.toml || true

# Commit (allow failure if nothing to commit)
echo "📝 Committing..."
git commit -m "PS101 Mosaic: trial-mode init, guardrails doc, verify script, base/publish=mosaic_ui" || echo "ℹ️  No changes to commit"

# Deployment gate
echo ""
echo "🛡️  Enforcing deployment gate..."
./scripts/run_deploy_gate.sh

# Push
echo "📤 Pushing to origin main..."
git push origin main

# Deploy to Netlify
echo "🌐 Deploying to Netlify production..."
NETLIFY_SITE_ID="bb594f69-4d23-4817-b7de-dadb8b4db874" NETLIFY_DEPLOY_DIR="mosaic_ui" ./scripts/deploy_frontend_netlify.sh

# Post-deploy verification
echo ""
echo "🔎 Running live deployment verification..."
if ! ./scripts/verify_live_deployment.sh; then
  echo ""
  echo "❌ Live verification failed. Investigate immediately."
  exit 1
fi

echo ""
echo "✅ Deploy complete!"

