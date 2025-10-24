# CRITICAL ISSUES REPORT FOR NARS
**Date:** 2025-10-14
**Session:** Claude Code troubleshooting session
**Status:** ✅ ROOT CAUSE CONFIRMED - Railway SQLite Ephemeral Storage
**Updated:** 2025-10-14 (Post-NARs Investigation)

---

## EXECUTIVE SUMMARY

The Mosaic platform is experiencing **persistent authentication and session management issues** that suggest a fundamental architectural problem rather than isolated bugs. Multiple fixes have been attempted but symptoms keep recurring, indicating we're treating symptoms rather than the root cause.

**Critical Observation:** Every "fix" works in code but fails in production, suggesting the issue is **infrastructure-level**, not code-level.

---

## SYMPTOMS OBSERVED (In Order)

### 1. ❌ PS101 Flow Not Working
- **Symptom:** Users get "huge pile of generic advice" instead of guided PS101 questions
- **Expected:** One question at a time, iterative flow
- **Fix Attempted:** Auto-activate PS101, track prompt_index for one-at-a-time
- **Status:** Fixed in code, deployed, but...

### 2. ❌ Login Credentials Invalid
- **Symptom:** User registers, logs out, tries to login → "Invalid credentials"
- **Expected:** Login should work with same credentials
- **Fix Attempted:** Created backend `/auth/logout` endpoint, session deletion
- **Status:** Worked initially, now broken again

### 3. ❌ Chat History Persists After Logout
- **Symptom:** User logs out, page reloads, chat window still has old messages
- **Expected:** Chat should be completely empty after logout
- **Fix Attempted:** Clear localStorage, chatLog.innerHTML, sessionStorage flag
- **Status:** Code deployed, but still not clearing

### 4. ❌ Login Form Pre-fills After Logout
- **Symptom:** Email/password fields populated after logout
- **Expected:** Clean login form
- **Note:** Partially browser autofill (expected), but suggests state not clearing

### 5. ❌ Invalid Credentials (Again)
- **Symptom:** After all fixes deployed, getting "Invalid credentials" again
- **Expected:** Login should work
- **Status:** RECURRING ISSUE - suggests deeper problem

---

## ROOT CAUSE HYPOTHESIS

Based on symptoms pattern, the underlying issue is likely **ONE** of:

### Hypothesis 1: Railway SQLite Ephemeral Storage (MOST LIKELY)
**Evidence:**
- Railway uses ephemeral filesystem for SQLite
- Database at `data/mosaic.db` gets wiped on every deployment
- User registers → user created in DB
- We deploy a fix → Railway rebuilds → DB wiped → user gone
- User tries to login → "Invalid credentials" because user no longer exists

**From Architecture Audit (line 308):**
> "Railway ephemeral storage - SQLite resets on deployment (CRITICAL)"

