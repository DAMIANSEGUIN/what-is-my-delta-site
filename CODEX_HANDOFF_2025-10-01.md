# CODEX HANDOFF - 2025-10-01

**From**: Claude Code (Infrastructure Debugger)
**To**: CODEX (Systematic Planning Engineer)
**Priority**: CRITICAL - Project chaos, repeated protocol failures
**Handoff Reason**: Systematic analysis required + drift from established organization

---

## CRITICAL ISSUE: PROTOCOL BREAKDOWN

### What Went Wrong This Session
1. **Claude Code failed to follow CODEX_INSTRUCTIONS**
2. **Worked in wrong directories** (mosaic_ui/ instead of root)
3. **Pushed to wrong repositories** (wimd-railway-deploy instead of what-is-my-delta-site)
4. **Made changes without systematic analysis**
5. **Did not hand off to CODEX when required**
6. **Ignored established file organization from weeks-ago resource audit**

### User Concern
> "this approach seems like complete chaos. we either return to the way we planned to work or i move the project to Netlify agent runners for oversight"

> "i organized a proper resources audit weeks ago so this is not ok"

**Result**: User considering moving entire project to Netlify Agent Runners due to repeated AI failures.

---

## IMMEDIATE TECHNICAL ISSUE

### Problem: Prompts CSV Returns Null
**Symptom**:
- `/prompts/active` endpoint returns `{"active": null}`
- Chat works but uses placeholder responses instead of actual prompts

**Evidence**:
- ✅ CSV files exist locally: `data/prompts_clean.csv` (138KB, 600+ prompts)
- ✅ CSV files in git: Verified with `git ls-files data/`
- ✅ CSV files in Railway repo: Verified with `git ls-tree railway-origin/main:data/`
- ✅ Local registry exists: `data/prompts_registry.json` shows `{"active": "f19c806ca62c..."}`
- ❌ Railway API returns null

**Files Verified Present**:
```bash
# Local
data/prompts.csv
data/prompts_clean.csv
data/prompts_fixed.csv
data/prompts_registry.json
data/prompts_6e488b26db77.json
data/prompts_f19c806ca62c.json

# Railway Repository
data/prompts.csv ✅
data/prompts_clean.csv ✅
data/prompts_fixed.csv ✅
data/prompts_6e488b26db77.json ✅
data/prompts_f19c806ca62c.json ✅
data/prompts_registry.json ❓ (not verified)
```

---

## PROJECT DIRECTORY STRUCTURE ISSUE

### Source of Truth Confusion
**Two locations exist**:
1. `/Users/damianseguin/projects/mosaic-platform/`
   - Created 2025-09-29 as consolidation
   - ⚠️ CODEX cannot access due to sandbox limitations
   - Status: NOT deployed

2. `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/`
   - Current LIVE deployment source
   - ✅ All AIs can access
   - ✅ CODEX ruled this is source of truth (see CODEX_HANDOVER_README.md lines 35-46)

### Resource Audit Drift
**User states**: Proper resource audit completed weeks ago
**Current state**: File organization has drifted from that audit
**Impact**: Files "keep getting lost", repeated mistakes, AI confusion

---

## SYSTEMATIC ANALYSIS REQUIRED

### Task 1: Prompts Loading Analysis
**CODEX to investigate**:
1. Why does Railway return `null` when local registry shows active SHA?
2. Is `prompts_registry.json` in Railway repository?
3. Is prompts_loader.py reading from correct location?
4. Are there Railway-specific file access issues?
5. Does Railway deployment need restart/rebuild?

**Files to Review**:
- `api/prompts_loader.py` - CSV loading logic
- `api/index.py` lines 280-285 - `/prompts/active` endpoint
- `data/prompts_registry.json` - Local registry state
- Railway deployment logs (if accessible)

**Expected Output**: Step-by-step fix plan with specific commands

---

### Task 2: File Organization Audit
**CODEX to document**:
1. Review original resource audit from weeks ago (locate documentation)
2. Document current actual file structure
3. Identify drift from original organization
4. Create PROJECT_STRUCTURE.md with:
   - Canonical directory structure
   - File locations (absolute paths)
   - Git repository mappings
   - Deployment target configurations
   - AI access constraints

