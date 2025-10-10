# CODEX Handoff - Systematic Deployment Recovery Plan

**From**: Claude Code (Infrastructure Debugger)
**To**: CODEX (Systematic Planning Engineer)
**Date**: 2025-10-09
**Type**: Planning Request (NOT Implementation)
**Priority**: CRITICAL - Production stuck on 3-day-old code

---

## Problem Statement

Railway deployments are failing despite successful builds. Need systematic analysis to identify root cause and create minimal fix plan.

**Current state**: Railway runs old deployment (a583d26a Oct 6) successfully
**Failed attempts**: Multiple deployments (Oct 8-9) fail health checks
**Impact**: User cannot test fixes for "CSV prompts not found" error

---

## Working vs Failing Comparison

### Working Deployment (Baseline)
**Commit**: `067f33a` (Oct 7, 2025)
**Status**: ✅ Active on Railway production
**Health response**: `{"ok": true, "timestamp": "..."}`
**Characteristics**:
- Simple health check (no validation)
- No AI client initialization
- No feature flag migration system
- No monitoring infrastructure

### Failed Deployments
**Commits**: `7c2807e`, `2888657` (Oct 9)
**Build**: ✅ Succeeds
**Deploy**: ❌ Fails health check (503)
**Railway action**: Keeps old deployment active

**Failure pattern**:
1. Build completes successfully
2. Container starts
3. Health check hits `/health` endpoint
4. Returns 503 Service Unavailable
5. Railway marks deployment failed
6. Old deployment remains active

---

## Changes Made (067f33a → 2888657)

### 1. AI Client Initialization
**File**: `api/ai_clients.py` (commit ee6712f)
**Change**: Uncommented imports, initialize if API keys present

```python
# BEFORE
# import openai
# from anthropic import Anthropic
self.openai_client = None
self.anthropic_client = None

# AFTER
try:
    import openai
    from anthropic import Anthropic
    AI_PACKAGES_AVAILABLE = True
except ImportError:
    AI_PACKAGES_AVAILABLE = False

if self.settings.OPENAI_API_KEY:
    self.openai_client = openai
if self.settings.CLAUDE_API_KEY:
    self.anthropic_client = Anthropic(api_key=...)
```

### 2. Database Migration System
**Files**: `api/migrations.py`, `api/startup_checks.py` (commit 79f9395)
**Change**: Added migration 004 to sync feature flags, runs at startup

```python
# startup_checks.py (lines 36-54)
async def run():
    init_db()

    # Run migration to sync feature flags from JSON to database
    result = run_migration("004_sync_feature_flags_from_json", dry_run=False)

    cleanup_expired_sessions()
```

**Migration SQL**:
```sql
UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'AI_FALLBACK_ENABLED';
UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'RAG_BASELINE';
-- ... more flags
```

### 3. Feature Flag Caching Fix
**File**: `api/prompt_selector.py` (commit 6d7e578)
**Change**: Removed cached flag value, check dynamically

```python
# BEFORE
def __init__(self):
    self.fallback_enabled = self._check_feature_flag("AI_FALLBACK_ENABLED")  # Cached

# AFTER
def __init__(self):
    # Don't cache feature flag - check dynamically
    pass

# All usages now call _check_feature_flag() dynamically
```

### 4. Boolean Conversion Fix
**File**: `api/prompt_selector.py:34` (commit 7c2807e)
**Change**: Force SQLite integer to Python boolean

```python
# BEFORE
return row and row[0] if row else False  # Returns 0 or 1

# AFTER
return bool(row[0]) if row else False  # Converts to True/False
```

**Rationale**: SQLite BOOLEAN returns integers 0/1, Python evaluates `0 or False` as `False`

### 5. Enhanced Health Check
**File**: `api/index.py:423-489` (commits 027eaf2, 7c2807e)
**Change**: Added validation logic that returns 503 if system unhealthy

