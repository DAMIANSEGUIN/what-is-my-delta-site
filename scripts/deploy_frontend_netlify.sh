#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
# Default to PS101-compliant mosaic UI; allow override via NETLIFY_DEPLOY_DIR
SITE_FILE="$ROOT_DIR/.netlify_site_id"
DEPLOY_DIR="${NETLIFY_DEPLOY_DIR:-$ROOT_DIR/mosaic_ui}"

if [ ! -d "$DEPLOY_DIR" ] && [ -d "$ROOT_DIR/frontend" ]; then
  echo "⚠️  Directory '$DEPLOY_DIR' not found; falling back to legacy frontend/"
  DEPLOY_DIR="$ROOT_DIR/frontend"
fi

if [ ! -d "$DEPLOY_DIR" ]; then
  echo "Error: Deploy directory '$DEPLOY_DIR' missing" >&2
  exit 1
fi

echo "=== WIMD Frontend Deploy (Netlify) ==="
echo "Using deploy directory: $DEPLOY_DIR"

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

echo "Deploying '$DEPLOY_DIR' to Netlify site '$SITE_ID'..."

STAGING_DIR="$(mktemp -d "${TMPDIR:-/tmp}/wimd_netlify_XXXXXX")"
cleanup() {
  rm -rf "$STAGING_DIR"
}
trap cleanup EXIT INT TERM

echo "Creating staging artefact at: $STAGING_DIR"
if command -v rsync >/dev/null 2>&1; then
  rsync -a "$DEPLOY_DIR"/ "$STAGING_DIR"/
else
  cp -R "$DEPLOY_DIR"/. "$STAGING_DIR"/
fi

INJECT_SCRIPT="$ROOT_DIR/Mosaic/PS101_Continuity_Kit/inject_build_id.js"
if [ -f "$INJECT_SCRIPT" ] && command -v node >/dev/null 2>&1; then
  echo "Stamping BUILD_ID into staging artefact..."
  (cd "$ROOT_DIR" && BUILD_ID_TARGET_ROOT="$STAGING_DIR" BUILD_ID_TARGETS="index.html" node "$INJECT_SCRIPT")
else
  echo "⚠️  BUILD_ID injection skipped (missing script or node.js)"
fi

netlify deploy --dir "$STAGING_DIR" --prod --site "$SITE_ID"

echo "=== Frontend deploy complete ==="
