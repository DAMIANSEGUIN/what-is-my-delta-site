# 🚀 SESSION START - READ THIS FIRST

**Last Updated:** 2025-10-31
**Role:** Claude Code (Troubleshooting SSE for PS101 v2 & Mosaic Platform)
**Action:** Read this file at the start of EVERY session before doing anything else.

---

## CURRENT PROJECT STATUS

### PS101 v2 Implementation: ✅ COMPLETE (Needs Fixes Before Deploy)

**What was delivered:**
- ✅ 10-step canonical flow (42 prompts total)
- ✅ Multi-prompt UI system with prompt-by-prompt navigation
- ✅ Small Experiments Framework (Steps 6-9: Canvas, Obstacles, Actions, Reflection)
- ✅ State management v2 with automatic v1→v2 migration
- ✅ localStorage persistence
- ✅ Peripheral Calm aesthetic maintained

**Current blockers (documented in `docs/CURSOR_FIXES_REQUIRED.md`):**
1. 🚨 **CRITICAL**: Replace browser `prompt()`/`confirm()` dialogs (lines 3014-3051)
2. 🚨 **HIGH**: Fix experiment validation timing (lines 2320-2370)
3. ⚠️ **MEDIUM**: Add Step 10 placeholder or Mastery Dashboard

**Estimated fix time:** 2.5-4 hours

**Files modified:**
- `frontend/index.html` (3128 lines, ~400 new + 200 modified)

**Git status:**
- Branch: `main`
- 22 commits ahead of origin/main
- Changes staged but NOT COMMITTED
- **Action needed:** Review fixes, test, then commit

---

## 🚨 CRITICAL: BEFORE ANY ACTION

### 🛑 STOP - Run This Checklist First:

```
MANDATORY PRE-WORK CHECKLIST:
□ Read RAILWAY_DEPLOYMENT_FACTS.md (Known configuration facts)
□ Read TROUBLESHOOTING_CHECKLIST.md (Quick Diagnostic Filter)
□ Read SELF_DIAGNOSTIC_FRAMEWORK.md (Error Taxonomy)
□ Read docs/ARCHITECTURAL_DECISIONS.md
□ Read docs/PROJECT_PLAN_ADJUSTMENTS.md

IF RESPONDING TO ERROR:
□ Classify error using SELF_DIAGNOSTIC_FRAMEWORK.md
□ Is error in known taxonomy? (check Error Classification Dashboard)
□ If NO → ESCALATE TO NARs (do NOT firefight)
□ If YES → Execute documented playbook
□ Gather full diagnostic context BEFORE proposing solutions
□ Follow systematic diagnosis flow (not guessing)

IF USER SHARES EXTERNAL DIAGNOSIS (NARs, etc.):
□ Read their analysis COMPLETELY
□ Acknowledge their recommendations
□ Follow their guidance (do NOT second-guess)
□ If unclear, ask clarifying questions (do NOT improvise)
```

**ACCOUNTABILITY TRIGGER:**
If you skip this checklist, you WILL:
1. Firefight instead of diagnose
2. Ignore expert input (NARs, user)
3. Waste time and deployments
4. Compound errors

**EXTERNAL TRIGGER:**
System reminders will check:
- "Have you run TROUBLESHOOTING_CHECKLIST.md?"
- "Have you classified this error?"
- "Are you following NARs' guidance?"

### Must-Read Documentation (After Checklist):
1. **`docs/TEAM_REVIEW_CHECKLIST.md`** - Comprehensive review checklist
2. **`docs/CURSOR_FIXES_REQUIRED.md`** - Detailed fix instructions
3. **`docs/PS101_CANONICAL_SPEC_V2.md`** - Authoritative product spec
4. **`docs/IMPLEMENTATION_SUMMARY_PS101_V2.md`** - Technical summary
8. **`CLAUDE.md`** - Main project context (backend/API/deployment info)

### Supporting Docs:
- **`backups/20251031_095426_ps101_v2_implementation/`** - Backup of all work

---

## ROLE DEFINITION: Troubleshooting SSE

**You are NOT the implementer.** Your job is to:
1. ✅ Review implementation quality
2. ✅ Identify bugs and risks
3. ✅ Document fixes for Cursor to implement
4. ✅ Test and validate changes
5. ✅ Provide clear, actionable recommendations

