# Pull Request Checklist

## Pre-Merge Checklist

- [ ] Code changes reviewed and tested locally
- [ ] All tests passing (if applicable)
- [ ] No merge conflicts with main branch
- [ ] Deployment checklist followed (see DEPLOYMENT_CHECKLIST.md)

## Deployment Verification (REQUIRED)

**⚠️ DO NOT MERGE until deployment is verified**

After merging to main, you MUST:

- [ ] Push to production: `git push railway-origin main`
- [ ] Wait 2-3 minutes for rebuild
- [ ] Verify changes live on https://whatismydelta.com
- [ ] Test the specific fix in browser (hard refresh first)
- [ ] Mark this PR with `deployed` label ONLY after verification

## Changes Summary

<!-- Describe what changed -->

## Testing Instructions

<!-- How to test this change -->

## Deployment Impact

<!-- Does this require database migration? Environment variables? -->

- [ ] Backend changes (Railway rebuild required)
- [ ] Frontend changes (Netlify rebuild required)
- [ ] Database migration needed
- [ ] Environment variables added/changed
- [ ] Breaking changes (requires coordination)

## Rollback Plan

<!-- How to rollback if this breaks production -->

---

**Remember:**
- Production remote = `railway-origin` (NOT `origin`)
- Always verify deployment before marking as complete
- If unsure, ping @DAMIANSEGUIN
