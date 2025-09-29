#!/bin/bash
set -e

echo "🔧 Fixing Railway deployment..."

# Add correct remote
git remote add origin https://github.com/DAMIANSEGUIN/what-is-my-delta-site.git

# Fix Procfile
cat > Procfile << 'EOF'
web: python -m uvicorn api.index:app --host 0.0.0.0 --port $PORT --workers 1 --timeout-keep-alive 120
EOF

# Commit and push
git add Procfile
git commit -m "Fix Procfile to point to api.index:app"
git push origin main --force

echo "✅ Deployment fix pushed to Railway"
echo "⏱️  Wait 2-3 minutes for Railway to redeploy"
echo "🧪 Then test: curl https://what-is-my-delta-site-production.up.railway.app/config"