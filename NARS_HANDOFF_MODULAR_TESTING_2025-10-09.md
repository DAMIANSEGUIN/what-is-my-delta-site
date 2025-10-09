# NARs Handoff - Modular Testing of Failed Deployments

**From**: Claude Code (Infrastructure Debugger)
**To**: Netlify Agent Runners (NARs)
**Date**: 2025-10-09
**Priority**: CRITICAL - Multiple deployment failures, production stuck on 3-day-old code

---

## Request

**Systematically compare working vs failing deployments and test new elements in isolation.**

Break down the changes I made into modules and test each one independently to identify which specific change is breaking Railway deployments.

---

## Working Deployment (Baseline)

**Commit**: `a583d26a` (Oct 6, 2025) or `067f33a` (Oct 7, 2025)
**Status**: ✅ Active on Railway production
**Health endpoint**: Returns `{"ok": true, "timestamp": "..."}`
**Location**: Railway service `what-is-my-delta-site`

**Key characteristics**:
- Simple health check (no "checks" field)
- No AI client initialization
- No feature flag migration
- No monitoring system
- No prompt selector caching fixes

---

## Failed Deployments (My Attempts)

**Commits**:
1. `7c2807e` - Fix health check 503: Force boolean conversion for SQLite feature flags
2. `2888657` - Force Railway cache clear

**Status**: ❌ Both failed Railway health checks
**Failure pattern**: Build succeeds → Container starts → Health check returns 503 → Deployment marked failed

**Railway keeps**: Old deployment (a583d26a) active

---

## Changes Made (067f33a → 2888657)

### 1. AI Client Initialization (`api/ai_clients.py`)
**Commit**: `ee6712f`
```python
# BEFORE: Commented out
# import openai
# from anthropic import Anthropic

# AFTER: Uncommented with try/except
try:
    import openai
    from anthropic import Anthropic
    AI_PACKAGES_AVAILABLE = True
except ImportError:
    AI_PACKAGES_AVAILABLE = False
```

**Impact**: Initialize OpenAI/Anthropic clients if API keys present

---

### 2. Feature Flag Migration (`api/migrations.py` + `api/startup_checks.py`)
**Commits**: `79f9395`, `79f9395`

**Added migration 004**:
```python
"004_sync_feature_flags_from_json": """
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'AI_FALLBACK_ENABLED';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'RAG_BASELINE';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'SELF_EFFICACY_METRICS';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'COACH_ESCALATION';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'JOB_SOURCES_STUBBED_ENABLED';
"""
```

**Startup hook** (`api/startup_checks.py:36-54`):
```python
async def run():
    init_db()
    # Run migration to sync feature flags from JSON to database
    try:
        result = run_migration("004_sync_feature_flags_from_json", dry_run=False)
        if result.get("success"):
            print("✅ Feature flags synced to database")
    except Exception as e:
        print(f"⚠️ Migration error: {e}, continuing startup")
    cleanup_expired_sessions()
```

**Impact**: Runs database migration during FastAPI startup

---

### 3. Prompt Selector Caching Fix (`api/prompt_selector.py`)
**Commit**: `6d7e578`

**BEFORE**:
```python
def __init__(self):
    self.settings = get_settings()
    self.cache_ttl_hours = 24
    self.fallback_enabled = self._check_feature_flag("AI_FALLBACK_ENABLED")  # Cached at init
```

**AFTER**:
```python
def __init__(self):
    self.settings = get_settings()
    self.cache_ttl_hours = 24
    # Don't cache feature flag - check dynamically to allow runtime updates
```

All references changed to dynamic checks:
```python
fallback_enabled = self._check_feature_flag("AI_FALLBACK_ENABLED")
```

**Impact**: Feature flags checked dynamically instead of cached at module import

---

### 4. Boolean Conversion Fix (`api/prompt_selector.py:34`)
**Commit**: `7c2807e`

**BEFORE**:
```python
def _check_feature_flag(self, flag_name: str) -> bool:
    row = conn.execute(...).fetchone()
    return row and row[0] if row else False  # Returns SQLite integer 0/1
```

**AFTER**:
```python
def _check_feature_flag(self, flag_name: str) -> bool:
    row = conn.execute(...).fetchone()
    # FORCE BOOLEAN CONVERSION - SQLite returns 0/1, not True/False
    return bool(row[0]) if row else False  # Converts to Python bool
```

**Impact**: Fixes `0 or False = False` evaluation issue

---

