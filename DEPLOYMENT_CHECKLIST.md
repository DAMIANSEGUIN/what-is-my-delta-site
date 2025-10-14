# Deployment Checklist

**CRITICAL:** Always follow this checklist before marking anything as "deployed"

## Pre-Deployment

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

- [ ] Push to **PRODUCTION** remote (not origin!)
  ```bash
  git push railway-origin main
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
✅ **RIGHT:** `git push railway-origin main` (goes to production)

❌ **WRONG:** Marking as "deployed" immediately after push
✅ **RIGHT:** Wait 2-3 minutes, verify live, THEN mark as deployed

❌ **WRONG:** Assuming deployment worked
✅ **RIGHT:** Always verify with curl/browser test

## Quick Reference

```bash
# 1. Commit changes
git add <files>
git commit -m "message"

# 2. Push to PRODUCTION
git push railway-origin main

# 3. Wait 2-3 minutes

# 4. Verify deployment
curl -s https://whatismydelta.com/ | grep "<search-term>"

# 5. Test in browser (hard refresh first)
```

---

**Remember:** If you can't verify it's live, it's NOT deployed.
