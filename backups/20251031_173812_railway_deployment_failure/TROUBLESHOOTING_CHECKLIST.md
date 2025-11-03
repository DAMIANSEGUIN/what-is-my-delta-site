# Mosaic Platform Troubleshooting Checklist
**Custom Dashboard Filter for Claude Code**

---

## Quick Diagnostic Filter

**Run this checklist BEFORE making any code changes:**

```
□ Read recent Railway deployment logs
□ Check /health endpoint status
□ Verify DATABASE_URL format (postgresql://...railway.internal)
□ Confirm PostgreSQL service status in Railway dashboard
□ Review last 3 git commits for breaking changes
□ Check if error is in known taxonomy (see below)
```

---

## Error Classification Dashboard

### 🔴 CRITICAL (Production Down)

| Error Label | Symptom | Root Cause | First Action |
|-------------|---------|------------|--------------|
| `RAILWAY_RESTART_LOOP` | Container crashes repeatedly | Code bug, dependency missing | Check deploy logs for exception |
| `PG_CONNECTION_FAILED` | App using SQLite fallback | Wrong DATABASE_URL, network issue | Verify DATABASE_URL contains `railway.internal` |
| `CONTEXT_MANAGER_BUG` | AttributeError: 'object has no attribute execute' | Using `conn = get_conn()` instead of `with get_conn() as conn:` | Search codebase for incorrect pattern |
| `OPENAI_INVALID_KEY` | All AI features fail | API key revoked/wrong | Check OPENAI_API_KEY in Railway variables |

### 🟡 WARNING (Degraded)

| Error Label | Symptom | Root Cause | First Action |
|-------------|---------|------------|--------------|
| `SQLITE_FALLBACK_ACTIVE` | Data wiped on deploy | PostgreSQL not connected | Check DATABASE_URL, PostgreSQL service status |
| `OPENAI_RATE_LIMIT` | 429 errors from OpenAI | Usage spike, quota exceeded | Enable retry with backoff, check usage |
| `PS101_STATE_CORRUPT` | Users seeing wrong questions | prompt_index out of range | Reset session PS101 state |
| `EMBEDDING_FAILED` | Semantic search not working | OpenAI embeddings API down | Use keyword fallback |

### 🟢 INFO (Functional but Needs Attention)

| Error Label | Symptom | Root Cause | First Action |
|-------------|---------|------------|--------------|
| `RERANKER_UNAVAILABLE` | Using mock reranker | CrossEncoder model load failed | Acceptable fallback, monitor quality |
| `PROMPT_CSV_WARNING` | Some prompts missing | CSV parse issue | Validate CSV format |
| `SESSION_EXPIRED` | User logged out unexpectedly | TTL exceeded (>30 days) | Normal behavior |

---

## Code Change Pre-Flight Checklist

**Before writing ANY code:**

```
ARCHITECTURE AWARENESS:
□ Do I understand what layer this touches? (DB / API / LLM / UI)
□ Have I checked for similar code patterns in the codebase?
□ Do I know what happens if this component fails?

DATABASE CHANGES:
□ Am I using context manager? (with get_conn() as conn:)
□ Am I using PostgreSQL syntax? (%s not ?, SERIAL not AUTOINCREMENT)
□ Am I getting cursor first? (cursor = conn.cursor())
□ Is this operation idempotent? (ON CONFLICT, check before insert)

ERROR HANDLING:
□ Am I logging errors explicitly? (not swallowing exceptions)
□ Will this fail gracefully? (fallback behavior defined)
□ Can I diagnose this from logs alone? (enough context logged)

DEPLOYMENT SAFETY:
□ Can I rollback this change? (git revert path clear)
□ Is there a feature flag? (can disable without deploy)
□ Have I tested locally? (golden dataset, manual test)
□ Did I check for breaking changes? (API contracts, schema)
```

---

## Symptom → Diagnosis Flow

### Symptom: "Invalid Credentials" After Deployment

```
1. Check: Is PostgreSQL connected?
   railway logs | grep STORAGE
   → Look for: "[STORAGE] ✅ PostgreSQL connection pool created"
   → If SQLite fallback: DATABASE_URL issue

2. Check: Does user exist in database?
   # This requires Railway shell or psql access
   → If user missing: Database wiped (SQLite fallback confirmed)

3. Check: Was deployment recent?
   git log --oneline -5
   → If deploy within last hour: Database reset on deploy

4. Diagnosis: SQLITE_FALLBACK_ACTIVE
   → Action: Fix DATABASE_URL (ensure railway.internal)
   → Verify: PostgreSQL service status in Railway
```

### Symptom: Deployment Failed

```
1. Check: Build logs or deploy logs?
   Railway dashboard → Deployment → Build Logs vs Deploy Logs
   → If no deploy logs: App crashed on startup
   → If build failed: Dependency or syntax error

2. Check: What's the error message?
   Look for:
   - "AttributeError" → Likely context manager bug
   - "ModuleNotFoundError" → Missing dependency in requirements.txt
   - "psycopg2" → PostgreSQL connection issue
   - "Syntax Error" → Python syntax error in code

3. Check: Recent commits
   git log --oneline -3
   → Identify what changed recently

4. Action: Rollback if needed
   git revert HEAD
   git push railway-origin main
```

