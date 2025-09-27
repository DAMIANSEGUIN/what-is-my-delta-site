#!/bin/zsh
set -euo pipefail

# Guarded cleanup helper for old Railway resources.
# This script DOES NOT silently delete anything. It:
# - Shows the currently linked project/service (if accessible)
# - Lets you unlink the repo from a project
# - Lets you delete an environment (with confirmation)
# - Lets you roll back the most recent deployment (railway down)
# - Opens the Railway dashboard for manual project/service deletion
#
# Note: Some destructive operations (deleting services/projects) are not
# exposed via all Railway CLI versions; use the dashboard for those.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v railway >/dev/null 2>&1; then
  echo "Error: Railway CLI not found. Install: https://docs.railway.app/reference/cli" >&2
  exit 1
fi

if ! railway whoami >/dev/null 2>&1; then
  echo "You are not logged into Railway. Launching 'railway login'..."
  railway login || { echo "Login failed" >&2; exit 1; }
fi

echo "=== WIMD – Guarded Cleanup for Old Railway Resources ==="
echo "This tool helps you clean up with explicit confirmation for every action."

echo "\nCurrent link status (may fail if offline):"
railway status || echo "(Could not fetch status — network or auth may be required)"

echo "\nSelect an action:"
echo "  1) Unlink current directory from project"
echo "  2) Delete an environment (e.g., Production)"
echo "  3) Roll back last deployment (railway down)"
echo "  4) List projects in your account"
echo "  5) Open dashboard to delete project/service manually"
echo "  6) Quit"

read -r "choice?Choose [1-6]: "
case "$choice" in
  1)
    echo "You are about to unlink this directory from its Railway project."
    read -r "ans?Type YES to confirm unlink: "
    if [[ "$ans" == "YES" ]]; then
      railway unlink || true
      echo "Unlinked."
    else
      echo "Aborted."
    fi
    ;;
  2)
    echo "Environment deletion is destructive and permanent."
    railway environment list || true
    read -r "env?Environment name to delete (exact): "
    if [[ -z "$env" ]]; then
      echo "No environment provided. Aborting."
      exit 1
    fi
    read -r "ans?Type DELETE $env to confirm: "
    if [[ "$ans" == "DELETE $env" ]]; then
      railway environment delete "$env" || {
        echo "Failed to delete environment via CLI. Use dashboard if needed." >&2
      }
    else
      echo "Confirmation did not match. Aborted."
    fi
    ;;
  3)
    echo "This will remove the most recent deployment for the active service."
    read -r "ans?Type DOWN to confirm: "
    if [[ "$ans" == "DOWN" ]]; then
      railway down || {
        echo "Failed to roll back deployment via CLI. Use dashboard if needed." >&2
      }
    else
      echo "Aborted."
    fi
    ;;
  4)
    echo "Listing projects (may require network access):"
    railway list || true
    ;;
  5)
    echo "Opening Railway dashboard in your browser..."
    railway open || echo "Could not open dashboard from CLI."
    echo "From the dashboard, you can delete projects/services safely."
    ;;
  6|*)
    echo "Bye."
    ;;
esac

