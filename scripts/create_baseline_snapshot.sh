#!/bin/bash
# Create comprehensive baseline snapshot before deployment changes

SNAPSHOT_FILE="BASELINE_SNAPSHOT_$(date +%Y%m%d-%H%M%S).md"

cat > "$SNAPSHOT_FILE" <<EOF
# Baseline Snapshot - $(date)

## Git State
\`\`\`
$(git status)
\`\`\`

## Current Branch & Commit
- Branch: $(git branch --show-current)
- Commit: $(git rev-parse HEAD)
- Message: $(git log -1 --pretty=%B)

## Modified Files
\`\`\`
$(git diff --name-only)
\`\`\`

## Staged Files
\`\`\`
$(git diff --cached --name-only)
\`\`\`

## Untracked Files
\`\`\`
$(git ls-files --others --exclude-standard)
\`\`\`

## Critical File Checksums
- index.html: $(shasum -a 256 frontend/index.html 2>/dev/null || echo "N/A")
- netlify.toml: $(shasum -a 256 frontend/netlify.toml 2>/dev/null || echo "N/A")
- package.json: $(shasum -a 256 package.json 2>/dev/null || echo "N/A")

## Deployment Status
- Last Railway deploy: [Check Railway dashboard]
- Last Netlify deploy: [Check Netlify dashboard]
- Health check: $(curl -s https://whatismydelta.com/health 2>/dev/null || echo "Failed")

## What's Being Attempted
[To be filled by user]

## Expected Changes
[To be filled by user]

## Rollback Plan
\`\`\`bash
git reset --hard $(git rev-parse HEAD)
# Or: git checkout $(git branch --show-current)
\`\`\`
EOF

echo "✅ Baseline snapshot created: $SNAPSHOT_FILE"
echo ""
echo "BEFORE proceeding, fill in:"
echo "  - What's Being Attempted"
echo "  - Expected Changes"
echo ""
echo "Then get user approval to proceed."
