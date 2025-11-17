#!/bin/bash
# Create timestamped site backup for rollback capability
# Usage: ./scripts/create_site_backup.sh

set -euo pipefail

TIMESTAMP=$(date -u +%Y%m%d_%H%M%SZ)
BACKUP_DIR="backups"
BACKUP_FILE="$BACKUP_DIR/site-backup_$TIMESTAMP.zip"

mkdir -p "$BACKUP_DIR"

echo "📦 Creating site backup..."
echo "   Timestamp: $TIMESTAMP"
echo ""

# Backup critical directories
zip -r "$BACKUP_FILE" \
  frontend/ \
  mosaic_ui/ \
  api/ \
  scripts/ \
  .ai-agents/ \
  deployment/ \
  Mosaic/PS101_Continuity_Kit/ \
  CLAUDE.md \
  TROUBLESHOOTING_CHECKLIST.md \
  SELF_DIAGNOSTIC_FRAMEWORK.md \
  DEPLOYMENT_CHECKLIST.md \
  -x "*.pyc" -x "__pycache__/*" -x ".git/*" -x "node_modules/*" -x ".venv/*" -x "*.log" \
  > /dev/null 2>&1

BACKUP_SIZE=$(ls -lh "$BACKUP_FILE" | awk '{print $5}')

echo "✅ Backup created: $BACKUP_FILE ($BACKUP_SIZE)"
echo ""
echo "Rollback command:"
echo "  unzip -o $BACKUP_FILE"
echo ""
echo "Backup includes:"
echo "  - Frontend/UI code"
echo "  - Backend API code"
echo "  - Deployment scripts & configs"
echo "  - Agent session notes"
echo "  - PS101 continuity kit"
echo "  - Critical documentation"
echo ""
