# Railway Deployment Health Check Debugging

**Issue:** New Railway deployments failing with "service unavailable" errors during health checks.

**Current Status:**
- ✅ Old deployment: Healthy and serving requests
- ❌ New deployment: Failing health checks repeatedly (12+ attempts)

## Immediate Action Needed

### 1. Check Railway Dashboard

**Go to:** Railway Dashboard → Your Service → Deployments → Latest Failed Deployment

**Look for:**
- **Build Logs:** Did the build succeed?
- **Deploy Logs:** What errors appear during startup?
- **Health Check Logs:** What response is `/health` returning?

### 2. Common Causes

#### A. Health Check Timing Issue
**Symptom:** Health checks failing before prompt system is ready

**Evidence to look for:**
```
INFO: "GET /health HTTP/1.1" 503 Service Unavailable
```

**Check deploy logs for:**
- Is `SERVICE_READY.set()` called?
- Does startup complete successfully?
- What does `get_prompt_health()` return?

#### B. Prompt System Not Ready
**Symptom:** `fallback_enabled=False` AND `ai_available=False` during health check

**Root cause:** Health check runs AFTER `SERVICE_READY.set()` but BEFORE prompt system is fully initialized.

**Fix needed:** Health check should have longer grace period or check should be more lenient during first few minutes.

#### C. Database Connection Issue
**Symptom:** Database connectivity check failing

**Evidence:**
- `"database": false` in health check response
- Connection errors in deploy logs

### 3. Possible Solutions

#### Option 1: Extend Grace Period
Modify health check to accept "initializing" status longer:

```python
# In api/index.py health() function
# Current: Returns "initializing" only if SERVICE_READY not set
# Better: Add time-based grace period (first 60 seconds always ok)
```

#### Option 2: Make Health Check More Lenient During Deployment
Accept health check as "ok" if SERVICE_READY is not set (current behavior), OR if less than 2 minutes since startup.

#### Option 3: Fix Prompt Health Check
Ensure `get_prompt_health()` returns correct values immediately after startup.

### 4. Debugging Steps

1. **Enable Health Debug Logging:**
   ```bash
   # In Railway environment variables
   HEALTH_DEBUG=true
   ```

2. **Check Startup Sequence:**
   Look in deploy logs for:
   ```
   Starting up...
   ✅ Feature flags synced to database
   Settings loaded successfully
   Startup complete
   SERVICE_READY.set()
   ```

3. **Check Health Check Responses:**
   Look for health check attempts in deploy logs:
   ```
   INFO: "GET /health HTTP/1.1" 503 Service Unavailable
   ```
   
   What is the response body? Should see:
   ```json
   {
     "ok": false,
     "checks": {
       "database": true/false,
       "prompt_system": true/false,
       "ai_fallback_enabled": true/false,
       "ai_available": true/false
     }
   }
   ```

### 5. Quick Fix (If Health Check Too Strict)

If health check is failing because prompt system isn't ready yet:

**Temporary workaround:** Make health check always return 200 during first 2 minutes after SERVICE_READY:

```python
STARTUP_TIME = time.time()

@app.get("/health")
def health():
    if not SERVICE_READY.is_set():
        return {"ok": True, "status": "initializing"}
    
    # Grace period: first 2 minutes after startup, always pass
    if time.time() - STARTUP_TIME < 120:
        return {
            "ok": True,
            "status": "starting",
            "checks": {"grace_period": True},
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    # ... rest of health check logic
```

### 6. Next Steps

1. **Check Railway dashboard** to see actual error
2. **Review deploy logs** for startup sequence
3. **Check health check response** in failed attempts
4. **Apply appropriate fix** based on what you find

---

**Last Updated:** 2025-11-01
**Status:** Awaiting Railway dashboard review

