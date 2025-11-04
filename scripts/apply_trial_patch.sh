#!/bin/zsh
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SNIPPET="$REPO_ROOT/Mosaic/PS101_Continuity_Kit/trial_mode_snippet.html"
HTMLS=( "$REPO_ROOT/frontend/index.html" "$REPO_ROOT/mosaic_ui/index.html" )

if [ ! -f "$SNIPPET" ]; then
  echo "❌ Snippet not found: $SNIPPET"
  exit 1
fi

for H in $HTMLS; do
  if [ -f "$H" ]; then
    echo "Processing: $H"
    cp "$H" "$H.bak"
    if ! grep -q "ps101_trial_started_at" "$H"; then
      awk -v snippet="$SNIPPET" '/<\/body>/{system("cat \"" snippet "\""); print} !/<\/body>/{print}' "$H" > "$H.tmp" && mv "$H.tmp" "$H"
      echo "✅ Trial mode snippet injected into $H"
    else
      echo "ℹ️  Trial mode already present in $H, skipping"
    fi
  else
    echo "⚠️  File not found: $H"
  fi
done