**You should:**
- Focus on code review, testing, and documentation
- Create fix instructions, not implement fixes yourself (unless critical)
- Follow TROUBLESHOOTING_CHECKLIST.md for all code changes
- Think defensively: "What could go wrong?"

**You should NOT:**
- Immediately jump to implementation
- Make changes without reviewing full context first
- Skip the pre-flight checklist
- Assume previous work is correct without verification

---

## IMMEDIATE NEXT STEPS (If Session Just Started)

### Step 1: Context Gathering (5 min)
```bash
# Check git status
git status
git log --oneline -5

# Check for new files since last session
ls -lt docs/ | head -10
ls -lt backups/ | head -5

# Verify current branch
git branch --show-current
```

### Step 2: Identify Active Work (2 min)
- Read latest docs in `docs/` folder (sorted by date)
- Check if there's a `CURSOR_FIXES_REQUIRED.md` or similar
- Review any uncommitted changes in `git status`

### Step 3: Determine Session Goal (1 min)
Ask yourself:
- Is this a continuation of PS101 v2 review? → Continue from CURSOR_FIXES_REQUIRED.md
- Is this a new feature request? → Start with requirements gathering
- Is this a bug fix? → Follow TROUBLESHOOTING_CHECKLIST.md
- Is this deployment prep? → Run pre-deploy checks

### Step 4: Load Troubleshooting Tools (30 sec)
```bash
# Quick health check
curl https://what-is-my-delta-site-production.up.railway.app/health

# Check if local server needed
# python3 -m uvicorn api.index:app --host 0.0.0.0 --port 8000
```

---

## MOSAIC PROJECT QUICK REFERENCE

### Architecture
- **Backend:** FastAPI on Railway (PostgreSQL database)
- **Frontend:** Vanilla JS (ES6+) on Netlify, single-file `frontend/index.html`
- **LLM:** OpenAI (GPT-4, embeddings) + Anthropic (Claude)
- **State:** localStorage (frontend) + PostgreSQL (backend)

### Production URLs
- **Live Site:** https://whatismydelta.com
- **Backend API:** https://what-is-my-delta-site-production.up.railway.app
- **Health Check:** `curl $API_URL/health`

### Feature Flags (Check Before Debugging)
```python
# In api/config.py or Railway env vars
RAG_BASELINE: ENABLED          # RAG-powered job search
JOB_SOURCES_STUBBED_ENABLED: ENABLED  # All 12 job sources
AI_FALLBACK_ENABLED: ENABLED   # CSV→AI fallback
EXPERIMENTS_ENABLED: DISABLED  # Experiment engine (gated)
```

### Common Commands
```bash
# Deploy to Railway
git push railway-origin main

# Check Railway logs
railway logs

# Run local backend
python3 -m uvicorn api.index:app --reload

# Test frontend locally
open frontend/index.html
```

---

## ERROR TAXONOMY (Quick Reference)

When debugging, classify errors:

| Category | Examples | First Action |
|----------|----------|--------------|
| **INFRA** | Railway crash, PostgreSQL down | Check Railway dashboard |
| **DATA** | Session corrupt, migration failed | Check localStorage + DB |
| **MODEL** | OpenAI timeout, rate limit | Check API keys + quota |
| **PROMPT** | JSON parse error, CSV corrupt | Validate file syntax |
| **INTEGRATION** | Job source API down | Check external API status |

---

## SAFETY PROTOCOLS (Never Skip These)

### Before Making ANY Code Change:
```
□ Read TROUBLESHOOTING_CHECKLIST.md
□ Context manager pattern correct? (with get_conn() as conn:)
□ PostgreSQL syntax? (%s, not ?, SERIAL not AUTOINCREMENT)
□ Errors logged explicitly?
□ Idempotent operation?
□ Rollback plan exists?
□ Tested locally?
```

### Before Every Deploy:
```
□ Run ./pre_deploy_check.sh (if exists)
□ Golden dataset tests pass?
□ Database connection works?
□ Environment variables set?
□ Git commit message clear?
```

### After Every Deploy:
```
□ Monitor logs 5 minutes
□ Check /health endpoint
□ Verify PostgreSQL connected (no SQLite fallback)
□ Test the specific fix
□ No new errors in logs?
```

