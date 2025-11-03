#!/bin/bash
# NUCLEAR_RAILWAY_RESET.sh - Last resort cache clearing
set -e

echo "🚨 NUCLEAR OPTION: Complete Railway Cache Reset"
echo "This script creates cache-busting changes and forces deployment"
echo ""

# Create unique cache-busting changes
TIMESTAMP=$(date +%s)
echo "🕐 Timestamp: $TIMESTAMP"

# Create cache-busting files
echo "# Nuclear cache bust: $TIMESTAMP" >> .railway-cache-bust
echo "RAILWAY_NUCLEAR_TIMESTAMP=$TIMESTAMP" > .env.railway

# Show what we're adding
echo "📁 Files to be committed:"
echo "  - .railway-cache-bust (cache buster)"
echo "  - .env.railway (environment timestamp)"

# Git operations
echo "📝 Adding files to git..."
git add .railway-cache-bust .env.railway

echo "💾 Committing nuclear cache bust..."
git commit -m "NUCLEAR: Force cache reset $TIMESTAMP"

echo "🚀 Pushing to Railway (force push)..."
git push origin main

echo ""
echo "✅ Nuclear cache bust deployed"
echo "⏱️  Wait 3-5 minutes, then test:"
echo "   curl https://what-is-my-delta-site-production.up.railway.app/config"
echo ""
echo "Expected: JSON with apiBase and schemaVersion (not 404)"