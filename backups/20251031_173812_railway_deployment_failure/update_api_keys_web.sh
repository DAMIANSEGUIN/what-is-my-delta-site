#!/bin/bash
set -e

echo "🔑 API Key Rotation Script (Web Dashboard Method)"
echo "================================================="
echo ""

# Prompt for new OpenAI API key
echo "Enter your NEW OpenAI API key (starts with sk-proj- or sk-):"
read -r NEW_OPENAI_KEY

if [[ ! "$NEW_OPENAI_KEY" =~ ^sk- ]]; then
    echo "❌ Error: OpenAI API key should start with 'sk-'"
    exit 1
fi

# Prompt for new Claude API key
echo ""
echo "Enter your NEW Claude API key (starts with sk-ant-):"
read -r NEW_CLAUDE_KEY

if [[ ! "$NEW_CLAUDE_KEY" =~ ^sk-ant- ]]; then
    echo "❌ Error: Claude API key should start with 'sk-ant-'"
    exit 1
fi

echo ""
echo "📋 Your new API keys:"
echo "OPENAI_API_KEY: ${NEW_OPENAI_KEY:0:20}..."
echo "CLAUDE_API_KEY: ${NEW_CLAUDE_KEY:0:20}..."
echo ""

echo "🌐 MANUAL STEPS - Update in Railway Dashboard:"
echo "=============================================="
echo "1. Go to: https://railway.app/project/what-is-my-delta-site-production"
echo "2. Click on your service: what-is-my-delta-site-production"
echo "3. Go to the 'Variables' tab"
echo "4. Update these variables:"
echo ""
echo "   Variable Name: OPENAI_API_KEY"
echo "   Value: $NEW_OPENAI_KEY"
echo ""
echo "   Variable Name: CLAUDE_API_KEY"
echo "   Value: $NEW_CLAUDE_KEY"
echo ""
echo "5. Railway will automatically redeploy after you save"
echo ""

# Update local .env file
echo "📁 Updating local .env file..."
cat > .env << EOF
OPENAI_API_KEY=$NEW_OPENAI_KEY
CLAUDE_API_KEY=$NEW_CLAUDE_KEY
PUBLIC_SITE_ORIGIN=https://whatismydelta.com
APP_SCHEMA_VERSION=v1
EOF

echo "✅ Local .env file updated!"
echo ""
echo "⏱️  After updating Railway dashboard (steps above):"
echo "Wait 2-3 minutes for deployment, then test:"
echo "curl https://what-is-my-delta-site-production.up.railway.app/config"
echo ""
echo "🔐 Don't forget to revoke the old API keys in:"
echo "- OpenAI Dashboard: https://platform.openai.com/api-keys"
echo "- Claude Dashboard: https://console.anthropic.com/settings/keys"