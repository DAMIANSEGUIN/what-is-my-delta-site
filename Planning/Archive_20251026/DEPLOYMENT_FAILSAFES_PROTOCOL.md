# WIMD Deployment Fail-Safes Protocol

**Created**: 2025-10-24
**Purpose**: Prevent repository corruption and work loss during deployments
**Applies to**: All WIMD project deployment attempts

---

## Lesson Learned

**What went wrong:**
- Netlify upgrade recommendations attempted without baseline documentation
- Repository entered broken rebase state with merge conflicts
- No clear restore point to return to
- Critical error: **No baseline documented before making changes**

**Result:**
- Hours of recovery work
- Risk of losing Netlify Agent's completed features
- Uncertainty about what to preserve vs. discard

---

## Mandatory Fail-Safes

### 1. Pre-Deployment Baseline Documentation

**BEFORE any deployment changes:**

```bash
# Create dated baseline snapshot
cd /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project
./scripts/create_baseline_snapshot.sh
```

**What it documents:**
- Current git state (branch, commit, status)
- All modified/staged/untracked files
- Key file checksums (index.html, config files)
- Environment state (Railway, Netlify status)
- What features are currently working
- What changes are being attempted

**Output**: `BASELINE_SNAPSHOT_[DATE].md`

**Rule**: No deployment changes without this file created first

---

### 2. Git Safety Checkpoints

**Before any git operations:**

```bash
# Create safety branch pointing to current state
git branch safety-checkpoint-$(date +%Y%m%d-%H%M%S)

# Tag current state
git tag -a baseline-$(date +%Y%m%d-%H%M%S) -m "Baseline before [operation]"
```

**This allows instant rollback:**
```bash
# If something goes wrong
git reset --hard baseline-YYYYMMDD-HHMMSS
```

**Rule**: Every rebase, merge, or restructure gets a safety branch + tag first

---

### 3. Working Tree Backup

**Before modifying critical files:**

```bash
# Backup entire working tree
rsync -av --exclude='.git' \
  /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/ \
  /Users/damianseguin/Downloads/WIMD-BACKUP-$(date +%Y%m%d-%H%M%S)/
```

**For critical files only:**
```bash
# Backup just the files being changed
cp frontend/index.html frontend/index.html.backup-$(date +%Y%m%d-%H%M%S)
cp netlify.toml netlify.toml.backup-$(date +%Y%m%d-%H%M%S)
```

**Rule**: Critical files (index.html, netlify.toml, package.json) backed up before editing

---

### 4. Incremental Changes with Commits

**NO MORE:**
- Making multiple changes without commits
- Long-running rebase operations
- Batching unrelated changes together

**INSTEAD:**
- One logical change = one commit
- Test after each commit
- Document what each commit does

**Example workflow:**
```bash
# Change 1: Update dependency
npm install new-package
git add package.json package-lock.json
git commit -m "Add new-package dependency"
git push origin main  # Deploy to verify nothing broke

# Change 2: Update config
vim netlify.toml
git add netlify.toml
git commit -m "Update Netlify proxy rules for /api endpoint"
git push origin main  # Deploy to verify proxy works

# Change 3: Update UI
vim frontend/index.html
git add frontend/index.html
git commit -m "Add booking button to user dashboard"
git push origin main  # Deploy to verify UI renders
```

**Rule**: Never make 5 changes and commit once. Make 1 change, commit, deploy, verify.

---

### 5. Deployment Verification Checklist

**After each deployment:**

```bash
# Run verification script
./scripts/verify_deployment.sh
```

**Manual checks:**
- [ ] Railway deployment succeeded (check dashboard)
- [ ] Netlify deployment succeeded (check dashboard)
- [ ] Health endpoint returns 200: `curl https://whatismydelta.com/health`
- [ ] Frontend loads: `curl https://whatismydelta.com/`
- [ ] API proxy works: `curl https://whatismydelta.com/config`
- [ ] Key features still work (test in browser)

**Rule**: If ANY check fails, rollback immediately before making more changes

---

### 6. Rollback Plan Ready

**Before starting deployment work, verify rollback works:**

```bash
# Test that you CAN rollback
git log -5  # Know what commits to rollback to
git show HEAD~1  # Verify previous commit is good
git tag rollback-ready-$(date +%Y%m%d)  # Mark current good state

# Document rollback commands
echo "Rollback: git reset --hard rollback-ready-YYYYMMDD" > ROLLBACK_PLAN.txt
```

**Rule**: Know how to undo before you do

---

### 7. Communication Protocol

**Before deployment work:**
1. Announce intent: "About to upgrade Netlify configuration"
2. Document expected changes: "Will modify netlify.toml to add new proxy rules"
3. Document expected impact: "Should not affect existing features"
4. Get approval: "Proceed? (yes/no)"

