#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/mosaic_ui"
SITE_FILE="$ROOT_DIR/.netlify_site_id"

echo "=== WIMD Frontend Deploy (Netlify) ==="

if [ ! -d "$FRONTEND_DIR" ]; then
  echo "Error: Frontend directory '$FRONTEND_DIR' missing" >&2
  exit 1
fi

if ! command -v netlify >/dev/null 2>&1; then
  echo "Netlify CLI not found. Install with: npm install -g netlify-cli" >&2
  exit 1
fi

if ! netlify status >/dev/null 2>&1; then
  echo "Logging into Netlify CLI..."
  netlify login
fi

SITE_ID="${NETLIFY_SITE_ID:-}"
if [ -z "$SITE_ID" ] && [ -f "$SITE_FILE" ]; then
  SITE_ID="$(cat "$SITE_FILE")"
fi

if [ -z "$SITE_ID" ]; then
  printf "Enter your Netlify site ID or slug (leave blank to cancel): "
  read -r SITE_ID
  if [ -z "$SITE_ID" ]; then
    echo "No site ID supplied; aborting." >&2
    exit 1
  fi
  echo "$SITE_ID" > "$SITE_FILE"
fi

echo "Deploying '$FRONTEND_DIR' to Netlify site '$SITE_ID'..."
netlify deploy --dir "$FRONTEND_DIR" --prod --site "$SITE_ID"

echo "=== Frontend deploy complete ==="
