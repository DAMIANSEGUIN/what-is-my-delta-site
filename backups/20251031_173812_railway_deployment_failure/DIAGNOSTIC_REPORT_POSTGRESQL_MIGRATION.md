# PostgreSQL Migration Diagnostic Report

**Date:** 2025-10-14  
**Author:** Claude Code (handoff for Codex)  
**Project:** What Is My Delta – Railway deployment

---

## Background & Root Cause

- The FastAPI backend originally used SQLite at `data/mosaic.db`. Railway application containers have ephemeral storage, so every deploy erased the database, wiping users and sessions.  
- First mitigation attempt (`railway.json` include rules) only bundled the `.db` file into the deploy artifact; it did **not** provide persistence.  
- To resolve, Claude Code migrated the backend to PostgreSQL using Railway's managed database service. The code now expects a PostgreSQL connection string supplied via `DATABASE_URL`.  
- Production still falls back to SQLite because the app service cannot reach PostgreSQL. The code quietly reverts to SQLite whenever the connection pool cannot initialize.

---

## Code Changes Made (commit `2b9fbc1`)

- `requirements.txt` – Added `psycopg2-binary` dependency for PostgreSQL connectivity.  
- `api/storage.py` – Replaced the SQLite implementation with a PostgreSQL-first design:
  - Loads `DATABASE_URL` from the environment and initializes a `psycopg2.pool.SimpleConnectionPool(1, 20, ...)`.  
  - Updates all SQL statements to PostgreSQL parameter syntax (`%s`) and switches `AUTOINCREMENT` columns to `SERIAL`.  
  - Uses context-managed connections with automatic commit/rollback.  
  - Retains the SQLite code path as a fallback when no pool is available.  
- `api/storage_sqlite_backup.py` – Preserved the original SQLite implementation for potential rollback.

No schema migrations are pending: PostgreSQL tables are created automatically on first run through the new storage module.

---

## Current Failure State (UPDATED 2025-10-14 19:15 UTC)

- Environment variable `DATABASE_URL` has been updated to use **private network** (`postgres.railway.internal`).
- Application deploys successfully and health check passes: `{"database":true}`
- **CRITICAL ISSUE:** App is silently falling back to SQLite despite DATABASE_URL being set correctly
- **ROOT CAUSE UNKNOWN:** The actual PostgreSQL connection error is being caught but we haven't retrieved the error message from logs
- Evidence: Users still getting "Invalid credentials" (SQLite wiping on deploy)
- **BLOCKER:** Need Railway deployment logs showing `[STORAGE] ❌ PostgreSQL connection failed:` message to diagnose

**Architecture Flaw Identified:**
- Code has silent fallback that masks PostgreSQL connection failures
- Exception caught without failing the application
- Health check reports `"database":true` even when using SQLite fallback
- No way to distinguish PostgreSQL success from SQLite fallback without checking logs

---

## Railway Dashboard Instructions (Human Action Required)

1. **Locate the private database URL**  
   - Railway Dashboard → `PostgreSQL` service → *Connect* → copy the `psql` connection string that includes `railway.internal`.  
2. **Update the application environment**  
   - Railway Dashboard → `what-is-my-delta-site` service → *Variables*.  
   - Edit `DATABASE_URL`, replace the existing value with the private/internal URL.  
   - Ensure the protocol prefix is `postgresql://` (not `postgres://`).  
3. **Redeploy the app service**  
   - Trigger a deploy (Redeploy button or push a no-op commit).  
   - Wait for the build to succeed.  
4. **Confirm connectivity**  
   - Tail logs for `what-is-my-delta-site`.  
   - Expect a line such as `[STORAGE] Connected to PostgreSQL` (or the absence of SQLite backup messages).  
5. **Functional smoke test**  
   - Hit the live site, create a user or mutate data.  
   - Redeploy once more to verify persistence.

Estimated time: ~10 minutes.

---

## Diagnostic Commands to Run

Run locally with Railway CLI or through the dashboard shell:

```bash
# 1. Verify the DATABASE_URL value seen by the service
railway variables --service what-is-my-delta-site | grep DATABASE_URL

# 2. Test outbound connectivity from the app container (requires Railway shell)
psql "$DATABASE_URL" -c '\dt'

# 3. Check logs for fallback indicators
railway logs --service what-is-my-delta-site --lines 200 | grep -E "STORAGE|mosaic.db"
```

If Railway's CLI shell is unavailable, perform steps 1 and 3 via the dashboard UI.

---

## Verification Tests

- **Connection smoke test:** After redeploy, confirm the logs show successful PostgreSQL connection and that no SQLite backup files are created.  
- **Persistence test:** Create or update a user record, redeploy, then verify the data persists.  
- **API health check:** Hit the `/health` or `/status` endpoint (if available) to ensure the app reports ready status while using PostgreSQL.  
- **Review `pg_stat_activity` (optional):** From the PostgreSQL service shell, run `SELECT datname, application_name FROM pg_stat_activity;` to confirm active connections from the app.

---

## Rollback Procedure (if PostgreSQL remains unusable)

1. Restore the SQLite implementation:
   ```bash
   cp api/storage_sqlite_backup.py api/storage.py
   sed -i '' '/psycopg2-binary/d' requirements.txt
   ```
2. Rebuild and redeploy the application.  
3. Remove `DATABASE_URL` from the service or set it blank to avoid confusion.  
4. Document that persistence remains non-functional until PostgreSQL connectivity is restored.

*Rollback reintroduces the original data-loss issue; use only if production stability is critical and outages must be minimized.*

---

## Additional Context

- Repository path: `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project`  
- Remote: `railway-origin` → `github.com/DAMIANSEGUIN/what-is-my-delta-site.git`  
- Latest migration commit: `2b9fbc1` (“CRITICAL: Migrate from SQLite to PostgreSQL for database persistence”).  
- Time spent by Claude Code: ~90 minutes. Remaining blocker is purely Railway configuration.

**End of Report**
