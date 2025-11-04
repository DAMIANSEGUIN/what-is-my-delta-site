#!/bin/zsh
set -euo pipefail
SNIPPET="trial_mode_snippet.html"
HTMLS=( "frontend/index.html" "mosaic_ui/index.html" )
for H in $HTMLS; do
  if [ -f "$H" ]; then
    cp "$H" "$H.bak"
    if ! grep -q "ps101_trial_started_at" "$H"; then
      awk '/<\/body>/{system("cat "SNIPPET); print} !/<\/body>/{print}' "$H" > "$H.tmp" && mv "$H.tmp" "$H"
    fi
  fi
done