**Critical Requirements**:
- Must work for ALL AIs (Claude Code, CODEX, Cursor)
- Must prevent files from "getting lost"
- Must prevent wrong directory/repo mistakes
- Must be checkable at session start

---

### Task 3: Protocol Enforcement Plan
**CODEX to specify**:
1. Session start checklist (what to read, where to cd)
2. When to hand off between AIs (exact triggers)
3. Gate system (when to STOP and await approval)
4. How to verify correct location before any action
5. Escalation criteria (when to call user)

**Goal**: Prevent chaos, ensure "project stays on rails"

---

## DEPLOYMENT CONFIGURATION

### Railway Backend
- **URL**: https://what-is-my-delta-site-production.up.railway.app
- **Repository**: https://github.com/DAMIANSEGUIN/what-is-my-delta-site
- **Remote**: `railway-origin`
- **Branch**: `main`
- **Status**: ✅ Healthy, CORS fixed, chat working

### Netlify Frontend
- **URL**: https://whatismydelta.com
- **Site**: resonant-crostata-90b706
- **Status**: ✅ Proxy working via Agent Runner deployment

### Current Working State
- ✅ Chat functional
- ✅ CORS resolved (apex and www domains)
- ✅ Netlify proxy routing to Railway
- ❌ Prompts CSV not loading
- ❌ File organization drifted

---

## REFERENCE DOCUMENTATION

**Must Read**:
- `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/CODEX_INSTRUCTIONS.md`
- `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/ROLLING_CHECKLIST.md`
- `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/CODEX_HANDOVER_README.md`
- Original resource audit documentation (location TBD - CODEX to find)

**Recent Session Failures**:
- `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/SESSION_TROUBLESHOOTING_LOG.md`

---

## SUCCESS CRITERIA

### Immediate (This Handoff)
1. ✅ Prompts CSV loading and returning correct data
2. ✅ PROJECT_STRUCTURE.md created and accurate
3. ✅ Protocol enforcement plan documented
4. ✅ No more "files getting lost"
5. ✅ Clear session start procedure

### Long-term (Project Health)
1. Project "stays on rails" - no more chaos
2. AI collaboration follows protocols
3. User confident in system
4. Alternative to Netlify Agent Runner takeover

---

## HANDOFF INSTRUCTIONS FOR CODEX

**Step 1**: Read all documentation in `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/`

**Step 2**: Systematically analyze prompts loading issue
- Review prompts_loader.py logic
- Check Railway repository for registry.json
- Determine root cause
- Provide fix plan with exact commands

**Step 3**: Create PROJECT_STRUCTURE.md
- Locate original resource audit
- Document current structure
- Identify drift
- Specify canonical organization

**Step 4**: Define protocol enforcement
- Session start checklist
- Handoff triggers
- Gate system
- Verification procedures

**Step 5**: Present to user for approval before any implementation

---

## CURRENT SESSION CONTEXT

**Working Directory**: `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/`

**Git Remotes**:
```
origin         https://github.com/DAMIANSEGUIN/wimd-railway-deploy.git
railway-origin https://github.com/DAMIANSEGUIN/what-is-my-delta-site.git
```

**Recent Commits**:
```
65420b1 Fix: Add exact /wimd redirect for OPTIONS requests
7f4d681 Fix: Simplify CORS origins to explicit list
e65e2d2 Add CORS debug endpoint
c8a956f Fix: Add explicit OPTIONS handlers
```

**Railway Deployment**: Most recent should be 65420b1 (CORS fix)

---

## DECISION POINT

User must decide:
- **Option A**: CODEX provides systematic fix, project continues with strict protocols
- **Option B**: Move to Netlify Agent Runners for oversight

**Recommendation**: Give CODEX one chance to fix chaos with systematic approach. If this fails, Netlify Agent Runners may be better suited.

---

**Handoff Complete**: Awaiting CODEX systematic analysis and action plan.

**Do NOT implement anything until user approves CODEX's plan.**
