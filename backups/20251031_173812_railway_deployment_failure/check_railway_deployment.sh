#!/bin/bash
# Railway Deployment Status Checker
# Run this to see current deployment status and recent logs

echo "======================================"
echo "Railway Deployment Status Check"
echo "======================================"
echo ""

echo "1. Checking Railway service status..."
railway status
echo ""

echo "======================================"
echo "2. Recent deployment activity..."
echo "======================================"
railway service
echo ""

echo "======================================"
echo "3. Latest deployment logs (last 100 lines)..."
echo "======================================"
railway logs --deployment latest | tail -100
echo ""

echo "======================================"
echo "4. Checking if backend is responding..."
echo "======================================"
echo "Health endpoint test:"
curl -s https://what-is-my-delta-site-production.up.railway.app/health || echo "Health check FAILED - service not responding"
echo ""
echo ""

echo "======================================"
echo "Summary:"
echo "======================================"
echo "If you see errors above, share the full output."
echo "If health check returns JSON with 'ok: true', deployment succeeded!"
echo ""
