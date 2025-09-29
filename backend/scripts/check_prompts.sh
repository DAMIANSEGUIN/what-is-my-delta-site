#!/bin/zsh
set -euo pipefail
CSV="${1:?Usage: $0 path/to/prompts.csv}"
python - <<'PY'
import sys
from api.prompts_loader import load_csv
load_csv(sys.argv[1]); print("[OK] prompts CSV validated")
PY "$CSV"
