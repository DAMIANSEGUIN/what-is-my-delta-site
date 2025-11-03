# Implementation Team Handoff Document
**Project:** WIMD - What Is My Delta (Mosaic Career Transition Platform)
**Date:** 2025-11-02
**Status:** Production v2.0 - All critical features operational
**System Health:** 🟢 GREEN

---

## Quick Start for New Team Members

### 1. Repository Access
- **GitHub:** github.com/DAMIANSEGUIN/wimd-railway-deploy
- **Production Frontend:** https://whatismydelta.com
- **Backend API:** https://what-is-my-delta-site-production.up.railway.app
- **Health Check:** https://what-is-my-delta-site-production.up.railway.app/health/comprehensive

### 2. Essential Documentation (Read in Order)
1. **`CLAUDE.md`** - Main architecture overview and deployment status
2. **`TROUBLESHOOTING_CHECKLIST.md`** - Error prevention and debugging workflows
3. **`SELF_DIAGNOSTIC_FRAMEWORK.md`** - Architecture-specific error handling
4. **`.ai-agents/SESSION_START_PROTOCOL.md`** - Mandatory first step for all AI agents
5. **`.ai-agents/FINAL_DIAGNOSTIC_20251102.md`** - Current system state (92% complete)
6. **`docs/README.md`** - Deployment procedures and restart protocols

### 3. Development Environment Setup

```bash
# Clone repository
git clone https://github.com/DAMIANSEGUIN/wimd-railway-deploy.git
cd wimd-railway-deploy

# Install Railway CLI (for backend)
npm install -g @railway/cli
railway login

# Install Netlify CLI (for frontend)
npm install -g netlify-cli
netlify login

# Backend local development
cd api
pip install -r requirements.txt
export OPENAI_API_KEY="your_key"
export CLAUDE_API_KEY="your_key"
export DATABASE_URL="postgresql://..."
python -m uvicorn api.index:app --reload

# Frontend local development
cd frontend
# Open index.html in browser (uses live backend proxy)
```

---

## System Architecture Overview

### Stack
- **Frontend:** Vanilla JavaScript (ES6+), deployed on Netlify
- **Backend:** Python FastAPI, deployed on Railway
- **Database:** PostgreSQL (Railway managed)
- **AI Providers:** OpenAI (embeddings, GPT-4), Anthropic (Claude)

### Key Components
1. **Authentication:** Login/register/password reset (5-min trial mode)
2. **PS101 Flow:** 10-step career problem-solving framework with inline forms
3. **Job Search:** 12 free sources (APIs + web scraping)
4. **Resume Optimization:** AI-powered rewriting and customization
5. **OSINT:** Company intelligence gathering
6. **Self-Efficacy Metrics:** Progress tracking and coach escalation
7. **Cost Controls:** Usage limits and emergency stop

---

## Safety Protocols (CRITICAL)

### Before Making ANY Code Changes

**ALWAYS run verification script:**
```bash
./scripts/verify_critical_features.sh
```

**Expected output:**
```
✅ Authentication UI present (16 occurrences)
✅ PS101 flow present (160 references)
✅ API_BASE configuration correct
✅ Production authentication detected
✅ All critical features verified
```

### Pre-commit Hook (Already Installed)
- **Location:** `.git/hooks/pre-commit`
- **Function:** Blocks commits that remove critical features
- **Critical patterns:** Authentication UI, PS101 flow, API_BASE config
- **Bypass:** NOT RECOMMENDED - defeats safety system

### After Making Changes

**MANDATORY steps:**
1. Run verification script (above)
2. Test backend health: `curl https://what-is-my-delta-site-production.up.railway.app/health/comprehensive`
3. For major changes: Run full diagnostic (see `.ai-agents/FINAL_DIAGNOSTIC_20251102.md`)
4. Update `CLAUDE.md` status section
5. Document findings in `.ai-agents/` directory

**Why?** This prevents incidents like the 2025-11-01 auth removal (commit 890d2bc).

---

## Common Tasks

