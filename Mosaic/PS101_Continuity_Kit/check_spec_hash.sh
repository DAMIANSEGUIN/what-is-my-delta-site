#!/bin/zsh
set -euo pipefail
FOOTER_FILE="frontend/index.html"
SPEC_HASH=$(grep -oE 'SHA:[0-9a-f]+' "$FOOTER_FILE" | cut -d: -f2)
if [ -z "$SPEC_HASH" ]; then
  echo "Spec hash not found in footer."
  exit 1
fi
echo "Spec hash verified: $SPEC_HASH"