```python
# BEFORE
@app.get("/health")
def health():
    return {"ok": True, "timestamp": datetime.utcnow().isoformat() + "Z"}

# AFTER
@app.get("/health")
def health():
    prompt_health = get_prompt_health()
    fallback_enabled = prompt_health.get("fallback_enabled", False)
    ai_available = prompt_health.get("ai_health", {}).get("any_available", False)

    prompt_system_ok = fallback_enabled or ai_available
    db_ok = True  # database check
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

### 6. Monitoring System
**File**: `api/monitoring.py` (commit 027eaf2)
**Change**: Added 199-line monitoring module

**Import** in `api/index.py:46`:
```python
from .monitoring import run_health_check, attempt_system_recovery
```

### 7. Railway Configuration
**File**: `railway.toml` (commit 027eaf2)
**Change**: Added health check configuration

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

---

## Root Cause Hypothesis

**Timing issue between health check and startup migration:**

```
Timeline:
1. Railway starts container                     (t=0s)
2. FastAPI begins accepting requests            (t=2s)
3. Railway hits /health endpoint                (t=3s)  ← HEALTH CHECK STARTS
4. Startup event runs migration                 (t=3s)  ← MIGRATION BEGINS
5. Health check reads database                  (t=3s)  ← Sees old value (0)
6. Health check evaluates: 0 or False = False   (t=3s)
7. Health check returns 503                     (t=3s)  ← FAILS
8. Migration completes, updates DB to 1         (t=5s)  ← TOO LATE
9. Railway marks deployment failed              (t=8s)
```

**Evidence**:
- Deploy logs show: "✅ Migration executed successfully"
- Deploy logs show: "✅ Feature flags synced to database"
- Deploy logs also show: `INFO: "GET /health HTTP/1.1" 503 Service Unavailable`
- 14 health check attempts over 5 minutes, all return 503
- Deployment fails despite migration succeeding

**The problem**: Health check validation happens BEFORE migration updates the database.

---

## Alternative Hypotheses

### Hypothesis 2: Boolean conversion doesn't work
- SQLite still returning integer despite `bool()` wrapper
- Health check still evaluating `0 or False` as `False`

### Hypothesis 3: AI clients fail to initialize
- API keys not set in Railway environment
- Import errors preventing initialization
- Health check sees `ai_available: false` always

### Hypothesis 4: Migration fails silently
- Migration says "success" but doesn't actually update database
- Database permissions issue
- SQLite file locking problem

### Hypothesis 5: Wrong code deployed
- Railway cache serving old code
- New commits not actually in deployed container
- Git push didn't reach Railway repository

---

## Request for CODEX

**DO NOT IMPLEMENT. PROVIDE SYSTEMATIC ANALYSIS AND PLAN.**

### Task 1: Identify Root Cause

**Question**: Which of the 7 changes is breaking deployment?

**Approach**:
1. Review working deployment code (`067f33a`)
2. Compare to failing deployment code (`2888657`)
3. Analyze each change's impact on startup sequence
4. Determine most likely culprit

**Deliverable**: Ranked list of suspected breaking changes with rationale

---

### Task 2: Create Isolation Test Plan

**Question**: How to test each change independently?

**Approach**:
1. Define 7-8 test branches (one change each)
2. Specify exact files to modify per test
3. Define expected outcome for each test
4. Prioritize tests by likelihood of being the problem

**Deliverable**: Step-by-step test plan with commands

---

### Task 3: Design Minimal Fix

**Question**: What's the smallest change to unblock deployment?

**Constraints**:
- Must pass Railway health check
- Must preserve original bug fixes (bool conversion, AI clients, migration)
- Must be reversible if it doesn't work

**Options to evaluate**:

**Option A: Health Check Grace Period**
```python
# First 60 seconds always return 200
startup_time = time.time()

@app.get("/health")
def health():
    if time.time() - startup_time < 60:
        return {"ok": True, "timestamp": "...", "grace_period": True}
    # ... normal validation
```

**Option B: Relaxed Health Check**
```python
# Only require database, not prompt system
@app.get("/health")
def health():
    db_ok = check_database()
    # Return 200 if database works, even if prompt system not ready
    return {"ok": db_ok, "timestamp": "..."}
