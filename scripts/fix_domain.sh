#!/bin/zsh
set -euo pipefail

# WIMD Domain Fix - Simple Approach
echo "=== WIMD Domain Fix ==="
echo "The domain is already configured with Netlify"
echo "We need to update Netlify DNS to point to Railway"

echo ""
echo "Step 1: Update Netlify DNS"
echo "1. Go to Netlify DNS panel"
echo "2. Remove existing NETLIFY records"
echo "3. Add CNAME record:"
echo "   Type: CNAME"
echo "   Name: @"
echo "   Value: what-is-my-delta-site-production.up.railway.app"
echo "   TTL: 3600"

echo ""
echo "Step 2: Add WWW record (optional)"
echo "   Type: CNAME"
echo "   Name: www"
echo "   Value: what-is-my-delta-site-production.up.railway.app"
echo "   TTL: 3600"

echo ""
echo "Step 3: Test domains"
echo "Wait 1-2 hours for DNS propagation, then test:"
echo "curl https://whatismydelta.com/health"
echo "curl https://www.whatismydelta.com/health"

echo ""
echo "=== Manual DNS Update Required ==="
echo "Update Netlify DNS first, then Railway will work automatically"

