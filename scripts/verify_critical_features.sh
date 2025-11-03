#!/bin/bash
# Automated critical feature verification

ERRORS=0

echo "🔍 Verifying critical features..."

# 1. Authentication UI Check
echo "Checking authentication UI..."
AUTH_COUNT=0
for file in frontend/index.html mosaic_ui/index.html; do
  if [[ -f "$file" ]]; then
    COUNT=$(grep -c "authModal\|LOGIN/REGISTER MODAL\|loginForm" "$file" 2>/dev/null || echo 0)
    COUNT=$(echo "$COUNT" | tr -d '\n')
    AUTH_COUNT=$((AUTH_COUNT + COUNT))
  fi
done

if [[ $AUTH_COUNT -eq 0 ]]; then
  echo "❌ CRITICAL: Authentication UI missing"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ Authentication UI present ($AUTH_COUNT occurrences)"
fi

# 2. PS101 Flow Check
echo "Checking PS101 flow..."
PS101_COUNT=0
for file in frontend/index.html mosaic_ui/index.html; do
  if [[ -f "$file" ]]; then
    COUNT=$(grep -c "PS101State\|ps101-" "$file" 2>/dev/null || echo 0)
    COUNT=$(echo "$COUNT" | tr -d '\n')
    PS101_COUNT=$((PS101_COUNT + COUNT))
  fi
done

if [[ $PS101_COUNT -eq 0 ]]; then
  echo "❌ CRITICAL: PS101 flow missing"
  ERRORS=$((ERRORS + 1))
else
  echo "✅ PS101 flow present ($PS101_COUNT references)"
fi

# 3. API Configuration Check
echo "Checking API_BASE configuration..."
API_BASE_CORRECT=0
for file in frontend/index.html mosaic_ui/index.html; do
  if [[ -f "$file" ]]; then
    if grep -q "API_BASE = ''" "$file" 2>/dev/null; then
      API_BASE_CORRECT=1
    fi
  fi
done

if [[ $API_BASE_CORRECT -eq 0 ]]; then
  echo "⚠️  WARNING: API_BASE may not be using relative paths"
else
  echo "✅ API_BASE configured correctly"
fi

# 4. Production Smoke Test (if curl available)
if command -v curl &> /dev/null; then
  echo "Checking production site..."
  PROD_AUTH=$(curl -s -m 5 https://whatismydelta.com/ 2>/dev/null | grep -c "authModal\|loginForm" || echo 0)
  PROD_AUTH=$(echo "$PROD_AUTH" | tr -d '\n')

  if [[ $PROD_AUTH -eq 0 ]]; then
    echo "⚠️  WARNING: Production site may be missing authentication (or unreachable)"
  else
    echo "✅ Production authentication detected"
  fi
fi

# Exit with error count
echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "💥 $ERRORS critical feature(s) missing"
  echo "🚨 BLOCKING: Fix required before proceeding"
  exit 1
else
  echo "✅ All critical features verified"
  exit 0
fi