### 5. Enhanced Health Check (`api/index.py:423-489`)
**Commits**: `027eaf2`, `7c2807e`

**BEFORE**:
```python
@app.get("/health")
def health():
    return {"ok": True, "timestamp": datetime.utcnow().isoformat() + "Z"}
```

**AFTER**:
```python
@app.get("/health")
def health():
    prompt_health = get_prompt_health()
    fallback_enabled = prompt_health.get("fallback_enabled", False)
    ai_available = prompt_health.get("ai_health", {}).get("any_available", False)

    prompt_system_ok = fallback_enabled or ai_available
    db_ok = True  # database connectivity check
    overall_ok = prompt_system_ok and db_ok

    health_status = {
        "ok": overall_ok,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {
            "database": db_ok,
            "prompt_system": prompt_system_ok,
            "ai_fallback_enabled": fallback_enabled,
            "ai_available": ai_available
        }
    }

    if not overall_ok:
        raise HTTPException(status_code=503, detail=health_status)

    return health_status
```

**Impact**: Health check now tests prompt system and returns 503 if unhealthy

---

### 6. Monitoring System (`api/monitoring.py`)
**Commit**: `027eaf2`

**Added**: New file `api/monitoring.py` (199 lines)
- PromptMonitor class
- Health check logging
- Auto-recovery system

**Import** in `api/index.py:46`:
```python
from .monitoring import run_health_check, attempt_system_recovery
```

**Impact**: Adds monitoring infrastructure (may or may not be used in health check)

---

### 7. Debug Endpoint (`api/index.py:501-534`)
**Commit**: `7c2807e` (later removed by CODEX)

**Added**:
```python
@app.get("/debug/system-state")
def debug_system_state():
    # Returns AI client status, database flags, prompt selector state
```

**CODEX removed this** in local uncommitted changes for security

**Impact**: Debug endpoint for diagnostics (removed before final deploy)

---

### 8. Railway Configuration (`railway.toml`)
**Commit**: `027eaf2`

**Added**:
```toml
[deploy]
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[healthcheck]
httpTimeout = 30
httpPath = "/health"
httpMethod = "GET"
```

**Impact**: Configures Railway to monitor /health endpoint with 300s timeout

---

### 9. Cache Busting File
**Commit**: `2888657`

**Added**: `.railwaybust` (dummy file to force cache clear)

**Impact**: Attempt to bypass Railway build cache

---

## Root Cause Hypothesis

**Railway health check timing issue:**

