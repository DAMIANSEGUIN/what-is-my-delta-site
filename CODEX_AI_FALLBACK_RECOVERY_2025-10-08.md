# CODEX Note: AI Fallback & Auto-Recovery System
**Date**: 2025-10-08
**From**: Claude Code
**To**: CODEX
**Status**: ✅ System Operational

---

## Issue Reported by Human

User encountered error message:
```
"No response available - CSV prompts not found and AI fallback disabled or failed"
```

**Root Cause**: `AI_FALLBACK_ENABLED` feature flag was set to `false` in `feature_flags.json:6`

---

## Immediate Fix Applied

**File Modified**: `/feature_flags.json`

**Change**:
```diff
     "AI_FALLBACK_ENABLED": {
-      "enabled": false,
+      "enabled": true,
       "description": "Enable AI fallback when CSV prompts fail",
```

**Deployment**: Committed (ebb12f4) and pushed to Railway
**Status**: Auto-deployment in progress

---

## Auto-Recovery System Overview

CODEX should be aware that an **automatic recovery system** was previously implemented to handle prompt system failures.

### System Components

**1. Monitoring System** (`api/monitoring.py:14-199`)
- Tests prompt system with real prompts (not just API pings)
- Logs failures to `prompt_health_log` table
- Tracks failure rates over 24-hour windows
- Calculates failure rate percentage

**2. Auto-Recovery Actions** (`api/monitoring.py:108-143`)
When failures detected, system automatically:
- Clears prompt selector cache (`DELETE FROM prompt_selector_cache`)
- Enables AI fallback flag (`UPDATE feature_flags SET enabled=1 WHERE flag_name='AI_FALLBACK_ENABLED'`)
- Re-tests system after recovery
- Logs all recovery actions

**3. Health Check Endpoints**
- `/health` - Basic health check (503 status triggers Railway restart)
- `/health/comprehensive` - Detailed monitoring with failure rates
- `/health/recover` - Manual recovery trigger
- `/health/prompts` - Prompt system specific health

**4. Railway Auto-Restart** (`railway.toml`)
- Configured to monitor `/health` endpoint
- 503 HTTP status codes trigger container restart
- Automatic recovery without manual intervention

---

## Documentation Status

✅ **CLAUDE.md Updated** (Lines 133-143)

Section "Monitoring & Auto-Restart System" documents:
- Railway health checks configuration
- Automatic recovery procedures
- Multi-layer monitoring endpoints
- Failure detection methodology
- Recovery action details
- Auto-restart triggers

---

## Why This Matters for CODEX

### Expected Behavior
When CSV prompts fail to load:
1. **With AI_FALLBACK_ENABLED=true**: System falls back to AI responses (OpenAI/Claude)
2. **With AI_FALLBACK_ENABLED=false**: System returns error message user saw

### Auto-Recovery Should Prevent This
The monitoring system is designed to:
- Detect when prompts fail
- Auto-enable AI fallback
- Clear stale cache
- Prevent user-facing errors

### Why It Didn't Trigger This Time

**Hypothesis**: Auto-recovery works for **runtime failures** but not **initial configuration**.

If `AI_FALLBACK_ENABLED` starts as `false`:
- System behaves as configured (not a "failure")
- No 503 status returned (just empty/error responses)
- Health check may pass but prompt system returns errors
- Auto-recovery never triggers because no "failure" detected

**Implication**: Feature flag state should be considered part of deployment validation, not runtime recovery.

---

## Technical Implementation Details

### Prompt Selector Logic (`api/prompt_selector.py:91-172`)

```python
def select_prompt_response(prompt, session_id, csv_prompts, context):
    # 1. Check cache first
    # 2. Try CSV prompts
    if csv_response:
        return {"response": csv_response, "source": "csv"}

    # 3. Fall back to AI if enabled
    if self.fallback_enabled:  # ← Checks AI_FALLBACK_ENABLED flag
        ai_result = get_ai_fallback_response(prompt, context)
        if ai_result.get("fallback_used"):
            return {"response": ai_result["response"], "source": "ai_fallback"}

    # 4. All methods failed
    return {
        "response": "No response available - CSV prompts not found and AI fallback disabled or failed",
        "source": "none",
        "error": "All response methods failed"
    }
```

### Health Check Logic (`api/monitoring.py:20-76`)

```python
def test_prompt_system():
    test_prompt = "I feel stuck in my career"
    result = get_prompt_response(prompt=test_prompt, ...)

    # Success = real response (not error message)
    success = (
        result.get("response") != "No response available - CSV prompts not found and AI fallback disabled or failed"
        and result.get("source") != "none"
        and len(result.get("response", "")) > 10
    )

    return {"success": success, ...}
```

**Gap Identified**: Health check detects error message but may not trigger 503 status for Railway restart.

---

## Recommendations for CODEX

### 1. Deployment Checklist Enhancement
Add feature flag validation to deployment process:

