#!/bin/bash
# Initial GDrive sync - run this ONCE manually
# After this, the git post-commit hook will auto-sync on every commit

PROJECT_DIR="/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project"
GDRIVE_PATH="gdrive:WIMD-Railway-Deploy-Project"
RCLONE="/Users/damianseguin/coachvox_tools/bin/rclone"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         Initial Google Drive Sync for ChatGPT Access          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "This will sync project files to Google Drive once."
echo "Future commits will auto-sync via git post-commit hook."
echo ""
echo "Syncing to: $GDRIVE_PATH"
echo ""

# Sync with progress
$RCLONE sync "$PROJECT_DIR" "$GDRIVE_PATH" \
  --exclude ".git/**" \
  --exclude "node_modules/**" \
  --exclude "venv/**" \
  --exclude ".venv/**" \
  --exclude ".test-venv/**" \
  --exclude ".claude-run/**" \
  --exclude "__pycache__/**" \
  --exclude "*.pyc" \
  --exclude ".DS_Store" \
  --exclude "*.log" \
  --fast-list \
  --transfers 8 \
  --progress

if [ $? -eq 0 ]; then
  echo ""
  echo "╔════════════════════════════════════════════════════════════════╗"
  echo "║                    ✅ SYNC COMPLETE                            ║"
  echo "╚════════════════════════════════════════════════════════════════╝"
  echo ""
  echo "Google Drive folder: WIMD-Railway-Deploy-Project"
  echo "Future commits will automatically sync via git hook."
  echo ""
  echo "Next: Share the GDrive folder with ChatGPT"
else
  echo ""
  echo "❌ Sync failed. Check rclone configuration:"
  echo "   $RCLONE listremotes"
  exit 1
fi