### Symptom: App Slow / Timeouts

```
1. Check: Health endpoint
   curl https://what-is-my-delta-site-production.up.railway.app/health
   → Check p95_latency_ms

2. Check: Is it OpenAI/Anthropic?
   Railway logs | grep -i "openai\|anthropic"
   → Look for slow response times

3. Check: Database queries
   → Slow queries (missing indexes)
   → Too many queries (N+1 problem)

4. Diagnosis:
   → If AI calls: Add timeout, retry logic
   → If DB: Add indexes, optimize queries
   → If overall: Scale Railway instance
```

### Symptom: Users Seeing Old Data

```
1. Check: Browser cache?
   → Ask user to hard refresh (Ctrl+Shift+R)

2. Check: Netlify deployment
   → Is frontend deployed?
   → Check Netlify dashboard

3. Check: Session state
   → Old session data in localStorage
   → Clear localStorage in browser console

4. Diagnosis: LIKELY_CACHING
   → Action: Add cache-busting headers
   → Or: Increment version number in /config
```

---

## Railway-Specific Diagnostics

### Check DATABASE_URL Format

```bash
# In Railway CLI
railway variables | grep DATABASE_URL

# Should contain:
✅ postgresql://
✅ railway.internal (NOT railway.app)
✅ :5432/railway

# Should NOT contain:
❌ sqlite://
❌ railway.app (public URL, use internal)
```

### Check PostgreSQL Service

```bash
# In Railway dashboard:
1. Click PostgreSQL service
2. Status should be: "Active" or "Running"
3. Check "Metrics" - should show connections
4. Check "Logs" - no errors
```

### Check Deployment Logs

```bash
# In Railway dashboard:
1. Click what-is-my-delta-site service
2. Click "Deployments" tab
3. Click most recent deployment
4. Click "Deploy Logs" (NOT Build Logs)
5. Look for:
   - [STORAGE] messages
   - Exception tracebacks
   - "ERROR:" lines
```

---

## Code Pattern Filters

### ✅ CORRECT Patterns (Use These)

```python
# Database operations
with get_conn() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()

# Error handling with logging
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    # Explicit fallback or re-raise
    raise

# Idempotent inserts
cursor.execute("""
    INSERT INTO table (id, data)
    VALUES (%s, %s)
    ON CONFLICT (id) DO UPDATE SET data = EXCLUDED.data
""", (id, data))

# Retry with backoff
@retry_with_exponential_backoff(max_retries=3)
def call_external_api():
    # API call here
    pass
```

### ❌ INCORRECT Patterns (Never Use)

```python
# Wrong: Direct get_conn() usage
conn = get_conn()
cursor = conn.execute(...)  # AttributeError!

# Wrong: SQLite syntax in PostgreSQL
cursor.execute("SELECT * FROM users WHERE email = ?", (email,))  # Use %s

# Wrong: Silent exception swallowing
try:
    risky_operation()
except:
    pass  # No logging, no fallback

# Wrong: Non-idempotent operations
cursor.execute("INSERT INTO table VALUES (%s)", (data,))  # Fails on duplicate

# Wrong: Infinite retry
while True:
    try:
        call_api()
        break
    except:
        continue  # Never gives up!
```

---

## Debugging Workflow

### Step 1: Classify the Issue

```
Ask yourself:
1. When did this start? (recent deploy? always?)
2. Who is affected? (all users? one user? specific action?)
3. What's the error? (exception? wrong behavior? slow?)
4. Where is it? (frontend? API? database? LLM?)

Map to category:
- INFRA: Railway, PostgreSQL, networking
- DATA: Sessions, users, PS101 state
- MODEL: OpenAI, Anthropic, prompts
- PROMPT: CSV, JSON parsing
- INTEGRATION: Job sources, external APIs
```

### Step 2: Gather Context

```
Collect diagnostics:
□ Railway deployment logs (last 200 lines)
□ Health endpoint response (/health)
□ Recent git commits (git log -5)
□ Environment variables (railway variables)
□ PostgreSQL service status
□ Error message (full traceback)
□ User actions that triggered it
□ Recent deployments timeline
```

### Step 3: Form Hypothesis

```
Based on error category + context:

If INFRA error:
  → Check DATABASE_URL format
  → Check PostgreSQL service status
  → Check recent Railway changes

If DATA error:
  → Check database schema version
  → Check for foreign key violations
  → Check session expiration

If MODEL error:
  → Check API keys set
  → Check rate limits / quota
  → Check model names valid

If PROMPT error:
  → Validate JSON/CSV files
  → Check file permissions
  → Check for schema changes

If INTEGRATION error:
  → Check external API status
  → Check API keys / auth
  → Check for API changes
```

### Step 4: Test Hypothesis