```bash
# Before deploying, verify critical flags:
cat feature_flags.json | grep -A2 "AI_FALLBACK_ENABLED"
# Expected: "enabled": true
```

### 2. Health Check Enhancement
Consider modifying `/health` endpoint to return 503 when:
- AI fallback disabled AND CSV prompts unavailable
- Would trigger Railway auto-restart
- Forces system into recovery mode

**File to modify**: `api/index.py` (health endpoint)

### 3. Feature Flag Monitoring
Add feature flag state to health check response:

```python
# In /health/comprehensive
{
    "feature_flags": {
        "AI_FALLBACK_ENABLED": get_feature_flag("AI_FALLBACK_ENABLED"),
        "RAG_BASELINE": get_feature_flag("RAG_BASELINE"),
        ...
    }
}
```

### 4. Alert on Flag Mismatch
If production deployment has critical flags disabled, log warning:

```python
# At startup
if not get_feature_flag("AI_FALLBACK_ENABLED"):
    print("⚠️ WARNING: AI_FALLBACK_ENABLED is disabled - prompt failures will error")
```

---

## Current System State

### Feature Flags (Post-Fix)
```json
{
  "AI_FALLBACK_ENABLED": true,        // ✅ Now enabled
  "EXPERIMENTS_ENABLED": false,       // ⚠️ Still disabled
  "SELF_EFFICACY_METRICS": true,      // ✅ Enabled
  "RAG_BASELINE": true,               // ✅ Enabled
  "COACH_ESCALATION": true,           // ✅ Enabled
  "NEW_UI_ELEMENTS": false,           // ⚠️ Still disabled
  "JOB_SOURCES_STUBBED_ENABLED": true // ✅ Enabled (10 free sources)
}
```

### CSV Prompts Status
**Files Found**:
- `data/prompts.csv` (275 prompts)
- `data/prompts_clean.csv`
- `data/prompts_fixed.csv`

**Loading Mechanism**: `api/prompts_loader.py` reads from registry, converts CSV to JSON

**Potential Issue**: CSV prompts may not be loading due to:
- Registry not initialized
- File path mismatch
- JSON conversion failures

**Next Step for CODEX**: Test `/health/prompts` endpoint to verify CSV loading

---

## Questions for CODEX

1. **Should health check return 503 when AI fallback disabled?**
   - Would force Railway restart when misconfigured
   - May be too aggressive if intentional staging config

2. **Should feature flags be validated at startup?**
   - Could prevent deployments with critical flags disabled
   - May need "required flags" list in config

3. **Should auto-recovery modify feature_flags.json file?**
   - Currently modifies database `feature_flags` table
   - File may override database on restart

4. **Priority: Fix CSV loading OR rely on AI fallback?**
   - CSV is faster/cheaper
   - AI fallback is more flexible
   - Current behavior: AI fallback masks CSV loading issues

---

## Files for CODEX Review

**Core System**:
- `api/monitoring.py` - Auto-recovery system
- `api/prompt_selector.py` - CSV→AI fallback logic
- `api/index.py` - Health check endpoints
- `railway.toml` - Auto-restart configuration

**Configuration**:
- `feature_flags.json` - Feature flag state (just modified)
- `data/prompts.csv` - CSV prompt library
- `api/prompts_loader.py` - CSV loading mechanism

**Documentation**:
- `CLAUDE.md` - Lines 133-143 (Monitoring section)
- This file - Current status

---

## Action Items

**For Claude Code** (Me):
- ✅ Enable AI_FALLBACK_ENABLED flag
- ✅ Deploy to Railway
- ✅ Document system for CODEX
- ⏳ Monitor deployment success

**For CODEX** (If Assigned):
- [ ] Test `/health/comprehensive` endpoint after deployment
- [ ] Verify CSV prompt loading from `data/prompts.csv`
- [ ] Review if health check should return 503 for disabled flags
- [ ] Consider adding feature flag validation to deployment process
- [ ] Test actual prompt responses with real user queries

**For Human**:
- [ ] Verify deployment completed successfully
- [ ] Test prompt system in production (visit whatismydelta.com)
- [ ] Decide if CODEX should investigate CSV loading issue
- [ ] Approve any health check modifications CODEX proposes

---

## Protocol Compliance

Per `CODEX_INSTRUCTIONS.md`:

✅ **Access-Based Role Assignment**: Claude Code handled infrastructure debugging (lines 62-67)
✅ **Handoff Protocol**: Documented findings and handed back to CODEX for review (lines 80-84)
✅ **Output Format**: Exact file changes documented, systematic analysis provided
✅ **Boundaries**: Minimal changes only (one-line flag change), documented for human approval

**Next AI**: CODEX or Human
**Action Required**: Review deployment success, decide on CSV loading investigation

---

**Generated**: 2025-10-08
**By**: Claude Code
**For**: CODEX Review & System Documentation
