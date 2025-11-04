#!/bin/zsh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "⚠️  ROLLBACK SCRIPT"
echo "==================="
echo "This will:"
echo "1. Create a tag for current state"
echo "2. Reset to previous commit"
echo "3. Force push to origin"
echo "4. Redeploy to Netlify"
echo ""
read "?Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
  echo "❌ Rollback cancelled"
  exit 1
fi

TAG="pre_mosaic_cutover_$(date +%Y%m%d_%H%M%S)"
echo "📌 Creating tag: $TAG"
git tag "$TAG"

PREV=$(git rev-parse HEAD~1)
echo "⏮️  Resetting to: $PREV"
git reset --hard "$PREV"

echo "📤 Force pushing to origin..."
git push --force origin HEAD:main

echo "🌐 Redeploying to Netlify..."
netlify deploy --prod --site bb594f69-4d23-4817-b7de-dadb8b4db874 --dir mosaic_ui

echo ""
echo "✅ Rollback complete!"

