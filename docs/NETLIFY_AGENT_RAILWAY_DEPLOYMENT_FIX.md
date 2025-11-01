# Railway Deployment Fix - For Netlify Agent Runners

**Date:** 2025-11-01  
**Issue:** Railway deployment failing with `python: command not found`  
**Status:** 🔴 BLOCKING - Deployment cannot start  
**Priority:** HIGH

---

## Executive Summary

Railway deployments are failing during container startup with error:
```
/bin/bash: line 1: python: command not found
```

This prevents any new deployments from going live. The **old deployment is still healthy** and serving requests, but **no new code can be deployed**.

---

## Error Details

**Deployment Logs Show:**
```
Starting Container
/bin/bash: line 1: python: command not found
/bin/bash: line 1: python: command not found
/bin/bash: line 1: python: command not found
/bin/bash: line 1: python: command not found
Stopping Container
```

**Error occurs:** During container startup, before application can run  
**Root cause:** Railway cannot find Python executable  
**Impact:** Zero successful deployments since Oct 31, 2025

---

## Diagnosis Steps

### Step 1: Verify Railway Root Directory Setting

**Problem:** Railway might be building from wrong directory (e.g., `mosaic_ui/` instead of repository root).

**Action:**
1. Open Railway Dashboard → Your Service → Settings → Source
2. Check **"Root Directory"** setting
3. **Should be:** Empty or `.` (repository root)
4. **If set to subdirectory:** Change to empty/root

**Why this matters:** If Railway builds from `mosaic_ui/`, it won't find `requirements.txt` in root and won't detect Python.

---

### Step 2: Verify Repository Structure

**Check that these files exist in repository root:**
```
what-is-my-delta-site/          # Railway source repository
├── api/                         # Python backend code
├── requirements.txt             # ✅ MUST EXIST (Python dependencies)
├── Procfile                     # ✅ MUST EXIST (startup command)
├── railway.toml                 # Railway configuration
└── frontend/                    # Frontend code
```

**Action:**
```bash
# Verify in Railway repository (what-is-my-delta-site)
cd /path/to/what-is-my-delta-site
ls -la requirements.txt Procfile api/
```

**Expected:**
- ✅ `requirements.txt` exists at root
- ✅ `Procfile` exists at root
- ✅ `api/` directory exists with Python code

---

### Step 3: Check for nixpacks.toml Interference

**Problem:** Previous attempts added `nixpacks.toml` which may be interfering with auto-detection.

**Action:**
```bash
# Check if nixpacks.toml exists
ls -la nixpacks.toml

# If it exists, check contents
cat nixpacks.toml
```

**NARs Recommendation (from 2025-10-31):**
- **Remove `nixpacks.toml`** if it exists
- **Let Railway auto-detect** Python from `requirements.txt`
- Railway's auto-detection works better than manual nixpacks config

**Fix:**
```bash
git rm nixpacks.toml
git commit -m "Remove nixpacks.toml - let Railway auto-detect Python"
git push railway-origin main
```

---

### Step 4: Verify Procfile Content

**Check Procfile is correct:**

```bash
cat Procfile
```

**Expected content:**
```
web: python -m uvicorn api.index:app --host 0.0.0.0 --port $PORT --workers 1 --timeout-keep-alive 120
```

**Note:** Procfile uses `python -m uvicorn`. If Railway can't find `python`, this will fail. Railway should auto-detect Python from `requirements.txt` and make `python` available.

**If incorrect:** Railway won't know how to start the application.

---

### Step 5: Verify requirements.txt Has Python Runtime

**Check requirements.txt includes necessary packages:**

```bash
head -20 requirements.txt
```

**Should include:**
- `fastapi`
- `gunicorn`
- `uvicorn`
- All other dependencies

**Railway auto-detects Python when it sees `requirements.txt`.**

---

## Recommended Fix Sequence

### Option A: Fix Root Directory (Most Likely)

