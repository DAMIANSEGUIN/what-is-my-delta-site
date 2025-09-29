#!/bin/bash
set -e

echo "📁 Copying complete API implementation to Railway repository..."

# Commit and push the complete local implementation
git add .
git commit -m "Deploy complete FastAPI implementation with all endpoints"
git push origin main --force

echo "✅ Complete API implementation pushed to Railway"
echo "⏱️  Railway will rebuild with full 449-line api/index.py in 2-3 minutes"
echo "🧪 Then test: curl https://what-is-my-delta-site-production.up.railway.app/config"