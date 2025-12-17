#!/bin/bash
# Railway Auto-Deploy Diagnostic Script
# Runs automated checks and provides manual steps for dashboard verification

set -e

# Change to project directory
PROJECT_DIR="/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project"
cd "$PROJECT_DIR"

echo "=================================================="
echo "Railway Auto-Deploy Diagnostic"
echo "=================================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check 1: Get expected commit from GitHub
echo "=========================================="
echo "CHECK 1: Expected Commit from GitHub"
echo "=========================================="
EXPECTED_COMMIT=$(git log origin/main --oneline -1)
EXPECTED_HASH=$(echo "$EXPECTED_COMMIT" | awk '{print $1}')
echo "Expected commit: $EXPECTED_COMMIT"
echo "Expected hash: $EXPECTED_HASH"
echo ""

# Check 2: Get currently deployed commit from Railway API
echo "=========================================="
echo "CHECK 2: Currently Deployed Code Version"
echo "=========================================="
echo "Testing production endpoint..."
DEPLOYED_TIMESTAMP=$(curl -s https://what-is-my-delta-site-production.up.railway.app/health | jq -r '.timestamp' 2>/dev/null || echo "ERROR")
if [ "$DEPLOYED_TIMESTAMP" = "ERROR" ]; then
    echo -e "${RED}❌ Cannot reach production API${NC}"
else
    echo -e "${GREEN}✅ Production API is responding${NC}"
    echo "Last restart: $DEPLOYED_TIMESTAMP"
fi
echo ""

# Check 3: Test if new endpoints exist
echo "=========================================="
echo "CHECK 3: New Endpoints Deployed?"
echo "=========================================="
echo "Checking for new ps101 endpoint..."
PS101_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://what-is-my-delta-site-production.up.railway.app/api/ps101/extract-context)
if [ "$PS101_STATUS" = "404" ]; then
    echo -e "${RED}❌ /api/ps101/extract-context NOT FOUND (new code not deployed)${NC}"
    NEW_CODE_DEPLOYED=false
else
    echo -e "${GREEN}✅ /api/ps101/extract-context exists (new code deployed)${NC}"
    NEW_CODE_DEPLOYED=true
fi
echo ""

# Check 4: Railway CLI Health
echo "=========================================="
echo "CHECK 4: Railway CLI Health"
echo "=========================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo -e "${RED}❌ Railway CLI not installed${NC}"
    RAILWAY_CLI_HEALTHY=false
else
    echo -e "${GREEN}✅ Railway CLI installed${NC}"
    railway --version

    # Check Railway CLI permissions
    if [ -f ~/.railway/version.json ]; then
        VERSION_JSON_OWNER=$(stat -f "%Su" ~/.railway/version.json 2>/dev/null || stat -c "%U" ~/.railway/version.json 2>/dev/null)
        CURRENT_USER=$(whoami)

        if [ "$VERSION_JSON_OWNER" != "$CURRENT_USER" ]; then
            echo -e "${RED}❌ ~/.railway/version.json owned by $VERSION_JSON_OWNER (should be $CURRENT_USER)${NC}"
            echo "   Fix: sudo chown $CURRENT_USER:staff ~/.railway/version.json"
            RAILWAY_CLI_HEALTHY=false
        else
            echo -e "${GREEN}✅ ~/.railway/ permissions correct${NC}"
            RAILWAY_CLI_HEALTHY=true
        fi
    else
        echo -e "${YELLOW}⚠️  ~/.railway/version.json not found${NC}"
        RAILWAY_CLI_HEALTHY=true
    fi

    # Test Railway CLI connectivity
    if railway status &> /dev/null; then
        echo -e "${GREEN}✅ Railway CLI can connect to project${NC}"
    else
        echo -e "${RED}❌ Railway CLI cannot connect (auth issue?)${NC}"
        RAILWAY_CLI_HEALTHY=false
    fi
fi
echo ""

# Check 5: Git status
echo "=========================================="
echo "CHECK 5: Git Working Tree Status"
echo "=========================================="
if git diff-index --quiet HEAD --; then
    echo -e "${GREEN}✅ Working tree is clean${NC}"
else
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    git status --short
fi
echo ""

# Summary
echo "=================================================="
echo "DIAGNOSTIC SUMMARY"
echo "=================================================="
echo ""
echo "Expected GitHub commit: $EXPECTED_HASH"
echo "New code deployed: $NEW_CODE_DEPLOYED"
echo "Railway CLI healthy: ${RAILWAY_CLI_HEALTHY:-unknown}"
echo ""

if [ "$NEW_CODE_DEPLOYED" = false ]; then
    echo -e "${RED}ISSUE CONFIRMED: Railway is not deploying latest code from GitHub${NC}"
    echo ""
    echo "Next steps require manual dashboard checks:"
    echo ""
    echo "=========================================="
    echo "MANUAL STEP 1: Check Railway Deployment Source"
    echo "=========================================="
    echo "1. Open: https://railway.app/dashboard"
    echo "2. Click project: 'wimd-career-coaching'"
    echo "3. Click service: 'what-is-my-delta-site'"
    echo "4. Click: 'Deployments' (left sidebar)"
    echo "5. Click: Most recent deployment"
    echo ""
    echo "QUESTION: Does the commit hash match $EXPECTED_HASH?"
    echo "If NO: Railway is not pulling from GitHub (integration broken)"
    echo ""
    echo "=========================================="
    echo "MANUAL STEP 2: Check Auto-Deploy Setting"
    echo "=========================================="
    echo "1. In Railway dashboard, click: 'Settings' (left sidebar)"
    echo "2. Scroll to: 'Integrations' section"
    echo "3. Find GitHub, click: 'Configure' or 'Manage'"
    echo ""
    echo "QUESTION: Is auto-deploy toggle ON (blue/enabled)?"
    echo "If NO: Toggle it ON and test with empty commit (see STEP 4)"
    echo ""
    echo "=========================================="
    echo "MANUAL STEP 3: Check GitHub Webhook"
    echo "=========================================="
    echo "1. Open: https://github.com/DAMIANSEGUIN/wimd-railway-deploy/settings/hooks"
    echo "2. Find webhook with URL containing 'railway.app'"
    echo "3. Click it, then click: 'Recent Deliveries' tab"
    echo ""
    echo "QUESTION: What is the most recent response code?"
    echo "If 4xx/5xx: Webhook is failing (need to recreate - see Fix 2 in diagnostic doc)"
    echo "If 200: Webhook working but Railway not deploying (platform issue)"
    echo ""
    echo "=========================================="
    echo "MANUAL STEP 4: Test with Empty Commit"
    echo "=========================================="
    echo "Run this to trigger a webhook test:"
    echo ""
    echo "  git commit --allow-empty -m 'test: Trigger Railway webhook'"
    echo "  git push origin main"
    echo ""
    echo "Then check:"
    echo "- GitHub webhooks (should see new delivery within 5 seconds)"
    echo "- Railway deployments (should see new deployment within 1 minute)"
    echo ""
    echo "=========================================="
    echo "WORKAROUND: Manual Deploy"
    echo "=========================================="
    echo "If you need to deploy immediately while investigating:"
    echo ""
    echo "  railway up --detach"
    echo ""
else
    echo -e "${GREEN}✅ New code is deployed - auto-deploy appears to be working${NC}"
fi

echo ""
echo "Full diagnostic documentation: RAILWAY_AUTO_DEPLOY_DIAGNOSTIC.md"
echo "=================================================="
