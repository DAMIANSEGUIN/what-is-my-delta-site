# 🚦 MOSAIC Project - Quick Start

**One-word trigger for Claude Code:** `Mosaic`

When you say "Mosaic", Claude Code will automatically:
1. Load Foundation canon from `/Users/damianseguin/Mosaic/foundation/Mosaic_Foundation_v1.0.md`
2. Review current project state (CLAUDE_CODE_README.md, CURSOR_CLAUDE_SYNC_README.md)
3. Assume Senior Debugger role with operational rules

---

## Restart Protocol

Run this to begin every session:

```zsh
/Users/damianseguin/restart_wimd.sh
```

The script auto-loads APP_URL from wimd_config.sh (asks once, then saves), runs update_status.sh, logs to DEPLOY_STATUS_NOTE.md, and prints the last 10 lines.

---

## 📊 Latest Diagnostics & Protocols (2025-11-02)

### System Status: 🟢 GREEN
- **Feature Completeness:** 92% (11/12 operational)
- **Backend Error Rate:** 0%
- **Critical Features:** 100% working
- **Latest Diagnostic:** `.ai-agents/FINAL_DIAGNOSTIC_20251102.md`

### Essential Documentation
1. **`CLAUDE.md`** - Main architecture overview and deployment status
2. **`TROUBLESHOOTING_CHECKLIST.md`** - Error prevention workflows
3. **`SELF_DIAGNOSTIC_FRAMEWORK.md`** - Architecture-specific error handling
4. **`.ai-agents/SESSION_START_PROTOCOL.md`** - Mandatory AI agent checklist
5. **`.ai-agents/IMPLEMENTATION_TEAM_HANDOFF.md`** - Team onboarding guide
6. **`.ai-agents/FINAL_DIAGNOSTIC_20251102.md`** - Current system state

### Safety Protocols (MANDATORY)

**Before ANY code changes:**
```bash
./scripts/verify_critical_features.sh
```

**After ANY deployment:**
```bash
# 1. Verify features
./scripts/verify_critical_features.sh

# 2. Check backend health
curl https://what-is-my-delta-site-production.up.railway.app/health/comprehensive

# 3. For major changes: Full diagnostic
# See .ai-agents/FINAL_DIAGNOSTIC_20251102.md for template
```

**Why?** Prevents incidents like 2025-11-01 auth removal (commit 890d2bc).

### Contingency System
- **Pre-commit hooks:** Block feature removal (`.git/hooks/pre-commit`)
- **Verification scripts:** Automated checks (`scripts/verify_critical_features.sh`)
- **Handoff protocol:** Agent transition procedures (`.ai-agents/HANDOFF_PROTOCOL.md`)
- **Session start:** Mandatory verification (`.ai-agents/SESSION_START_PROTOCOL.md`)

---

# 📝 WIMD Railway Deploy – Context Note

> Action on Restart: run ~/restart_wimd.sh (auto-logs status; URL saved in wimd_config.sh)

## Required Env Vars (Railway → Variables)
OPENAI_API_KEY=sk-xxx
CLAUDE_API_KEY=sk-ant-xxx
PUBLIC_SITE_ORIGIN=https://whatismydelta.com
PUBLIC_API_BASE=https://what-is-my-delta-site-production.up.railway.app
DATABASE_URL=
SENTRY_DSN=
APP_SCHEMA_VERSION=v1

## Dependencies (requirements.txt)
- fastapi
- uvicorn
- gunicorn
- httpx
- pydantic
- pydantic-settings
- python-multipart (CRITICAL: Required for file uploads)

## API Endpoints
- `GET /health` — basic health probe
- `GET /config` — returns `{ apiBase, schemaVersion }`
- `GET /prompts/active` — returns `{ active }` (may be null until a CSV is ingested)

## Verify Deploy
```zsh
# Test Railway API directly
curl https://what-is-my-delta-site-production.up.railway.app/health
curl https://what-is-my-delta-site-production.up.railway.app/config

# Run verification scripts
./scripts/predeploy_sanity.sh
./scripts/verify_deploy.sh "$PUBLIC_API_BASE"
```

## Local Development (RECOMMENDED FOR DEBUGGING)
```zsh
# Set environment variables
export OPENAI_API_KEY="your_key_here"
export CLAUDE_API_KEY="your_key_here"
export PUBLIC_SITE_ORIGIN="https://whatismydelta.com"
export APP_SCHEMA_VERSION="v1"

# Install dependencies
pip3 install --user -r requirements.txt

# Start local server
python3 -m uvicorn api.index:app --host 0.0.0.0 --port 8000

# Test locally
curl http://localhost:8000/health
curl http://localhost:8000/config
curl http://localhost:8000/prompts/active
```

## One-Shot Fresh Deploy (New Railway Project)
- Run to create a brand-new Railway project, set variables, and deploy:
  
  ```zsh
  ./scripts/one_shot_new_deploy.sh
  ```

- Notes:
  - It does not delete your existing Railway project; it creates a new one with a timestamped name.
  - You’ll be prompted for variables based on `.env.example`.
  - After deploy, copy the service URL to `PUBLIC_API_BASE` as needed and re-run `./scripts/verify_deploy.sh`.
  - If you want to remove the old service/project, do so from the Railway dashboard to avoid accidental data loss.

## Railway Variables (Build vs Runtime)
- In the Railway service → Variables, ensure each variable is:
  - Scoped to the correct environment (e.g., Production)
  - Marked "Available during deploy" so Nixpacks can access it at build time
- Typical vars: `OPENAI_API_KEY`, `CLAUDE_API_KEY`, `PUBLIC_API_BASE`, `PUBLIC_SITE_ORIGIN`, `APP_SCHEMA_VERSION`

If build fails with "secret NAME: not found":
- The variable likely isn’t marked "Available during deploy" or isn’t defined for this service/environment.
- Toggle it on and redeploy.
# Force rebuild: 1759167655

# PostgreSQL connection test
# PostgreSQL connection retry