**During deployment work:**
1. Announce each step: "Creating baseline snapshot"
2. Announce each commit: "Committed netlify.toml update"
3. Announce each deploy: "Deploying to Netlify"
4. Announce each verification: "Verified health endpoint still works"

**After deployment work:**
1. Announce completion: "Deployment complete"
2. Document what changed: "Added 3 new proxy rules to netlify.toml"
3. Document verification results: "All checks passed"

**Rule**: No silent operations. Keep user informed of every step.

---

## Specific Fail-Safes for Common Operations

### Rebase Operations

**Before rebase:**
```bash
# 1. Create safety branch
git branch safety-before-rebase-$(date +%Y%m%d-%H%M%S)

# 2. Document current state
git log --oneline -10 > rebase-baseline-$(date +%Y%m%d).txt
git status >> rebase-baseline-$(date +%Y%m%d).txt

# 3. Verify working tree is clean
git status | grep "working tree clean" || echo "WARNING: Uncommitted changes"

# 4. Have abort plan ready
echo "If rebase fails: git rebase --abort" > REBASE_ABORT_PLAN.txt
```

**During rebase:**
- At first sign of conflict, STOP
- Document the conflict
- Ask user if should continue or abort
- DO NOT make assumptions about conflict resolution

**After rebase:**
```bash
# Verify nothing lost
git diff safety-before-rebase-YYYYMMDD-HHMMSS

# If anything looks wrong
git rebase --abort  # Return to safety
```

**Rule**: Rebase only when necessary, always with safety branch, abort at first problem

---

### File Reorganization

**Before moving/deleting files:**
```bash
# 1. Document what exists now
find . -type f -name "*.md" > file-inventory-before.txt

# 2. Document what will change
echo "Will delete: frontend/docs/OLD_FILE.md" > reorganization-plan.txt
echo "Will move: specs/* to frontend/docs/specs/" >> reorganization-plan.txt

# 3. Create backup
tar -czf backup-before-reorganization-$(date +%Y%m%d).tar.gz frontend/docs/

# 4. Get approval
cat reorganization-plan.txt
# Wait for user "yes"
```

**After reorganization:**
```bash
# Verify critical files still exist
test -f frontend/index.html || echo "CRITICAL: index.html MISSING"
test -f netlify.toml || echo "CRITICAL: netlify.toml MISSING"

# Document what changed
find . -type f -name "*.md" > file-inventory-after.txt
diff file-inventory-before.txt file-inventory-after.txt
```

**Rule**: Never delete files without backup and explicit approval

---

### Dependency Updates

**Before updating packages:**
```bash
# 1. Backup current package files
cp package.json package.json.backup-$(date +%Y%m%d)
cp package-lock.json package-lock.json.backup-$(date +%Y%m%d)

# 2. Document current versions
npm list --depth=0 > installed-packages-before.txt

# 3. Test current state works
npm run build  # or relevant test command
```

**After updating:**
```bash
# 1. Document new versions
npm list --depth=0 > installed-packages-after.txt
diff installed-packages-before.txt installed-packages-after.txt

# 2. Test still works
npm run build

# 3. If broken, rollback
# cp package.json.backup-YYYYMMDD package.json
# cp package-lock.json.backup-YYYYMMDD package-lock.json
# npm install
```

**Rule**: Package updates are code changes. Treat them as deployments with verification.

---

## Automation Scripts to Create

### 1. `scripts/create_baseline_snapshot.sh`

```bash
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
- Health check: $(curl -s https://whatismydelta.com/health || echo "Failed")

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
```

**Make executable:**
```bash
chmod +x scripts/create_baseline_snapshot.sh
```

---

### 2. `scripts/create_safety_checkpoint.sh`

```bash
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
```

**Make executable:**
```bash
chmod +x scripts/create_safety_checkpoint.sh
```

---

### 3. `scripts/verify_deployment.sh`

```bash
#!/bin/bash
# Verify deployment succeeded and critical features still work

echo "=== WIMD Deployment Verification ==="
echo ""

# Check health endpoint
echo "Checking health endpoint..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" https://whatismydelta.com/health)
if [ "$HEALTH" = "200" ]; then
  echo "✅ Health endpoint: OK"
else
  echo "❌ Health endpoint: FAILED (HTTP $HEALTH)"
  exit 1
fi

# Check config endpoint
echo "Checking config endpoint..."
CONFIG=$(curl -s -o /dev/null -w "%{http_code}" https://whatismydelta.com/config)
if [ "$CONFIG" = "200" ]; then
  echo "✅ Config endpoint: OK"
else
  echo "❌ Config endpoint: FAILED (HTTP $CONFIG)"
  exit 1
fi

# Check frontend loads
echo "Checking frontend..."
FRONTEND=$(curl -s -o /dev/null -w "%{http_code}" https://whatismydelta.com/)
if [ "$FRONTEND" = "200" ]; then
  echo "✅ Frontend: OK"
else
  echo "❌ Frontend: FAILED (HTTP $FRONTEND)"
  exit 1
fi

# Check critical files exist
echo "Checking critical files..."
test -f frontend/index.html && echo "✅ index.html exists" || echo "❌ index.html MISSING"
test -f frontend/netlify.toml && echo "✅ netlify.toml exists" || echo "❌ netlify.toml MISSING"
test -f package.json && echo "✅ package.json exists" || echo "❌ package.json MISSING"

echo ""
echo "=== Verification Complete ==="
echo "All checks must pass before proceeding with more changes."
```