### Deploy Frontend
```bash
cd frontend
netlify deploy --prod --dir=. --site=bb594f69-4d23-4817-b7de-dadb8b4db874
```

### Deploy Backend
```bash
git push railway-origin main
# Railway auto-deploys on push
```

### Check Deployment Status
```bash
# Frontend
netlify status

# Backend
railway status
railway logs
```

### Run Tests
```bash
# Backend golden dataset tests
pytest tests/test_golden_dataset.py -v

# Regression tests
pytest tests/test_prompts.py -v
```

### Access Database
```bash
railway run psql $DATABASE_URL

# List tables
\dt

# Check users
SELECT id, email, created_at FROM users LIMIT 10;
```

---

## Phase Implementation Status

### ✅ Phase 1: Migration Framework
- AI fallback operational
- CSV→AI fallback working
- Feature flags configured
- Prompt system healthy (0% error rate)

### ⚠️ Phase 2: Experiment Engine
- Backend implemented
- Feature flag DISABLED (intentional - gated feature)
- No action required

### ✅ Phase 3: Self-Efficacy Metrics
- Backend operational (requires auth session)
- Frontend code deployed
- Coach escalation working
- Focus Stack present

### ✅ Phase 4: RAG + Job Sources
- Job search operational (12 sources)
- RAG engine working (real OpenAI embeddings)
- OSINT operational
- Cost controls active
- Source analytics working

### ✅ PS101 v2 (Restored 2025-11-02)
- Enhanced inline forms (no browser prompts)
- Experiment components (Steps 6-9)
- Progress dot navigation
- Previous answers review/edit
- Auto-save functionality

---

## Known Issues & Priorities

### Priority 1: Add `/rag/health` Endpoint
- **Status:** Missing (returns 404)
- **Impact:** Low - RAG functionality working
- **Effort:** 15 minutes
- **Implementation:**
```python
# api/rag/router.py
@router.get("/health")
async def rag_health():
    return {"ok": True, "service": "rag", "timestamp": datetime.utcnow().isoformat()}
```

### Priority 2: Verify Database Schema
- **Status:** Not verified (needs Railway credentials)
- **Impact:** Low - system working fine
- **Effort:** 15 minutes
- **Action:**
```bash
railway run psql $DATABASE_URL -c "\dt"
```

### Priority 3: E2E Testing Suite
- **Status:** Not implemented
- **Impact:** High - prevents regressions
- **Effort:** 4-6 hours
- **Tools:** Playwright or Cypress
- **Coverage:**
  - Authentication flows
  - PS101 complete journey
  - Job search
  - Resume optimization
  - File upload

### Priority 4: Email Service Integration
- **Status:** Password reset sends placeholder
- **Impact:** Low - can reset via DB
- **Effort:** 2-3 hours
- **Tools:** SendGrid or AWS SES

---

## AI Agent Protocols

### Session Start (MANDATORY)
**Every AI agent session MUST:**

1. Read `.ai-agents/SESSION_START_PROTOCOL.md`
2. Run `./scripts/verify_critical_features.sh`
3. Declare acknowledgment:
```
✅ Session start verification passed
✅ Critical features confirmed present:
   - Authentication UI: [count] references
   - PS101 v2 flow: [count] references
   - API configuration: [status]

I acknowledge these features MUST BE PRESERVED.
```

### Agent Handoff (When Switching Tools)
**When handing off to another AI agent:**

1. Read `.ai-agents/HANDOFF_PROTOCOL.md`
2. Generate handoff manifest:
```bash
./scripts/create_handoff_manifest.sh > handoff_manifest.json
```
3. Document what was done and what's pending
4. Verify critical features before exiting

### Emergency Rollback
```bash
# If deployment breaks production
git log --oneline -5  # Find last good commit
git revert HEAD
git push railway-origin main --force
```

---

## Feature Flags

**Location:** Railway environment variables

```bash
# Check current flags
railway variables | grep ENABLED

# Expected values
RAG_BASELINE=true
JOB_SOURCES_STUBBED_ENABLED=true
AI_FALLBACK_ENABLED=true
EXPERIMENTS_ENABLED=false  # Intentionally disabled
```

