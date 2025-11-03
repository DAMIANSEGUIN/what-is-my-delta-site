# Deployment Checklist

**CRITICAL:** Always follow this checklist before marking anything as "deployed"

## Pre-Deployment

- [ ] Ensure enforcement hooks are installed
  ```bash
  ./scripts/setup_hooks.sh
  # If config is locked, run: git config core.hooksPath .githooks
  ```

- [ ] Verify git remote configuration
  ```bash
  git remote -v
  # PRODUCTION = railway-origin (what-is-my-delta-site)
  # BACKUP = origin (wimd-railway-deploy)
  ```

- [ ] Ensure you're on the correct branch
  ```bash
  git branch
  # Should show: * main
  ```

- [ ] All changes committed
  ```bash
  git status
  # Should show: "nothing to commit, working tree clean"
  ```

## Deployment

- [ ] Push to **PRODUCTION** using wrapper (not origin!)
  ```bash
  ./scripts/push.sh railway-origin main
  ```

- [ ] Confirm push succeeded
  ```bash
  git log railway-origin/main --oneline -1
  # Should show your latest commit
  ```

## Post-Deployment Verification

- [ ] Wait for Railway backend rebuild (2 minutes)
  ```bash
  # Check Railway deployment status
  curl -s https://what-is-my-delta-site-production.up.railway.app/health | jq
  ```

- [ ] Wait for Netlify frontend rebuild (1 minute)
  ```bash
  # Check Netlify deployment status
  curl -I https://whatismydelta.com/ | grep -i "x-nf-request-id\|age"
  ```

- [ ] Verify specific changes are live
  ```bash
  # Example: Check if new function exists in deployed code
  curl -s https://whatismydelta.com/ | grep "LOGGING_OUT"
  ```

- [ ] Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)

- [ ] Test the specific fix you deployed
  - [ ] Can reproduce the original bug? (should be NO)
  - [ ] Does the fix work as expected? (should be YES)

## If Deployment Failed

- [ ] Check Railway logs: https://railway.app/dashboard
- [ ] Check Netlify logs: https://app.netlify.com/sites/resonant-crostata-90b706/deploys
- [ ] Verify correct remote was used: `git remote -v`
- [ ] Rollback if needed: `git revert <commit-hash> && git push railway-origin main`

## Common Mistakes to Avoid

❌ **WRONG:** `git push` (goes to 'origin' = backup repo)
✅ **RIGHT:** `./scripts/push.sh railway-origin main` (enforced verification + production push)

❌ **WRONG:** `git push railway-origin main` (bypasses wrapper script)
✅ **RIGHT:** `./scripts/push.sh railway-origin main` (wrapper enforces verification)

❌ **WRONG:** `netlify deploy --prod` (no verification)
✅ **RIGHT:** `./scripts/deploy.sh netlify` (automated verification)

❌ **WRONG:** Marking as "deployed" immediately after push
✅ **RIGHT:** Wait 2-3 minutes, verify live, THEN mark as deployed

❌ **WRONG:** Assuming deployment worked
✅ **RIGHT:** Always verify with curl/browser test

## Deployment Wrapper Scripts (MANDATORY)

**Always use wrapper scripts - they enforce automated verification:**

```bash
# Deploy frontend only
./scripts/deploy.sh netlify

# Deploy backend only
./scripts/deploy.sh railway

# Deploy both
./scripts/deploy.sh all

# Push to production (with verification)
./scripts/push.sh railway-origin main

# Push to backup repo (no verification required)
./scripts/push.sh origin main
```

**Emergency bypass (logged to audit):**
```bash
SKIP_VERIFICATION=true BYPASS_REASON="Production hotfix" ./scripts/push.sh railway-origin main
```

## Quick Reference

```bash
# 1. Commit changes
git add <files>
git commit -m "message"

# 2. Deploy to PRODUCTION (uses wrapper script)
./scripts/push.sh railway-origin main

# Script will automatically:
# - Run verification checks
# - Push to railway-origin
# - Display next steps

# 3. Wait 3 minutes for Railway + Netlify

# 4. Verify deployment
./scripts/verify_deployment.sh

# 5. Test in browser (hard refresh first)
```

---

**Remember:**
- If you can't verify it's live, it's NOT deployed
- Always use wrapper scripts (`./scripts/push.sh`, `./scripts/deploy.sh`)
- Never use raw `git push` or `netlify deploy` commands
