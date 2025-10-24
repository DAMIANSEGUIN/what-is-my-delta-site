# ESCALATION TO NARS - PostgreSQL Connection Issue

**Date:** 2025-10-14
**Status:** PostgreSQL provisioned but not connecting
**Session:** Claude Code PostgreSQL migration (90 min)

---

## Current Situation

**Migration Status:**
- ✅ Code migrated to PostgreSQL (committed: `2b9fbc1`)
- ✅ Railway PostgreSQL service provisioned
- ✅ DATABASE_URL added to app service environment variables
- ✅ App deployed successfully
- ❌ **App still using SQLite fallback - PostgreSQL connection failing**

**Evidence:**
- Deployment logs show: `data/migration_backups/backup_...db` (SQLite paths)
- User registration returns "Invalid credentials" (SQLite being wiped on deploy)
- No PostgreSQL connection errors in logs (failing silently)

---

## What NARs Needs to Do

### Step 1: Verify DATABASE_URL Configuration

**In Railway dashboard:**

1. Click on **PostgreSQL service**
2. Check **"Variables"** or **"Connect"** section
3. Look for **TWO possible connection strings:**
   - **Public URL:** `postgresql://...@something.railway.app:5432/railway`
   - **Private URL:** `postgresql://...@postgres.railway.internal:5432/railway`

4. **Copy the PRIVATE/INTERNAL network URL** (if available)

### Step 2: Update App Service DATABASE_URL

5. Click on **`what-is-my-delta-site` service**
6. Go to **"Variables"** section
7. **Edit** (not add new) the existing `DATABASE_URL` variable
8. **Replace** with the private network URL from Step 1
9. Save

### Step 3: Manual Redeploy

10. In `what-is-my-delta-site` service, go to **"Deployments"**
11. Click **"Redeploy"** or **"Deploy"** button
12. Wait ~2 minutes for build to complete

### Step 4: Verify Connection

13. Check deployment logs for:
    ```
    [STORAGE] Attempting PostgreSQL connection...
    [STORAGE] ✅ PostgreSQL connection pool created successfully
    ```

14. If you see `❌ PostgreSQL connection failed:` - **note the error message**

### Step 5: Test Persistence

15. Go to https://whatismydelta.com
16. Register test user: `nars-test@example.com` / `testpass123`
17. Verify login works
18. Trigger another deployment (any code change)
19. Try logging in again with same credentials
20. **Expected:** Login succeeds (user persisted)
21. **Old behavior:** "Invalid credentials" (user wiped)

---

## Alternative: Check Railway PostgreSQL Status

If private URL doesn't exist or connection still fails:

**Possible issues:**
1. PostgreSQL service not fully provisioned yet (wait 5 more minutes)
2. Network connectivity between services not configured
3. PostgreSQL credentials incorrect
4. PostgreSQL not accepting connections

**Check PostgreSQL service:**
- Status should be **"Active"** or **"Running"**
- Check **"Metrics"** - should show database activity
- Check **"Logs"** - look for initialization complete messages

---

## Debugging Information

**Current DATABASE_URL format (confirmed by user):**
- Starts with: `postgresql://`
- Ends with: `railway.app:5432/railway`

**Code Status:**
- `api/storage.py` has PostgreSQL connection pool initialization
- Fallback to SQLite if `DATABASE_URL` not set or connection fails
- Debug logging added (commit pending user approval)

**Files Changed:**
- `requirements.txt` - Added `psycopg2-binary`
- `api/storage.py` - PostgreSQL migration complete
- `api/storage_sqlite_backup.py` - Original SQLite backup

---

## If All Else Fails

**Rollback to SQLite:**
```bash
cp api/storage_sqlite_backup.py api/storage.py
sed -i '' '/psycopg2-binary/d' requirements.txt
git add api/storage.py requirements.txt
git commit -m "Rollback: PostgreSQL connection failed, restore SQLite"
git push railway-origin main
```

**Note:** This returns to the original problem (database wiped on every deploy).

---

## What Was Attempted

**Session work (90 minutes):**
1. ✅ Diagnosed root cause (Railway ephemeral SQLite storage)
2. ✅ Migrated all SQL queries to PostgreSQL syntax
3. ✅ Added connection pooling
4. ✅ Deployed code changes
5. ✅ Provisioned Railway PostgreSQL
6. ✅ Added DATABASE_URL to app service
7. ❌ **Connection not working - needs Railway dashboard troubleshooting**

**Claude Code limitation:**
- Cannot access Railway dashboard interactively
- Cannot view visual UI elements (tabs, panels, buttons)
- Cannot switch between Railway services via CLI in non-TTY mode
- **Requires human with dashboard access to complete final configuration**

---

## Expected Outcome

Once DATABASE_URL is correctly configured:
- PostgreSQL connection succeeds
- Database schema auto-created on first connection
- User accounts persist across deployments
- All authentication/session issues resolved
- Platform production-ready

---

**Status:** Awaiting NARs Railway dashboard configuration

**Estimated Time to Resolution:** 10 minutes (if DATABASE_URL just needs updating)
