#!/bin/zsh
set -euo pipefail
CSV="${1:?Usage: $0 path/to/prompts.csv}"
python - <<'PY'
import sys
from api.prompts_loader import load_csv, sha256_file
rows = load_csv(sys.argv[1])
digest = sha256_file(sys.argv[1])
print(f"[OK] prompts CSV validated - rows={len(rows)} sha256={digest[:12]}…")
PY "$CSV"
