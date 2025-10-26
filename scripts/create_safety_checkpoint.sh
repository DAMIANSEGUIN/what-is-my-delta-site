#!/bin/bash
# Create safety checkpoint before risky operations

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BRANCH_NAME="safety-checkpoint-$TIMESTAMP"
TAG_NAME="baseline-$TIMESTAMP"

# Create safety branch
git branch "$BRANCH_NAME"
echo "✅ Created safety branch: $BRANCH_NAME"

# Create tag
git tag -a "$TAG_NAME" -m "Baseline before deployment work"
echo "✅ Created tag: $TAG_NAME"

# Document rollback
cat > ROLLBACK_PLAN_$TIMESTAMP.txt <<EOF
# Rollback Plan - $TIMESTAMP

## To rollback git state:
git reset --hard $TAG_NAME

## To rollback to safety branch:
git checkout $BRANCH_NAME

## Current state:
- Branch: $(git branch --show-current)
- Commit: $(git rev-parse HEAD)
- HEAD: $(git log -1 --oneline)
EOF

echo "✅ Rollback plan: ROLLBACK_PLAN_$TIMESTAMP.txt"
echo ""
echo "You can now proceed with changes."
echo "To rollback: git reset --hard $TAG_NAME"