**This explains:**
- ✅ Why login works initially, then breaks after deployments
- ✅ Why session state persists (session never actually deleted from DB)
- ✅ Why fixes "work" but then fail (DB reset destroys all data)
- ✅ Why PS101 state persists (old sessions in DB that don't get cleared)

### Hypothesis 2: Multiple Concurrent Sessions Per User
**Evidence:**
- No session cleanup on logout (fixed, but may not have deployed correctly)
- User creates session A, logs out, session A still in DB
- User logs in again → creates session B, but session A still exists
- Backend might be loading wrong session

### Hypothesis 3: Browser Aggressive Caching
**Evidence:**
- Changes deployed to production
- Browser still serving old JavaScript
- Hard refresh (Ctrl+Shift+R) required but user may not be doing it
- Service worker or CDN caching

### Hypothesis 4: Deployment Not Actually Reaching Production
**Evidence:**
- We pushed to wrong repo for 9 commits (wimd-railway-deploy vs what-is-my-delta-site)
- Fixed the repo issue, but Netlify might still not auto-deploying
- Code shows as deployed via `curl`, but actual runtime might be cached/old

---

## EVIDENCE FOR HYPOTHESIS 1 (Railway SQLite)

**From `api/storage.py:12-13`:**
```python
DATA_ROOT = Path(os.getenv("DATA_ROOT", "data"))
DB_PATH = Path(os.getenv("DATABASE_PATH", DATA_ROOT / "mosaic.db"))
```

**Railway Deployment Behavior:**
1. Git push triggers rebuild
2. Container rebuilt from scratch
3. `data/` directory **not persisted** (no Railway volume configured)
4. New container starts with **empty database**
5. All users, sessions, PS101 state → **GONE**

**From CLAUDE.md:**
> "Production URL: https://whatismydelta.com (LIVE ✅)"
> "Backend API: Railway deployment"

**No mention of:**
- Railway PostgreSQL setup
- Railway volume mount for SQLite persistence
- Database backup strategy
- Migration to persistent storage

**This is a P0 CRITICAL issue from the Architecture Audit.**

---

## WHY SYMPTOMS KEEP RECURRING

**Timeline:**
1. User registers → works (user in DB)
2. Claude deploys PS101 fix → Railway rebuilds → **DB wiped**
3. User tries to login → "Invalid credentials" (user gone from DB)
4. User registers again → works (new user in DB)
5. Claude deploys logout fix → Railway rebuilds → **DB wiped again**
6. User tries to login → "Invalid credentials" **AGAIN**

**We're in a cycle:**
```
Register → Works → Deploy → DB wiped → Login fails → Repeat
```

---

## VALIDATION NEEDED

**To confirm Hypothesis 1 (Railway SQLite), check:**

1. **SSH into Railway container and check DB:**
   ```bash
   railway shell
   ls -la data/
   sqlite3 data/mosaic.db "SELECT COUNT(*) FROM users;"
   ```

2. **Check Railway environment variables:**
   ```bash
   railway variables
   # Look for DATABASE_PATH, DATABASE_URL
   ```

3. **Check Railway volumes:**
   ```bash
   railway volumes list
   # Should be EMPTY if using ephemeral storage
   ```

4. **Check Railway filesystem persistence:**
   - Go to Railway dashboard
   - Check if `data/` directory is mounted as a volume
   - If NO volume → confirms hypothesis

5. **Test: Register → Check DB → Deploy → Check DB again:**
   - Register a test user
   - SSH in: `sqlite3 data/mosaic.db "SELECT email FROM users;"`
   - Deploy any change (trigger rebuild)
   - SSH in again: `sqlite3 data/mosaic.db "SELECT email FROM users;"`
   - If user gone → **CONFIRMED**

---

## RECOMMENDED SOLUTION (P0 CRITICAL)

### Option 1: Migrate to Railway PostgreSQL (RECOMMENDED)
**Why:** Production-grade, persistent, backed up
**Timeline:** 2-4 hours
**Steps:**
1. Provision Railway PostgreSQL database
2. Update `api/storage.py` to use PostgreSQL instead of SQLite
3. Add `psycopg2` to `requirements.txt`
4. Run migration scripts
5. Test thoroughly
6. Deploy

**Impact:**
- ✅ Database persists across deployments
- ✅ Production-ready
- ✅ Automatic backups
- ✅ Scales properly
- ✅ Fixes all symptoms

### Option 2: Configure Railway Volume for SQLite
**Why:** Quick fix, keeps SQLite
**Timeline:** 30 minutes
**Steps:**
1. Create Railway volume mounted at `/app/data`
2. Update `DATA_ROOT` env var to point to volume
3. Test that DB persists across deployments

**Drawbacks:**
- SQLite not ideal for production
- No automatic backups
- Single point of failure
- Doesn't scale

### Option 3: External Database (AWS RDS, etc.)
**Why:** Maximum control and reliability
**Timeline:** 4-8 hours
**Drawbacks:** Cost, complexity, overkill for MVP

---

## IMMEDIATE ACTIONS REQUIRED

**STOP deploying fixes until root cause confirmed.**

**Instead:**

1. **NARs to validate Hypothesis 1:**
   - Check Railway dashboard for volumes
   - SSH into Railway container
   - Check if `data/mosaic.db` persists across deploys

2. **If Hypothesis 1 confirmed:**
   - STOP all feature work
   - PRIORITY: Migrate to Railway PostgreSQL
   - Timeline: 1 day max
   - Then retest all symptoms

3. **If Hypothesis 1 wrong:**
   - Work through Hypotheses 2, 3, 4
   - Add more diagnostics
   - May need pair programming session with screen share

---

## WHAT CLAUDE CODE DID (Session Summary)

**Fixes Attempted:**
1. ✅ PS101 auto-activation (deployed)
2. ✅ PS101 one-question-at-a-time (deployed)
3. ✅ Backend `/auth/logout` endpoint (deployed)
4. ✅ sessionStorage LOGGING_OUT flag (deployed)
5. ✅ Comprehensive architecture audit (documented)
6. ✅ Deployment safety mechanisms (git hooks, checklists)
7. ✅ Debug logging for troubleshooting (deployed)

**Process Failures:**
1. ❌ Pushed 9 commits to wrong repo (wimd-railway-deploy instead of what-is-my-delta-site)
2. ❌ Didn't verify deployments were live before claiming "fixed"
3. ❌ Treated symptoms instead of investigating root cause
4. ❌ Should have checked infrastructure first (Railway config, database persistence)

**Correct Actions:**
1. ✅ Identified deployment process issue
2. ✅ Fixed repo configuration
3. ✅ Created deployment safety hooks
4. ✅ Created comprehensive architecture audit (60+ issues documented)
5. ✅ Escalated to NARs when pattern became clear

---

## RECOMMENDATION FOR NARS

**Priority 1:** Confirm Railway SQLite persistence issue (30 min investigation)

**Priority 2:** If confirmed, migrate to Railway PostgreSQL (4 hours work)

**Priority 3:** Retest all symptoms with persistent database

**Priority 4:** Address remaining P0 issues from Architecture Audit:
- Session management (httpOnly cookies instead of localStorage)
- Password hashing (bcrypt instead of SHA-256)
- Rate limiting
- Security headers

**DO NOT:**
- Deploy more symptom fixes
- Continue troubleshooting without confirming root cause
- Waste more time on chat clearing / logout issues until DB persistence confirmed

---

## FILES CHANGED THIS SESSION

**Code:**
- `api/index.py` - Added `/auth/logout` endpoint
- `api/storage.py` - Added `delete_session()` function
- `api/ps101_flow.py` - Fixed one-question-at-a-time, added prompt_index tracking
- `mosaic_ui/index.html` - Logout logic, sessionStorage flag, console logging

**Documentation:**
- `ARCHITECTURE_AUDIT_2025-10-14.md` - Comprehensive audit (322 lines)
- `DEPLOYMENT_CHECKLIST.md` - Deployment process documentation
- `.github/PULL_REQUEST_TEMPLATE.md` - PR deployment verification
- `.git/hooks/pre-push` - Git safety hook

**Tools:**
- `mosaic_ui/debug.html` - Logout debugging tool

---

## NEXT SESSION PROTOCOL

**Before continuing troubleshooting:**

1. NARs confirms or refutes Railway SQLite hypothesis
2. If confirmed: migrate to PostgreSQL FIRST
3. If refuted: new hypothesis with evidence
4. Only then continue symptom fixes

**Don't repeat today's mistake:** Treating symptoms without understanding root cause.

---

## NARs INVESTIGATION RESULTS (2025-10-14)

**Status:** ✅ **ROOT CAUSE CONFIRMED**

### NARs Findings

1. **Railway Configuration Analysis:**
   - `railway.json` contains `"include": ["data/**/*"]` directive
   - This directive **only copies files into build** - does NOT create persistent storage
   - No Railway Volume configured in project dashboard
   - SQLite database stored in ephemeral container filesystem

2. **Technical Confirmation:**
   - **Ephemeral Storage:** Files included via directive are wiped on each deployment
   - **Persistent Storage:** Would require explicit Railway Volume or managed database service
   - **Current Behavior:** `data/mosaic.db` recreated fresh on every Railway rebuild

3. **Root Cause Validated:**
   - ✅ Pattern matches: User registers → deploy → DB wiped → "Invalid credentials"
   - ✅ All symptoms (authentication, sessions, PS101) explained by DB resets
   - ✅ Hypothesis 1 from original report **CONFIRMED**

### Conclusion

**The `railway.json` include directive is insufficient for database persistence.** Every deployment triggers Railway container rebuild, wiping the SQLite database and all user accounts/sessions.

---

## IMMEDIATE ACTION REQUIRED

**Status:** P0 CRITICAL - Production blocker **CONFIRMED**

**Solution:** Migrate to Railway PostgreSQL (managed database service)

**Estimated Fix Time:** 4 hours (PostgreSQL migration + schema migration + testing)

**DO NOT:**
- Deploy any more symptom fixes
- Continue troubleshooting authentication/session issues
- Create new user accounts for testing (will be wiped on next deploy)

**DO:**
- Provision Railway PostgreSQL database immediately
- Migrate schema from SQLite to PostgreSQL
- Update `api/storage.py` connection logic
- Deploy and verify database persists across deployments
- THEN retest all symptoms
