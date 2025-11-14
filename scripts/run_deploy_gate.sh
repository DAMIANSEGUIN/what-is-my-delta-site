#!/bin/zsh
# Enforce Mosaic deployment gate before any production push/deploy.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

LOG_FILE=".verification_audit.log"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
ACTOR="${DEPLOY_ACTOR:-$(whoami)}"

echo "🛡️  Mosaic Deployment Gate"
echo "==============================="
echo ""
echo "Timestamp : $TIMESTAMP (UTC)"
echo "Actor     : $ACTOR"
echo ""
echo "Step 1: Running automated verification pipeline..."
echo ""

if ! ./scripts/pre_push_verification.sh; then
  {
    echo "[$TIMESTAMP] deploy_gate FAIL (pre_push_verification) actor=$ACTOR"
  } >> "$LOG_FILE"
  echo ""
  echo "❌ Deployment gate aborted - automated verification failed."
  exit 1
fi

echo ""
echo "✅ Automated verification passed"
echo ""

CHECKS=(
  "Baseline snapshot or diff review completed (PS101 + docs up to date)"
  "Auth + coach smoke test executed on local/staging build"
  "PS101 10-step flow walked end-to-end against this build"
  "Release notes & DEPLOYMENT_CHECKLIST updated for this deploy"
  "Human reviewer notified (or queued) for user-facing changes"
)

typeset -a RESPONSES
echo "Step 2: Confirm manual gate checklist (answer yes / no / n/a)."
echo ""

for idx in "${!CHECKS[@]}"; do
  check="${CHECKS[$idx]}"
  while true; do
    printf "%s? [yes/no/n/a]: " "$check"
    read -r reply
    reply="${reply:l}"
    if [[ "$reply" == "yes" || "$reply" == "y" ]]; then
      RESPONSES[$idx]="yes"
      break
    elif [[ "$reply" == "no" || "$reply" == "n" ]]; then
      RESPONSES[$idx]="no"
      {
        echo "[$TIMESTAMP] deploy_gate FAIL (manual:$check) actor=$ACTOR"
      } >> "$LOG_FILE"
      echo ""
      echo "❌ Deployment gate aborted - '$check' not confirmed."
      exit 1
    elif [[ "$reply" == "n/a" || "$reply" == "na" ]]; then
      RESPONSES[$idx]="n/a"
      break
    else
      echo "Please respond with yes, no, or n/a."
    fi
  done
done

echo ""
echo "✅ Manual checklist confirmed"
echo ""

{
  echo "[$TIMESTAMP] deploy_gate PASS actor=$ACTOR"
  echo "  automated=pass"
  for idx in "${!CHECKS[@]}"; do
    check="${CHECKS[$idx]}"
    response="${RESPONSES[$idx]-unset}"
    echo "  ${check} => ${response}"
  done
} >> "$LOG_FILE"

echo "Gate log appended to $LOG_FILE"
echo ""
echo "🟢 Deployment gate cleared. Safe to push and deploy."