1. **Railway Dashboard:** Settings → Source → Root Directory
   - Set to: **Empty** (or `.`)
   - Save changes

2. **Trigger redeploy:**
   ```bash
   # Make trivial change to force rebuild
   echo "# $(date)" >> README.md
   git add README.md
   git commit -m "Trigger deployment after root directory fix"
   git push railway-origin main
   ```

3. **Monitor deployment:** Check Railway logs for Python detection

---

### Option B: Remove nixpacks.toml (If Present)

1. **Remove file:**
   ```bash
   git rm nixpacks.toml
   git commit -m "Remove nixpacks.toml - let Railway auto-detect"
   git push railway-origin main
   ```

2. **Monitor deployment**

---

### Option C: Verify Repository Sync

**Problem:** Railway might be building from stale/incorrect repository state.

**Check:**
1. Verify Railway is connected to: `DAMIANSEGUIN/what-is-my-delta-site`
2. Verify latest commits are present in Railway repository
3. Force rebuild if needed (Railway dashboard → Redeploy)

---

## What NOT To Do

❌ **DON'T:** Modify `nixpacks.toml` to fix Python path  
❌ **DON'T:** Add more buildpack configurations  
❌ **DON'T:** Change `Procfile` to use `python3` instead of `python`  
❌ **DON'T:** Guess at solutions - follow NARs diagnosis

**Previous failed attempts:**
- Added `nixpacks.toml` with python311 → Still failed
- Added `python311Packages.pip` → Still failed
- Changed to `python -m pip` → Still failed

**These didn't work because Railway isn't detecting Python at all.**

---

## Verification Steps

After applying fix:

1. **Watch deployment logs** in Railway dashboard
   - Look for: "Detected Python" or "Installing Python"
   - Should NOT see: "python: command not found"

2. **Check container starts:**
   ```
   Starting Container
   Detected Python 3.x
   Installing dependencies...
   Starting application...
   ```

3. **Verify health check:**
   ```bash
   curl https://what-is-my-delta-site-production.up.railway.app/health
   ```
   Should return: `{"ok": true, ...}`

---

## Context

**Source Repository:** `DAMIANSEGUIN/what-is-my-delta-site`  
**Working Repository:** `DAMIANSEGUIN/wimd-railway-deploy` (we push to `railway-origin`)

**Git Remote:**
```bash
railway-origin → https://github.com/DAMIANSEGUIN/what-is-my-delta-site.git
```

**Current Status:**
- ✅ Old deployment: Healthy (serving requests)
- ❌ New deployments: Failing (can't start container)

**Previous Expert Diagnosis (NARs, 2025-10-31):**
> "Railway likely building from wrong directory. Check Railway Root Directory setting. Remove nixpacks.toml and let Railway auto-detect from requirements.txt."

---

## Success Criteria

✅ Deployment completes without "python: command not found"  
✅ Container starts successfully  
✅ Health endpoint returns 200  
✅ New code changes deploy successfully

---

## Files to Check

1. **Railway Dashboard:**
   - Settings → Source → Root Directory
   - Deployments → Latest → Logs

2. **Repository (`what-is-my-delta-site`):**
   - `requirements.txt` (root directory) - ✅ Exists, contains FastAPI/uvicorn/gunicorn
   - `Procfile` (root directory) - ✅ Exists, uses `python -m uvicorn`
   - `api/index.py` (Python entry point) - ✅ Exists
   - `railway.toml` - ✅ Exists, builder set to "nixpacks"
   - `nixpacks.toml` - ❓ Check if exists (should be removed per NARs recommendation)

---

## Questions?

- **Repository location:** Check `railway-origin` remote in local repo
- **Railway dashboard:** https://railway.app/dashboard
- **Health check:** https://what-is-my-delta-site-production.up.railway.app/health

---

**Created:** 2025-11-01  
**For:** Netlify Agent Runners (Railway infrastructure fix)  
**Reference:** RAILWAY_DEPLOYMENT_FACTS.md (previous diagnosis)

