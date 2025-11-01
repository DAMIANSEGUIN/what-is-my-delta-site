# Deployment Verification Checklist

**Purpose:** Standard verification steps for ALL deployments to production
**Owner:** Damian (Project Owner)
**Usage:** Run this checklist immediately after every Railway deployment completes
**Created:** 2025-10-31
**Last Updated:** 2025-10-31

---

## Pre-Deployment (Before Pushing)

**Run these checks BEFORE deploying:**

- [ ] All code changes committed to git
- [ ] Git commit message clear and descriptive
- [ ] No sensitive data in code (API keys, passwords, secrets)
- [ ] `./scripts/predeploy_sanity.sh` passes (if exists)
- [ ] Local testing complete
- [ ] Feature flags set correctly for deployment
- [ ] Database migrations tested locally (if applicable)
- [ ] Rollback plan documented

---

## During Deployment (Active Monitoring)

**Monitor these while deployment in progress:**

### Railway Dashboard
- [ ] Build logs show no errors
- [ ] Build completes successfully
- [ ] Deploy logs show application starting
- [ ] No exception tracebacks in deploy logs
- [ ] Container status shows "Active" or "Running"

### Critical Log Messages
Watch for these in Railway logs:

**✅ Good signs:**
```
[STORAGE] ✅ PostgreSQL connection pool created
[STORAGE] Using PostgreSQL backend
Application startup complete
Uvicorn running on http://0.0.0.0:8000
```

**🚨 Bad signs:**
```
[STORAGE] ⚠️ SQLite fallback active
ERROR: Connection refused
AttributeError: 'object has no attribute execute'
ModuleNotFoundError:
psycopg2.OperationalError:
```

---

## Post-Deployment (Immediate - Within 5 Minutes)

**Run these checks immediately after deployment completes:**

### 1. Health Check Endpoint

```bash
curl https://what-is-my-delta-site-production.up.railway.app/health
```

**Verify response:**
- [ ] Status code: 200 OK
- [ ] `"ok": true`
- [ ] `"database.connected": true`
- [ ] `"database.type": "postgresql"` (NOT sqlite)
- [ ] `"database.fallback_active": false`
- [ ] `"metrics.error_rate"` < 0.05 (5%)
- [ ] `"metrics.p95_latency_ms"` < 2000ms
- [ ] `"deployment.git_commit"` matches your recent commit

**If any check fails:** Investigate immediately, consider rollback

### 2. Config Endpoint

```bash
curl https://what-is-my-delta-site-production.up.railway.app/config
```

**Verify response:**
- [ ] Returns valid JSON
- [ ] `"apiBase"` matches expected URL
- [ ] `"schemaVersion"` correct

### 3. Critical API Endpoints

**Test key endpoints:**

```bash
# Prompts endpoint
curl https://what-is-my-delta-site-production.up.railway.app/prompts/active

# Auth health check (should return 401 without credentials)
curl https://what-is-my-delta-site-production.up.railway.app/auth/me
```

**Verify:**
- [ ] Prompts endpoint returns data (not null)
- [ ] Auth endpoint returns 401 Unauthorized (expected)
- [ ] No 500 Internal Server Error responses

### 4. Frontend Load Test

**Open in browser:**
- [ ] https://whatismydelta.com loads without errors
- [ ] No console errors in browser DevTools
- [ ] Chat interface visible
- [ ] Login/register buttons work
- [ ] Navigation buttons functional

### 5. Database Connection Verification

**Check Railway logs for:**
- [ ] `[STORAGE] ✅ PostgreSQL connection pool created`
- [ ] No `SQLite fallback active` warnings
- [ ] No connection timeout errors

### 6. Feature-Specific Checks

**For PS101 v2 deployments:**
- [ ] Navigate to PS101 flow
- [ ] Step navigation works (Next/Previous)
- [ ] Multi-prompt display correct
- [ ] Experiment components visible on Steps 6-9
- [ ] **Issue #1 fix:** Inline forms appear (NOT browser prompts)
- [ ] **Issue #1 fix:** Keyboard navigation works (Tab, ESC, Enter)
- [ ] **Issue #1 fix:** Inline validation shows error messages
- [ ] State persists in localStorage
- [ ] Download summary works

**For job search deployments (Phase 4):**
- [ ] Job search button functional
- [ ] Job sources returning data
- [ ] RAG search working (not falling back to random)
- [ ] Resume optimization functional

**For authentication changes:**
- [ ] Register new user works
- [ ] Login with credentials works
- [ ] Password reset flow functional
- [ ] Session persists across page refresh

---

## Post-Deployment (Extended - Within 30 Minutes)

**Continue monitoring for 30 minutes after deployment:**

### 7. Error Rate Monitoring

**Check Railway logs every 5-10 minutes:**
- [ ] No new exception tracebacks appearing
- [ ] No spike in error messages
- [ ] Request volume normal
- [ ] Response times stable

**Run health check multiple times:**
```bash
# Run 5 times, 1 minute apart
for i in {1..5}; do
  echo "Check $i:"
  curl -s https://what-is-my-delta-site-production.up.railway.app/health | jq '.metrics'
  sleep 60
done
```

**Verify:**
- [ ] Error rate stays < 5%
- [ ] P95 latency stable (not increasing)
- [ ] No database connection drops

### 8. User Journey Testing

**Complete a full user journey:**