```
Verify hypothesis:
□ Can I reproduce locally?
□ Does the log match the hypothesis?
□ Does a simple fix resolve it?
□ Is there a known playbook for this?

If hypothesis wrong:
→ Go back to Step 2 with more context
→ Consult SELF_DIAGNOSTIC_FRAMEWORK.md
→ Escalate to NARs with full context
```

### Step 5: Implement Fix

```
Before fixing:
□ Check pre-flight checklist (above)
□ Ensure rollback path exists
□ Test locally first
□ Run golden dataset tests

After fixing:
□ Deploy with clear commit message
□ Monitor logs for 5 minutes
□ Verify health endpoint
□ Test the specific symptom
□ Update documentation if new pattern
```

---

## Quick Reference Commands

```bash
# Check deployment status
railway status

# Get environment variables
railway variables

# View recent logs
railway logs

# Check health endpoint
curl https://what-is-my-delta-site-production.up.railway.app/health

# Check if PostgreSQL connected
railway logs | grep -i "storage\|postgres"

# Rollback to previous commit
git revert HEAD && git push railway-origin main

# Force redeploy (no code changes)
git commit --allow-empty -m "Redeploy" && git push railway-origin main

# Run tests locally
pytest tests/test_golden_dataset.py -v
```

---

## Decision Tree: "Should I Deploy This?"

```
START
  │
  ├─> Does this change database code?
  │     ├─> YES: Did I use context manager pattern?
  │     │     ├─> NO: ❌ FIX FIRST
  │     │     └─> YES: Did I use PostgreSQL syntax (%s)?
  │     │           ├─> NO: ❌ FIX FIRST
  │     │           └─> YES: Continue
  │     └─> NO: Continue
  │
  ├─> Does this change error handling?
  │     ├─> YES: Am I logging errors?
  │     │     ├─> NO: ❌ ADD LOGGING
  │     │     └─> YES: Continue
  │     └─> NO: Continue
  │
  ├─> Have I tested locally?
  │     ├─> NO: ❌ TEST FIRST
  │     └─> YES: Continue
  │
  ├─> Do I have a rollback plan?
  │     ├─> NO: ❌ PLAN ROLLBACK
  │     └─> YES: Continue
  │
  └─> ✅ SAFE TO DEPLOY
        │
        ├─> Deploy: git push railway-origin main
        ├─> Monitor: railway logs (5 min)
        ├─> Verify: curl /health
        └─> Test: specific symptom resolved
```

---

## Emergency Procedures

### 🚨 Production is Down

```
IMMEDIATE:
1. Check Railway dashboard - is service running?
2. If crashed: Check deploy logs for error
3. If context manager bug: Rollback immediately
4. If PostgreSQL: Check DATABASE_URL, PostgreSQL service

ROLLBACK:
git revert HEAD
git push railway-origin main --force
# Wait 2 minutes
curl /health

COMMUNICATE:
- Post status update
- ETA for fix
- Workaround if any
```

### 🔥 Data Loss Detected

```
ASSESS:
1. Is PostgreSQL connected? (check logs for STORAGE messages)
2. If SQLite fallback: All data lost on last deploy
3. If PostgreSQL: Check if table dropped/truncated

RECOVER:
- If SQLite: No recovery possible (ephemeral)
- If PostgreSQL: Check for backups in Railway
- Last resort: Restore from git history + redeploy

PREVENT:
- Ensure DATABASE_URL uses railway.internal
- Verify PostgreSQL service active
- Add data backup strategy
```

### ⚡ Performance Degradation

```
DIAGNOSE:
1. Check /health endpoint - what's p95_latency_ms?
2. Check Railway metrics - CPU/Memory usage
3. Check logs - slow queries, API timeouts?

IMMEDIATE FIX:
- If OpenAI timeout: Add shorter timeout + fallback
- If DB slow: Add indexes, optimize queries
- If memory: Restart service, investigate leak

LONG TERM:
- Scale Railway instance
- Add caching layer
- Optimize hot paths
```

---

## Checklist Summary (Print This)

**Before Every Code Change:**
```
□ Read SELF_DIAGNOSTIC_FRAMEWORK.md
□ Context manager pattern? (with get_conn() as conn:)
□ PostgreSQL syntax? (%s, SERIAL, cursor first)
□ Errors logged explicitly?
□ Idempotent operation?
□ Rollback plan exists?
□ Tested locally?
```

**Before Every Deploy:**
```
□ Run ./pre_deploy_check.sh
□ Golden dataset tests pass?
□ Regression tests pass?
□ Database connection works?
□ Environment variables set?
□ Git commit message clear?
```

**After Every Deploy:**
```
□ Monitor logs 5 minutes
□ Check /health endpoint
□ Verify PostgreSQL connected (no SQLite fallback)
□ Test the specific fix
□ No new errors in logs?
```

**When Things Break:**
```
□ Get full error message from logs
□ Classify error (INFRA/DATA/MODEL/PROMPT/INTEGRATION)
□ Check if known error (see dashboard above)
□ Execute playbook if exists
□ If new error: gather full context
□ Form hypothesis → test → fix → verify
□ If stuck: escalate with FULL context
```

---

**END OF TROUBLESHOOTING CHECKLIST**
