#!/bin/bash
# Verify deployment succeeded and critical features still work

echo "=== WIMD Deployment Verification ==="
echo ""

# Check health endpoint
echo "Checking health endpoint..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" https://whatismydelta.com/health)
if [ "$HEALTH" = "200" ]; then
  echo "✅ Health endpoint: OK"
else
  echo "❌ Health endpoint: FAILED (HTTP $HEALTH)"
  exit 1
fi

# Check config endpoint
echo "Checking config endpoint..."
CONFIG=$(curl -s -o /dev/null -w "%{http_code}" https://whatismydelta.com/config)
if [ "$CONFIG" = "200" ]; then
  echo "✅ Config endpoint: OK"
else
  echo "❌ Config endpoint: FAILED (HTTP $CONFIG)"
  exit 1
fi

# Check frontend loads
echo "Checking frontend..."
FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" https://whatismydelta.com/)
if [ "$FRONTEND" = "200" ]; then
  echo "✅ Frontend: OK"
else
  echo "❌ Frontend: FAILED (HTTP $FRONTEND)"
  exit 1
fi

# Check critical files exist
echo "Checking critical files..."
test -f frontend/index.html && echo "✅ index.html exists" || echo "❌ index.html MISSING"
test -f frontend/netlify.toml && echo "✅ netlify.toml exists" || echo "❌ netlify.toml MISSING"
test -f package.json && echo "✅ package.json exists" || echo "❌ package.json MISSING"

echo ""
echo "=== Verification Complete ==="
echo "All checks must pass before proceeding with more changes."