**New user flow:**
- [ ] Register new account
- [ ] Verify email shows in users table (psql or Railway shell)
- [ ] Login with new account
- [ ] Start PS101 journey
- [ ] Complete Step 1
- [ ] Verify state persists (refresh page)
- [ ] Logout works

**Returning user flow:**
- [ ] Login with existing account
- [ ] Previous PS101 progress loads correctly
- [ ] Can continue from last step
- [ ] Can navigate to any completed step
- [ ] State auto-saves on changes

### 9. Regression Testing

**Verify existing features still work:**

- [ ] Chat/coach interface responds
- [ ] File upload works (resume upload)
- [ ] Job search returns results
- [ ] Resume optimization generates output
- [ ] Authentication (login/logout) works
- [ ] Trial mode works for unauthenticated users
- [ ] All navigation buttons functional

### 10. Performance Verification

**Check for performance degradation:**

- [ ] Page load time < 3 seconds
- [ ] API response times < 2 seconds
- [ ] No slow query warnings in logs
- [ ] No memory warnings in Railway metrics
- [ ] CPU usage normal (not spiking)

---

## Post-Deployment (Final - Within 24 Hours)

### 11. Monitor for Anomalies

**Check the next day:**
- [ ] No overnight errors in Railway logs
- [ ] No user-reported issues
- [ ] Database size normal (no unexpected growth)
- [ ] No security alerts (if monitoring enabled)
- [ ] Cost metrics normal (Railway usage dashboard)

### 12. Update Documentation

**After successful deployment:**
- [ ] Update DEPLOYMENT_LOG.md with deployment date and version
- [ ] Mark task as complete in PROJECT_PLAN_ADJUSTMENTS.md
- [ ] Update ARCHITECTURAL_DECISIONS.md if new decisions made
- [ ] Create team update if significant changes (use TEAM_UPDATE_TEMPLATE.md)
- [ ] Close related GitHub issues (if applicable)

---

## Rollback Procedure

**If ANY critical check fails, execute rollback:**

### Immediate Rollback (< 5 min from deploy)

```bash
# Get last known good commit
git log --oneline -5

# Rollback to previous commit
git revert HEAD
git push railway-origin main --force

# Or checkout specific commit
git checkout <LAST_GOOD_COMMIT>
git push railway-origin HEAD:main --force
```

**After rollback:**
- [ ] Verify health check passes
- [ ] Verify critical endpoints work
- [ ] Document issue in DEPLOYMENT_LOG.md
- [ ] Create incident report (if major)
- [ ] Plan fix for next deployment

### Partial Rollback (Feature Flag)

**If feature flag enabled:**
```bash
# Disable problematic feature via Railway variables
railway variables set FEATURE_FLAG_NAME=false

# Force redeploy
git commit --allow-empty -m "Disable feature: FEATURE_FLAG_NAME"
git push railway-origin main
```

### Database Rollback (CRITICAL - USE WITH CAUTION)

**Only if database migration failed:**
- [ ] Check Railway PostgreSQL backups
- [ ] Restore from most recent backup
- [ ] Document data loss (if any)
- [ ] Notify affected users (if any)

---

## Deployment Log Entry Template

**After every deployment, add entry to DEPLOYMENT_LOG.md:**

```markdown
## Deployment: YYYY-MM-DD HH:MM

**Commit:** <git commit hash>
**Deployed By:** <Your name>
**Duration:** <X minutes>

**Changes:**
- <Summary of changes>
- <Feature additions>
- <Bug fixes>

**Verification Results:**
- [ ] Health check: PASS/FAIL
- [ ] Database: PostgreSQL connected
- [ ] Critical endpoints: PASS/FAIL
- [ ] User journey: PASS/FAIL
- [ ] Regression tests: PASS/FAIL

**Issues Encountered:**
- <None or list issues>

**Rollback:** Yes/No (if yes, explain)

**Notes:**
- <Any additional notes>
```

---

## Emergency Contacts

**If critical issues found during deployment:**

1. **Database issues:** Check Railway PostgreSQL service status
2. **API down:** Check Railway deployment logs, restart if needed
3. **Data loss detected:** Check DATABASE_URL, verify PostgreSQL connected
4. **Security incident:** Rotate API keys immediately, investigate breach

**Escalation path:**
1. Self-diagnosis: Check TROUBLESHOOTING_CHECKLIST.md
2. Playbook execution: Check SELF_DIAGNOSTIC_FRAMEWORK.md
3. Team notification: Post in team channel
4. Owner notification: Alert Damian if production down > 15 minutes

---

## Quick Reference Commands

```bash
# Check Railway deployment status
railway status

# Get recent logs
railway logs --tail 100

# Check environment variables
railway variables

# Health check
curl https://what-is-my-delta-site-production.up.railway.app/health

# Force redeploy (no code changes)
git commit --allow-empty -m "Force redeploy" && git push railway-origin main

# Rollback to previous commit
git revert HEAD && git push railway-origin main
```

---

## Checklist Maintenance

**This checklist should be updated:**
- After every major incident (add new check to prevent recurrence)
- When new features deployed (add feature-specific checks)
- Monthly review (remove outdated checks, improve clarity)
- When team feedback suggests improvements

**Owner:** Damian
**Reviewers:** All agents (Cursor, Codex, Claude Code)
**Next Review:** 2025-11-30

---

**END OF DEPLOYMENT VERIFICATION CHECKLIST**

**Usage:** Copy relevant sections to task brief or run through this list manually after every deployment.