**Make executable:**
```bash
chmod +x scripts/verify_deployment.sh
```

---

## Deployment Workflow with Fail-Safes

**Complete safe deployment process:**

```bash
# 1. Create baseline snapshot
./scripts/create_baseline_snapshot.sh
# Fill in: What's Being Attempted, Expected Changes
# Get user approval

# 2. Create safety checkpoint
./scripts/create_safety_checkpoint.sh

# 3. Make ONE incremental change
# Example: Update netlify.toml
vim frontend/netlify.toml

# 4. Commit immediately
git add frontend/netlify.toml
git commit -m "Add /api proxy rule to netlify.toml"

# 5. Deploy
git push origin main

# 6. Verify
./scripts/verify_deployment.sh

# 7. If verification FAILS:
git reset --hard baseline-YYYYMMDD-HHMMSS
git push origin main --force

# 8. If verification PASSES:
# Repeat steps 3-6 for next change
```

**Rule**: Follow this exact sequence. No shortcuts.

---

## Emergency Recovery Procedures

### If Repository Gets Corrupted Again

```bash
# 1. STOP all operations immediately
# 2. Create emergency snapshot
git status > emergency-state-$(date +%Y%m%d-%H%M%S).txt
git log --oneline -20 >> emergency-state-$(date +%Y%m%d-%H%M%S).txt

# 3. Find most recent safety checkpoint
git tag -l "baseline-*" | tail -5

# 4. Reset to safety checkpoint
git reset --hard baseline-YYYYMMDD-HHMMSS

# 5. Verify recovery
./scripts/verify_deployment.sh

# 6. Document what happened
# Create incident report in incidents/ directory
```

### If Working Tree Files Lost

```bash
# 1. Check backups
ls -lt /Users/damianseguin/Downloads/WIMD-BACKUP-*/

# 2. Restore from most recent backup
rsync -av /Users/damianseguin/Downloads/WIMD-BACKUP-YYYYMMDD-HHMMSS/ \
  /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/

# 3. Verify critical files restored
test -f frontend/index.html && echo "OK" || echo "STILL MISSING"
```

---

## Success Criteria

**Deployment is considered safe when:**
- [ ] Baseline snapshot created before changes
- [ ] Safety checkpoint (branch + tag) created
- [ ] Each change committed incrementally
- [ ] Each commit verified with deployment check
- [ ] All verification checks pass
- [ ] Rollback plan documented and tested
- [ ] User informed at every step

**Deployment is considered UNSAFE when:**
- [ ] No baseline snapshot exists
- [ ] Multiple uncommitted changes
- [ ] No safety checkpoint
- [ ] Rebase in progress without documentation
- [ ] Files being deleted without backup
- [ ] User not informed of steps

---

## Integration with Planning Project Protocol

This fail-safe protocol implements the Pre-Flight Checklist from:
`/Users/damianseguin/Downloads/planning/TEAM_ORCHESTRATION_README.md`

**Before ANY deployment work:**
1. ✅ READ complete relevant documents (FULL READ)
2. ✅ VERIFY all file paths exist and are correct
3. ✅ TEST any commands before executing
4. ✅ CHECK for prerequisites or dependencies
5. ✅ CONFIRM sequence of steps is complete
6. ✅ **CREATE BASELINE SNAPSHOT** (added for deployments)
7. ✅ **CREATE SAFETY CHECKPOINT** (added for deployments)
8. ✅ **GET USER APPROVAL** before proceeding

---

## Next Steps

**To activate these fail-safes:**

1. **Create scripts directory:**
   ```bash
   mkdir -p /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/scripts
   ```

2. **Create the 3 automation scripts** listed above

3. **Test scripts on non-critical operation:**
   ```bash
   ./scripts/create_baseline_snapshot.sh
   ./scripts/create_safety_checkpoint.sh
   ./scripts/verify_deployment.sh
   ```

4. **Update WIMD documentation** to reference this protocol

5. **Make protocol mandatory** for all future deployment work

**Rule**: This protocol is now required. No deployment work without following these fail-safes.

---

**Document Status**: ✅ COMPLETE
**Next Action**: Create automation scripts, then ready for next deployment
**Date**: 2025-10-24
