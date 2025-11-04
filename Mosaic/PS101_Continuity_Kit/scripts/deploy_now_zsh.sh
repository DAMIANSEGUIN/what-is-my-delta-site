#!/bin/zsh
set -euo pipefail
git add docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md scripts/verify_mosaic_ui.sh frontend/index.html mosaic_ui/index.html netlify.toml
git commit -m "PS101 Mosaic: trial-mode init, guardrails doc, verify script, base/publish=mosaic_ui" || true
git push origin main
netlify deploy --prod --site bb594f69-4d23-4817-b7de-dadb8b4db874 --dir mosaic_ui