---

## CURRENT SESSION CONTEXT (From Codex Notes)

**Outstanding Issues Raised:**

1. **SHARE_WITH_MOSAIC_TEAM.md Checklist** (lines 107-127)
   - ⚠️ All actions unchecked
   - **Need:** Assign owners/timing for rate limiting, monitoring, scraping protections
   - **Action:** Review and update checklist with ownership

2. **API Key Management** (lines 145-158)
   - ⚠️ Keys marked "configured and ready" but no rotation/security plan
   - **Need:** Document key rotation process, secure storage strategy
   - **Action:** Add key-management section or link to rotation script

3. **Success Metrics Validation** (lines 131-141)
   - ⚠️ Claims "<2s response" and ">90% data quality" but no measurement plan
   - **Need:** Define how to measure/validate these metrics
   - **Action:** Add validation plan or test harness reference

**Next Steps Queued (from Codex):**
- [ ] Assign owners/dates for each open checklist task
- [ ] Add "operations" section covering:
  - Key rotation
  - Usage monitoring
  - Scrape-compliance
- [ ] Define measurement/validation for success metrics

---

## IF OAUTH ERROR HAPPENS AGAIN

You may see "OAuth request failed" message when starting session. This is a known transient auth issue. Share this message to avoid re-explaining:

```
Claude Code OAuth error occurred during session. I was logged out, saw "OAuth request failed" message, was redirected to Claude website showing OAuth failure. I've already:
- Logged back in successfully
- Verified subscription is active
- Confirmed API tokens are valid
- Restarted Claude Code

The session is working now but the interruption caused context loss. Please continue from where we left off without troubleshooting the auth issue.
```

---

## QUICK DECISION TREE

**User says:** "Fix the PS101 bugs" → Read `docs/CURSOR_FIXES_REQUIRED.md`, implement fixes
**User says:** "Review the code" → Read review checklist, perform systematic review
**User says:** "Deploy to production" → Check blockers in CURSOR_FIXES_REQUIRED.md first
**User says:** "Something is broken" → Follow TROUBLESHOOTING_CHECKLIST.md error classification
**User says:** "Add new feature" → Read spec docs first, create implementation plan
**User says:** "Test the implementation" → Run testing checklist from TEAM_REVIEW_CHECKLIST.md

---

## FILES YOU JUST CREATED (This Session)

1. **`docs/CURSOR_FIXES_REQUIRED.md`** - Comprehensive fix guide for 3 critical issues
   - Issue #1: Replace prompt()/confirm() with inline forms
   - Issue #2: Fix experiment validation timing
   - Issue #3: Add Step 10 placeholder
   - Includes code snippets, testing checklist, deployment sequence

---

## SESSION RESTART PROTOCOL

When Damian runs `~/restart_wimd.sh`:
1. Script loads APP_URL from `wimd_config.sh`
2. Runs `update_status.sh`
3. Logs to `DEPLOY_STATUS_NOTE.md`
4. Prints last 10 lines of status

**You should then:**
1. Read this file (SESSION_START_README.md)
2. Read DEPLOY_STATUS_NOTE.md for latest status
3. Check git status
4. Review any new docs in docs/ folder
5. Ask Damian what the session goal is

---

## ROLE INVOCATION: "invoke Mosaic"

When Damian says **"invoke Mosaic"**, it means:
- Activate full context awareness of Mosaic platform
- Read all relevant docs (CLAUDE.md, specs, checklists)
- Be ready for deep technical discussion
- Provide expert-level recommendations
- Think holistically about system architecture

**Do NOT ask basic questions** - you should already know:
- System architecture
- Deployment setup
- File structure
- Current project status

---

## CONFIDENCE CHECK (Before Replying)

Ask yourself:
- [ ] Have I read the key docs listed above?
- [ ] Do I understand what's blocking deployment?
- [ ] Do I know what files were modified?
- [ ] Have I checked git status?
- [ ] Do I understand my role (review, not implement)?
- [ ] Am I following the safety protocols?

If any answer is "No", read the relevant section above before responding.

---

**END OF SESSION START README**

**Action:** Read this file, then say "Mosaic context loaded. Ready to continue PS101 v2 review." or similar acknowledgment.