---

## Monitoring & Health

### Backend Health Check
```bash
curl https://what-is-my-delta-site-production.up.railway.app/health/comprehensive | jq
```

**Expected response:**
- `current_test.success: true`
- `prompt_system_health.fallback_enabled: true`
- `recent_failures: 0`
- `failure_rate_percent: 0`

### Railway Auto-Restart
- **Trigger:** `/health` endpoint returns 503
- **Action:** Container automatically restarted
- **Recovery:** Cache clearing + flag reset attempted

### Frontend Verification
```bash
curl -s https://whatismydelta.com | grep -c "authModal"
# Should return: 15+
```

---

## Contact & Escalation

### When to Escalate
- Production down (backend 503, frontend 404)
- Data loss detected (users can't log in)
- Security issue (credentials exposed, API keys leaked)
- Critical feature missing (auth, PS101, job search)

### How to Escalate
1. Check `.ai-agents/` directory for recent diagnostics
2. Run verification script and save output
3. Gather logs: `railway logs > backend_logs.txt`
4. Create detailed GitHub issue with:
   - Error message
   - Steps to reproduce
   - Verification script output
   - Backend logs
   - Recent commits: `git log --oneline -10`

---

## Recent Incident & Recovery (2025-11-02)

### What Happened
- **Incident:** Commit 890d2bc copied `frontend/` → `mosaic_ui/`, overwriting auth system
- **Cause:** AI agent handoff between Claude Code → Codex → Cursor without context preservation
- **Impact:** Login/register UI removed from production

### How We Fixed It
1. Traced git history to find auth (commit 70b8392)
2. Restored auth from backup commit
3. Merged PS101 v2 enhancements with authenticated base
4. Deployed combined version to production
5. Verified all features operational

### What We Built to Prevent Recurrence
1. **Pre-commit hooks** - Block feature removal automatically
2. **Verification scripts** - Automated checks before/after changes
3. **Handoff protocol** - Manifest generation for agent transitions
4. **Session start protocol** - Mandatory verification checklist
5. **Diagnostic framework** - Systematic architecture review process

### Lessons Learned
- Never bypass verification scripts
- Always run diagnostics after major changes
- Document AI agent handoffs explicitly
- Test production immediately after deployment
- Keep backups of all working versions

---

## Quick Reference Commands

```bash
# Backend
railway status                  # Check Railway service status
railway logs                    # View backend logs
railway variables               # List environment variables
railway run psql $DATABASE_URL  # Access database

# Frontend
netlify status                  # Check Netlify deploy status
netlify deploy --prod           # Deploy to production
netlify logs                    # View deployment logs

# Verification
./scripts/verify_critical_features.sh          # Check critical features
./scripts/verify_deploy.sh <api-url>           # Verify deployment
curl <backend-url>/health/comprehensive        # Backend health

# Git
git log --oneline -10           # Recent commits
git show <commit>:path/to/file  # View file at commit
git revert HEAD                 # Undo last commit
git push railway-origin main    # Deploy backend
```

---

## Success Metrics

**System is healthy when:**
- ✅ Verification script passes (all 4 checks)
- ✅ Backend health shows 0% error rate
- ✅ Frontend has 15+ auth references
- ✅ All Phase 1-4 features operational
- ✅ No 404s on documented endpoints (except /rag/health)

**Current Status (2025-11-02):**
- 🟢 92% feature completeness (11/12 features)
- 🟢 100% critical features working
- 🟢 0% backend error rate
- 🟢 All Phase 1-4 deployed

---

## Conclusion

Welcome to the WIMD implementation team! This system is robust, well-documented, and protected by automated safety checks. Follow the protocols, run the verification scripts, and you'll avoid the issues we've already solved.

**Most important takeaway:**
**ALWAYS run `./scripts/verify_critical_features.sh` before and after making changes.**

Questions? Check the diagnostic reports in `.ai-agents/` directory first.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-02
**Next Review:** After E2E tests implemented
**Maintained By:** AI Agent Team + Implementation Team
