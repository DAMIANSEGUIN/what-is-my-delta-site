#!/bin/zsh
set -euo pipefail

# One-shot script to create a fresh Railway deployment for this repo.
# - Creates a new Railway project (does NOT delete your existing one)
# - Prompts for env vars (from .env.example) and sets them
# - Deploys using railway.json/Procfile (Nixpacks + gunicorn)
#
# Requirements:
# - Railway CLI installed: https://docs.railway.app/reference/cli
# - Logged in: `railway login`

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v railway >/dev/null 2>&1; then
  echo "Error: Railway CLI not found. Install: https://docs.railway.app/reference/cli" >&2
  exit 1
fi

# Check login
if ! railway whoami >/dev/null 2>&1; then
  echo "You are not logged into Railway. Launching 'railway login'..."
  railway login || { echo "Login failed" >&2; exit 1; }
fi

echo "=== WIMD – One Shot New Deploy ==="

# Sanity check files
[[ -f Procfile ]] || { echo "Missing Procfile" >&2; exit 1; }
[[ -f railway.json ]] || { echo "Missing railway.json" >&2; exit 1; }

# Run predeploy sanity if available
if [[ -x ./scripts/predeploy_sanity.sh ]]; then
  echo "Running predeploy sanity checks..."
  ./scripts/predeploy_sanity.sh
fi

# Create a fresh project name
TS=$(date +%y%m%d-%H%M)
DEFAULT_NAME="wimd-api-${TS}"
read -r "PROJECT_NAME?Project name [${DEFAULT_NAME}]: "
PROJECT_NAME=${PROJECT_NAME:-$DEFAULT_NAME}

echo "Creating new Railway project: ${PROJECT_NAME}"
if ! railway init --name "$PROJECT_NAME" --no-prompt >/dev/null 2>&1; then
  echo "Note: 'railway init --name' may not be supported on your CLI version. Falling back to interactive init..."
  railway init || true
fi

# Ensure we are linked to the created/selected project
if ! railway status >/dev/null 2>&1; then
  echo "Linking to a project interactively..."
  railway link || true
fi

echo "Selecting or creating an environment (e.g., Production)"
if ! railway environment list >/dev/null 2>&1; then
  echo "Your CLI may use a different command for environments. Proceeding without switching."
else
  # Try to ensure we are in a reasonable environment (Production), create if missing
  if ! railway environment list | rg -q '^Production$'; then
    railway environment create Production || true
  fi
  railway environment use Production || true
fi

# Ensure there is a service created before setting variables
echo "\nCreating/ensuring service exists with initial deploy..."
if ! railway up; then
  echo "Initial 'railway up' failed. Try linking/selecting project/service and rerun."
  exit 1
fi

# Try to detect service name for targeted variable setting
SERVICE_NAME="$(railway status 2>/dev/null | awk -F": " '/^Service:/ {print $2; exit}')"
if [[ -n "$SERVICE_NAME" ]]; then
  echo "Detected service: $SERVICE_NAME"
else

  echo "Could not auto-detect service name; variable setting will not target a service explicitly."
fi

# Always prompt securely for provider API keys first
echo "\nEnter provider API keys (input hidden)."
read -s -r "OPENAI_API_KEY?  OPENAI_API_KEY (starts with sk-): " || true; echo
read -s -r "CLAUDE_API_KEY?  CLAUDE_API_KEY (starts with sk-ant-): " || true; echo

if [[ -n "$OPENAI_API_KEY" ]]; then
  echo "Setting OPENAI_API_KEY"
  if [[ -n "$SERVICE_NAME" ]]; then
    railway variables --service "$SERVICE_NAME" --set "OPENAI_API_KEY=$OPENAI_API_KEY" --skip-deploys >/dev/null 2>&1 || \
    railway variables set "OPENAI_API_KEY=$OPENAI_API_KEY" >/dev/null 2>&1 || \
    echo "Failed to set OPENAI_API_KEY via CLI. You may need to set it manually in the dashboard."
  else
    railway variables --set "OPENAI_API_KEY=$OPENAI_API_KEY" --skip-deploys >/dev/null 2>&1 || \
    railway variables set "OPENAI_API_KEY=$OPENAI_API_KEY" >/dev/null 2>&1 || \
    echo "Failed to set OPENAI_API_KEY via CLI. You may need to set it manually in the dashboard."
  fi
fi

if [[ -n "$CLAUDE_API_KEY" ]]; then
  echo "Setting CLAUDE_API_KEY"
  if [[ -n "$SERVICE_NAME" ]]; then
    railway variables --service "$SERVICE_NAME" --set "CLAUDE_API_KEY=$CLAUDE_API_KEY" --skip-deploys >/dev/null 2>&1 || \
    railway variables set "CLAUDE_API_KEY=$CLAUDE_API_KEY" >/dev/null 2>&1 || \
    echo "Failed to set CLAUDE_API_KEY via CLI. You may need to set it manually in the dashboard."
  else
    railway variables --set "CLAUDE_API_KEY=$CLAUDE_API_KEY" --skip-deploys >/dev/null 2>&1 || \
    railway variables set "CLAUDE_API_KEY=$CLAUDE_API_KEY" >/dev/null 2>&1 || \
    echo "Failed to set CLAUDE_API_KEY via CLI. You may need to set it manually in the dashboard."
  fi
fi

# Collect env vars from .env.example and set them for the created service (skip provider keys already handled)
VARS_FILE=".env.example"
if [[ ! -f "$VARS_FILE" ]]; then
  echo "Warning: $VARS_FILE not found. Skipping variable prompts."
else
  echo "\nConfiguring variables (Railway → Variables)"
  while IFS= read -r line; do
    [[ -z "$line" || "$line" == \#* ]] && continue
    key="${line%%=*}"
    default="${line#*=}"
    current="${(P)key:-}"
    # skip provider keys here; already handled securely above
    if [[ "$key" == "OPENAI_API_KEY" || "$key" == "CLAUDE_API_KEY" ]]; then
      continue
    fi
    prompt_default="$current";
    [[ -z "$prompt_default" ]] && prompt_default="$default"
    read -r "val?  $key [${prompt_default}]: "
    val=${val:-$prompt_default}
    echo "Setting $key"
    if [[ -n "$SERVICE_NAME" ]]; then
      if ! railway variables --service "$SERVICE_NAME" --set "$key=$val" --skip-deploys >/dev/null 2>&1; then
        if ! railway variables set "$key=$val" >/dev/null 2>&1; then
          echo "Failed to set $key via CLI. You may need to set it manually in the dashboard." >&2
        fi
      fi
    else
      if ! railway variables --set "$key=$val" --skip-deploys >/dev/null 2>&1; then
        if ! railway variables set "$key=$val" >/dev/null 2>&1; then
          echo "Failed to set $key via CLI. You may need to set it manually in the dashboard." >&2
        fi
      fi
    fi
  done < "$VARS_FILE"
fi

echo "\nRedeploying with updated variables..."
if ! railway up; then
  echo "railway up failed. You can try again after adjusting variables."
  exit 1
fi

echo "\n=== Deploy triggered ==="
echo "Next steps:"
echo "- Watch the build/deploy in the Railway dashboard (railway open)."
echo "- Once live, copy the service URL into PUBLIC_API_BASE (if needed)."
echo "- Optionally run: ./scripts/verify_deploy.sh \"\$PUBLIC_API_BASE\""
echo "\nNote about old deploys:"
echo "- This script creates a brand-new project and does NOT delete your existing one."
echo "- If you want to remove the old service/project, do it from the Railway dashboard to avoid accidental data loss."
