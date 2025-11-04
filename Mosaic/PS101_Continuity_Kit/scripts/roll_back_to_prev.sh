#!/bin/zsh
set -euo pipefail
TAG="pre_mosaic_cutover_$(date +%Y%m%d_%H%M%S)"
git tag "$TAG"
PREV=$(git rev-parse HEAD~1)
git reset --hard "$PREV"
git push --force origin HEAD:main
netlify deploy --prod --site bb594f69-4d23-4817-b7de-dadb8b4db874 --dir mosaic_ui
