#!/bin/bash
# Update Netlify publish directory to mosaic_ui

set -e

echo "=== Updating Netlify Publish Directory ==="
echo ""

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found"
    echo "Install with: npm install -g netlify-cli"
    exit 1
fi

echo "✅ Netlify CLI found"

# Check if logged in
if ! netlify status &> /dev/null; then
    echo "⚠️  Not logged in to Netlify"
    echo "Running: netlify login"
    netlify login
fi

# Get site ID from .netlify_site_id or prompt
SITE_ID="${NETLIFY_SITE_ID:-}"
if [ -z "$SITE_ID" ] && [ -f ".netlify_site_id" ]; then
    SITE_ID="$(cat .netlify_site_id)"
fi

if [ -z "$SITE_ID" ]; then
    echo ""
    echo "Please provide your Netlify site ID:"
    read -r SITE_ID
    echo "$SITE_ID" > .netlify_site_id
fi

echo "Using site ID: $SITE_ID"
echo ""

# Update build settings
echo "Updating publish directory to 'mosaic_ui'..."
netlify api updateSite --data "{
  \"build_settings\": {
    \"base\": \"mosaic_ui\",
    \"dir\": \"mosaic_ui\",
    \"cmd\": \"\"
  }
}" --site-id "$SITE_ID"

echo ""
echo "✅ Publish directory updated!"
echo ""
echo "Next steps:"
echo "1. Trigger a new deploy: netlify deploy --prod --dir=mosaic_ui"
echo "2. Or push a new commit to trigger auto-deploy"
echo ""
echo "Verify in dashboard: https://app.netlify.com/sites/$SITE_ID/configuration/deploys"