1. Railway starts container
2. FastAPI begins accepting requests
3. **Railway hits `/health` endpoint** (starts health check timer)
4. Startup migration begins running (`api/startup_checks.py:run()`)
5. Health check sees `fallback_enabled: 0` (migration hasn't updated DB yet)
6. Health check logic: `0 or False = False` → `prompt_system_ok = False`
7. Health check returns **503**
8. **Railway marks deployment failed** (before migration completes)
9. Migration completes successfully (too late)
10. Railway keeps old deployment (a583d26a) active

**Evidence**:
- Deploy logs show: "✅ Migration executed successfully"
- Deploy logs show: "✅ Feature flags synced to database"
- But also show: `INFO: "GET /health HTTP/1.1" 503 Service Unavailable`
- Deployment fails after 14 health check attempts over 5 minutes

---

## Modular Testing Request

**NARs, please test these changes in isolation:**

### Test 1: AI Client Initialization Only
**Branch**: Create from `067f33a` + only AI client changes from `ee6712f`

Files to modify:
- `api/ai_clients.py` - Uncomment imports

**Expected**: Should deploy successfully (no health check changes)

---

### Test 2: Feature Flag Migration Only
**Branch**: Create from `067f33a` + only migration from `79f9395`

Files to modify:
- `api/migrations.py` - Add migration 004
- `api/startup_checks.py` - Add migration call

**Expected**: Should deploy successfully (no health check enforcement)

---

### Test 3: Prompt Selector Caching Fix Only
**Branch**: Create from `067f33a` + only caching fix from `6d7e578`

Files to modify:
- `api/prompt_selector.py` - Remove cached flag, make dynamic

**Expected**: Should deploy successfully (no health check enforcement)

---

### Test 4: Boolean Conversion Only
**Branch**: Create from `067f33a` + only bool fix from `7c2807e`

Files to modify:
- `api/prompt_selector.py:34` - Add `bool()` conversion

**Expected**: Should deploy successfully (no health check enforcement)

---

### Test 5: Health Check Enhancement Only
**Branch**: Create from `067f33a` + only health check from `027eaf2`

Files to modify:
- `api/index.py:423-489` - Enhanced health check logic
- `railway.toml` - Health check configuration

**Expected**: **This is likely the breaking change** - will fail if prompt system not ready

---

### Test 6: Monitoring System Only
**Branch**: Create from `067f33a` + only monitoring from `027eaf2`

Files to modify:
- `api/monitoring.py` - New file
- `api/index.py:46` - Import statement

**Expected**: Should deploy successfully (adds code but doesn't use it)

---

### Test 7: Railway Config Only
**Branch**: Create from `067f33a` + only `railway.toml` from `027eaf2`

Files to modify:
- `railway.toml` - Health check configuration

**Expected**: Should deploy successfully (simple health check still passes)

---

### Test 8: Combined (Phased Approach)
If individual tests pass, combine in phases:

**Phase A**: Tests 1-4 together (AI + migration + caching + bool fix)
**Phase B**: Add monitoring (Test 6)
**Phase C**: Add Railway config (Test 7)
**Phase D**: Add health check last (Test 5)

**Expected**: Identifies which combination breaks

---

## Alternative Hypothesis to Test

**Could the migration itself be failing?**

Check if migration is actually running and succeeding:

1. Add HEALTH_DEBUG=1 to Railway environment variables
2. Deploy with enhanced logging
3. Check logs for migration success/failure
4. Verify database actually has `AI_FALLBACK_ENABLED = 1`

**Could AI clients be failing to initialize despite logs saying success?**

Test:
1. Add `/health/prompts` endpoint test during deployment
2. Verify `ai_available` value during health check
3. Check if API keys are set in Railway environment

---

## Files to Review

**Working deployment code**:
- `git show 067f33a:api/index.py` - Simple health check
- `git show 067f33a:api/ai_clients.py` - Commented imports
- `git show 067f33a:api/prompt_selector.py` - Cached flags

**Failed deployment code**:
- `git show 2888657:api/index.py` - Enhanced health check
- `git show 2888657:api/ai_clients.py` - Initialized clients
- `git show 2888657:api/prompt_selector.py` - Dynamic flags with bool()

**Diff summary**:
```bash
git diff 067f33a..2888657 --stat
```
Shows 21 files changed, 451 insertions, 19 deletions

---

## Railway Deployment Info

**Project**: `wimd-career-coaching`
**Service**: `what-is-my-delta-site`
**Environment**: `production`
**Repository**: `github.com/DAMIANSEGUIN/what-is-my-delta-site`
**Branch**: `main`

**Active deployment**: `a583d26a` (Oct 6)
**Failed deployments**: Multiple from Oct 8-9
**Health endpoint**: `/health` with 300s timeout

---

## Success Criteria

**Immediate**:
1. Identify which specific change breaks Railway deployment
2. Determine if it's the enhanced health check or something else
3. Propose minimal fix that gets new code deployed

**Validation**:
1. Deployment succeeds (health check passes)
2. Production serves new code
3. User can test site without "CSV prompts not found" error
4. Feature flags properly enabled in database

---

## Reference Documents

**In project directory** (`/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/`):

1. `CODEX_HANDOFF_HEALTH_CHECK_2025-10-09.md` - Full technical analysis
2. `CLAUDE_CODE_DEBUGGING_REPORT_2025-10-08.md` - Original issue investigation
3. `CODEX_INSTRUCTIONS.md` - Role definitions and protocols
4. `CLAUDE.md` - Current project status

---

## Questions for NARs

1. **Can you create isolated test branches** for each module and deploy to Railway staging/preview?
2. **Can you verify the migration actually runs** by checking Railway database state?
3. **Can you test health check timing** - does it fail before migration completes?
4. **Can you add grace period** to health check (return 200 for first 60 seconds)?
5. **Can you identify the minimal working fix** to unblock deployment?

---

## Recommended Approach

**Step 1**: Test health check change in isolation (Test 5)
**Hypothesis**: This is the breaking change due to timing issue

**Step 2**: If health check breaks deployment, test two solutions:
- **A)** Add startup grace period (health check returns 200 for first 60s)
- **B)** Make health check less strict (return 200 if database OK, even if prompt system not ready)

**Step 3**: Once health check fix identified, re-test combined deployment

**Step 4**: Verify fix resolves original "CSV prompts not found" error

---

## Handoff Complete

Awaiting NARs systematic modular testing and findings.

**Claude Code will not make further changes until NARs provides analysis.**