```

**Option C: Run Migration Before FastAPI Starts**
```python
# Move migration to main entry point, not startup event
# Ensures DB updated before health checks begin
```

**Option D: Revert to Simple Health Check Temporarily**
```python
# Deploy with working code + fixes, but without strict health check
# Get deployment live, then add health check in follow-up
```

**Deliverable**: Recommended fix with exact code changes and rationale

---

### Task 4: Create Deployment Run Sheet

**Question**: Exact steps for Claude Code to execute deployment?

**Format**:
```
Step 1: Create test branch
  Command: git checkout -b test-health-grace-period 067f33a

Step 2: Apply minimal fix
  File: api/index.py
  Change: [exact diff]

Step 3: Commit and push
  Command: git commit -m "..." && git push railway-origin test-health-grace-period

Step 4: Deploy to Railway
  Command: railway up --detach

Step 5: Monitor deployment
  Check: Railway dashboard for build/deploy status
  Expected: Health check passes, deployment goes live

Step 6: Validate fix
  Test: curl https://... /health
  Expected: {"ok": true, ...}
```

**Deliverable**: Complete run sheet for deployment execution

---

## Files for CODEX Review

**Working deployment**:
```bash
git show 067f33a:api/index.py          # Simple health check
git show 067f33a:api/ai_clients.py     # Commented imports
git show 067f33a:api/prompt_selector.py # Original code
```

**Failed deployment**:
```bash
git show 2888657:api/index.py          # Enhanced health check
git show 2888657:api/ai_clients.py     # Initialized clients
git show 2888657:api/prompt_selector.py # Bool conversion
git show 2888657:api/startup_checks.py  # Migration system
```

**Diff summary**:
```bash
git diff 067f33a..2888657 --stat
# 21 files changed, 451 insertions(+), 19 deletions(-)
```

---

## Environment Context

**Railway Project**: wimd-career-coaching
**Service**: what-is-my-delta-site
**Environment**: production
**Repository**: https://github.com/DAMIANSEGUIN/what-is-my-delta-site
**Branch**: main

**Working directory**: `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/`

**Git remotes**:
- `origin`: wimd-railway-deploy.git (wrong repo)
- `railway-origin`: what-is-my-delta-site.git (correct repo)

**Deployment method**: `railway up` or `railway redeploy`

---

## Success Criteria

**Immediate**:
1. CODEX identifies most likely breaking change
2. CODEX provides minimal fix plan
3. CODEX creates executable run sheet
4. Plan approved by human before implementation

**Validation**:
1. Deployment succeeds (health check passes)
2. Production serves new code
3. Original "CSV prompts not found" error resolved
4. System stable and healthy

---

## Protocol Reminder

**CODEX Role**: Systematic planning, not implementation
**Claude Code Role**: Execute CODEX's plan with human approval

**Process**:
1. CODEX analyzes and creates plan
2. CODEX presents plan to human
3. Human reviews and approves
4. Claude Code executes approved plan
5. Report results back to CODEX

**DO NOT**:
- Implement code changes directly
- Deploy without human approval
- Make assumptions about environment
- Skip systematic analysis

---

## Reference Documents

**In project directory**:
1. `CODEX_HANDOFF_HEALTH_CHECK_2025-10-09.md` - Previous technical analysis
2. `NARS_HANDOFF_MODULAR_TESTING_2025-10-09.md` - Detailed modular test plan
3. `CLAUDE_CODE_DEBUGGING_REPORT_2025-10-08.md` - Original issue investigation
4. `CODEX_INSTRUCTIONS.md` - Role definitions and protocols

---

## Expected CODEX Deliverables

1. **Root Cause Analysis** (1-2 paragraphs)
2. **Isolation Test Plan** (prioritized list with commands)
3. **Minimal Fix Recommendation** (exact code changes)
4. **Deployment Run Sheet** (step-by-step execution plan)
5. **Risk Assessment** (what could go wrong, rollback plan)

**Format**: Exact file diffs + Run Sheet (no prose explanations unless critical)

**Timeframe**: Systematic analysis required, not rushed implementation

---

## Handoff Complete

Awaiting CODEX systematic analysis and deployment recovery plan.

**Claude Code will execute plan only after human approval.**
