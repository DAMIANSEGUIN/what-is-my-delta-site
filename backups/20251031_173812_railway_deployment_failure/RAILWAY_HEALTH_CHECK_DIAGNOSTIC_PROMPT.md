# Railway Deployment Health Check Failure - Diagnostic Prompt

## Problem Statement
Railway deployment builds successfully and starts up correctly with all components initialized, but health check returns 503 causing deployment failure and rollback to old version.

## Current Deployment Status
- **Active (Old)**: Deployment from Oct 6, 2025 (commit a583d26a) - healthy but missing fixes
- **Failed (New)**: Deployment from Oct 9, 2025 (commit 80155006) - has all fixes but fails health check

## Evidence from Deploy Logs (New Deployment)

### ✅ Successful Startup Sequence
```
Starting Container
✅ OpenAI client initialized
✅ Anthropic client initialized
INFO: Started server process [1]
INFO: Waiting for application startup.
Starting up...
Running feature flag sync migration...
🚀 Executing migration: 004_sync_feature_flags_from_json
✅ Backup created: data/migration_backups/backup_20251009_140625_004_sync_feature_flags_from_json.db
✅ Migration executed successfully
✅ Feature flags synced to database
Settings loaded successfully
Anthropic API ping successful
OpenAI API ping successful
Startup complete
INFO: Application startup complete.
```

### ❌ Health Check Failures (14 attempts, all 503)
```
INFO: 100.64.0.2:60093 - "GET /health HTTP/1.1" 503 Service Unavailable
INFO: 100.64.0.2:49883 - "GET /health HTTP/1.1" 503 Service Unavailable
[... 12 more identical failures ...]
```

## Health Check Logic (api/index.py:420-471)

```python
@app.get("/health")
def health():
    prompt_health = get_prompt_health()

    fallback_enabled = prompt_health.get("fallback_enabled", False)
    ai_available = prompt_health.get("ai_health", {}).get("any_available", False)

    prompt_system_ok = fallback_enabled or ai_available
    db_ok = True  # (database check)
    overall_ok = prompt_system_ok and db_ok

    if not overall_ok:
        raise HTTPException(status_code=503, detail=health_status)

    return health_status
```

**Health check fails if**: `(fallback_enabled == False OR None) AND (ai_available == False)`

## What Old Deployment Shows (Still Active)

Query: `https://whatismydelta.com/health/prompts`
```json
{
  "ok": true,
  "prompt_selector": {
    "fallback_enabled": 0,
    "ai_health": {
      "openai": {"available": false},
      "anthropic": {"available": false},
      "any_available": false
    }
  }
}
```

## Fixes Already Applied (In New Deployment)

### 1. AI Client Initialization (api/ai_clients.py)
```python
# BEFORE: imports commented out
# import openai
# from anthropic import Anthropic

# AFTER: imports uncommented with try/except
try:
    import openai
    from anthropic import Anthropic
    AI_PACKAGES_AVAILABLE = True
except ImportError:
    AI_PACKAGES_AVAILABLE = False
```

### 2. Feature Flag Sync Migration (api/migrations.py:221-227)
```python
"004_sync_feature_flags_from_json": """
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'AI_FALLBACK_ENABLED';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'RAG_BASELINE';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'SELF_EFFICACY_METRICS';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'COACH_ESCALATION';
    UPDATE feature_flags SET enabled = TRUE WHERE flag_name = 'JOB_SOURCES_STUBBED_ENABLED';
"""
```

### 3. Dynamic Feature Flag Checking (api/prompt_selector.py:22)
```python
# BEFORE: cached at init
self.fallback_enabled = self._check_feature_flag("AI_FALLBACK_ENABLED")

# AFTER: check dynamically each time
# Don't cache feature flag - check dynamically to allow runtime updates
```

## Key Questions

1. **Why does new deployment return 503 when logs show everything initialized?**
   - AI clients initialized successfully
   - Migration ran successfully
   - Database updated successfully
   - API pings successful

2. **What is the health check actually seeing at runtime?**
   - Need to log `fallback_enabled` and `ai_available` values in health check
   - Possible the values are different than expected

