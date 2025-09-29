#!/bin/bash
set -e

echo "🔑 API Key Rotation Script"
echo "=========================="
echo ""

# Navigate to project directory
cd "/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project"

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
echo "🚀 Updating Railway environment variables..."

# Update Railway variables
railway variables set "OPENAI_API_KEY=$NEW_OPENAI_KEY"
railway variables set "CLAUDE_API_KEY=$NEW_CLAUDE_KEY"

echo ""
echo "📋 Current Railway variables:"
railway variables

echo ""
echo "🔄 Triggering Railway redeploy..."
railway redeploy

echo ""
echo "✅ API keys updated successfully!"
echo "🔗 Check deployment status at: https://railway.app"
echo ""
echo "⏱️  Wait 2-3 minutes for deployment, then test:"
echo "curl https://what-is-my-delta-site-production.up.railway.app/config"