3. **Could there be a module initialization order issue?**
   - `ai_client_manager` is global instance created at module import time
   - Migration runs during FastAPI startup event
   - Health checks happen after startup completes
   - Timeline should be correct

4. **Could there be a database transaction/persistence issue?**
   - Migration creates backup, then updates original database
   - Could SQLite connection be reading stale data?
   - Could Railway volume mounting cause database file confusion?

## Recommended Diagnostic Steps

### Step 1: Add Debug Logging to Health Check
Modify `api/index.py` health check to log actual values:

```python
@app.get("/health")
def health():
    prompt_health = get_prompt_health()

    fallback_enabled = prompt_health.get("fallback_enabled", False)
    ai_available = prompt_health.get("ai_health", {}).get("any_available", False)

    # DEBUG LOGGING
    print(f"🔍 Health check values:")
    print(f"   fallback_enabled: {fallback_enabled}")
    print(f"   ai_available: {ai_available}")
    print(f"   prompt_health: {prompt_health}")

    prompt_system_ok = fallback_enabled or ai_available
    # ... rest of logic
```

### Step 2: Verify AI Client Manager State
Add diagnostic endpoint to check actual client state:

```python
@app.get("/debug/ai-clients")
def debug_ai_clients():
    from .ai_clients import ai_client_manager
    return {
        "openai_client_type": str(type(ai_client_manager.openai_client)),
        "openai_client_is_none": ai_client_manager.openai_client is None,
        "anthropic_client_type": str(type(ai_client_manager.anthropic_client)),
        "anthropic_client_is_none": ai_client_manager.anthropic_client is None,
        "health_status": ai_client_manager.get_health_status()
    }
```

### Step 3: Verify Database Flag Value
Add diagnostic endpoint to check database directly:

```python
@app.get("/debug/feature-flags")
def debug_feature_flags():
    from .storage import get_conn
    with get_conn() as conn:
        rows = conn.execute("SELECT flag_name, enabled FROM feature_flags").fetchall()
    return {"flags": {row[0]: bool(row[1]) for row in rows}}
```

### Step 4: Alternative Solution - Temporary Health Check Bypass
If debugging shows all values are correct but health check still fails, consider:

```python
@app.get("/health")
def health():
    # TEMPORARY: Return 200 always to unblock deployment
    return {
        "ok": True,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "note": "Temporary bypass - remove after deployment succeeds"
    }
```

Then investigate why original health check logic fails despite correct initialization.

## Environment Details

- **Platform**: Railway (automated container deployment)
- **Database**: SQLite with file persistence (`data/mosaic.db`)
- **API Keys**: Set in Railway environment variables
  - `OPENAI_API_KEY`: ✅ Configured
  - `CLAUDE_API_KEY`: ✅ Configured
- **Python**: FastAPI application with uvicorn server
- **Volume**: Railway provides persistent volume for `data/` directory

## Success Criteria

Deployment is successful when:
1. Build completes ✅ (already working)
2. Container starts ✅ (already working)
3. Application startup completes ✅ (already working)
4. `/health` endpoint returns 200 OK ❌ (currently failing)
5. Railway promotes new deployment as active ❌ (blocked by #4)

## Files to Review

- `api/index.py` (lines 420-471) - Health check endpoint
- `api/prompt_selector.py` (lines 16-220) - Prompt selector and feature flag checking
- `api/ai_clients.py` (lines 22-210) - AI client initialization and health status
- `api/startup_checks.py` (lines 36-54) - Migration execution during startup
- `api/migrations.py` (lines 221-227) - Feature flag sync migration

## Repository & Deployment

- **Repo**: github.com/DAMIANSEGUIN/what-is-my-delta-site
- **Branch**: main
- **Remote**: railway-origin
- **Production URL**: https://whatismydelta.com
- **Railway Service**: what-is-my-delta-site-production
- **Last Working Commit**: a583d26a (Oct 6, 2025)
- **Current Failed Commit**: 80155006 (Oct 9, 2025)
