# MASTER INDEX - SESSION RECOVERY & QUICK START
**Created:** 2025-11-07 17:20 EST
**Purpose:** Single entry point for complete context restoration after crash/new session

---

## 🚀 QUICK START PROMPT (Copy/Paste This)

```
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project

Read this file first:
.ai-agents/MASTER_INDEX_SESSION_RECOVERY.md

This is the master index that will guide you through:
1. Session start protocol (MANDATORY checklist)
2. Current issue diagnosis and fix
3. All project documentation
4. Advanced techniques used in diagnostics

After reading the master index, confirm you understand the current status and what action is needed.
```

---

## 📋 SESSION START SEQUENCE (Follow This Order)

### Step 1: MANDATORY Session Start Protocol
**File:** `.ai-agents/SESSION_START_PROTOCOL.md`
**Action:** Run through entire checklist before doing ANYTHING else

**Quick commands to run:**
```bash
# Verify critical features
./scripts/verify_critical_features.sh

# Check recent commits
git log -5 --oneline

# Check for handoff
ls -1t .ai-agents/handoff_*.json | head -1

# Check for urgent files
ls -1 URGENT_* FOR_*_AGENT*.md 2>/dev/null
```

### Step 2: Read Current Issue Recovery Document
**File:** `.ai-agents/SESSION_RECOVERY_2025-11-07_1712.md`
**Contains:**
- Complete problem description
- Exact fix code to apply
- File and line number
- Deployment checklist
- Verification steps

### Step 3: Understand the Diagnostic Approach Used
**File:** `.ai-agents/DOM_TIMING_PLAYBOOK_PROTOCOL.md`
**Why read this:**
- Explains the DOM timing issue pattern
- Prevention checklist for future
- Reference implementation
- Common mistakes to avoid

**Advanced technique used:**
- Chain-of-Verification prompt (see Advanced Techniques section below)
- This helped identify the root cause vs symptoms

### Step 4: Review Recent Deployment Attempts
**Files (in chronological order):**
1. `.ai-agents/DEPLOYMENT_STATUS_2025-11-07.md` - First deployment result
2. `.ai-agents/DEPLOYMENT_ATTEMPT_2_2025-11-07.md` - Second deployment (config only)

**Key takeaway:** Fix was documented but never actually applied to code

---

## 🎯 CURRENT STATUS SNAPSHOT

**Production:** 🔴 BROKEN - https://whatismydelta.com
**Error:** `initApp is not defined`
**Root Cause:** Missing `document.readyState` check in DOMContentLoaded listener
**Fix Status:** IDENTIFIED, DOCUMENTED, NOT YET APPLIED
**File to Fix:** `mosaic_ui/index.html` line 4018
**Time Estimate:** 12 minutes (apply + deploy + verify)

---

## 📂 COMPLETE DOCUMENTATION MAP

### Tier 1: MANDATORY Reading (Session Start)
1. **SESSION_START_PROTOCOL.md** - Must run before any action
2. **SESSION_RECOVERY_2025-11-07_1712.md** - Current issue & fix
3. **CLAUDE.md** - Project architecture overview

### Tier 2: Current Issue Context
4. **DOM_TIMING_PLAYBOOK_PROTOCOL.md** - Issue diagnosis & prevention
5. **DOM_TIMING_DIAGNOSTIC_2025-11-07.md** - Original diagnostic analysis
6. **DEPLOYMENT_STATUS_2025-11-07.md** - Latest deployment status
7. **DEPLOYMENT_ATTEMPT_2_2025-11-07.md** - What was tried

### Tier 3: General Protocols & Reference
8. **TROUBLESHOOTING_CHECKLIST.md** - Pre-flight checks & debugging workflow
9. **SELF_DIAGNOSTIC_FRAMEWORK.md** - Error taxonomy & automated fixes
10. **docs/README.md** - General project documentation

### Tier 4: Background Context (Read If Needed)
11. **STAGE3_VERIFICATION_2025-11-05.md** - Prior verification attempts
12. **CURSOR_COMPLETION_SUMMARY_2025-11-05.md** - Code consolidation work
13. **FOR_NETLIFY_AGENT_RAILWAY_FIX.md** - Railway deployment issues (older)
14. **URGENT_FOR_NARS_LOGS_NEEDED.md** - PostgreSQL issues (older, resolved)

### Tier 5: Handoffs & Team Communication
15. **handoff_20251103_101528.json** - Latest handoff manifest
16. **HANDOFF_NETLIFY_RUNNER_2025-11-06.md** - Netlify runner handoff
17. **TEAM_NOTE_STAGE3_MANUAL_CHECKS_2025-11-05.md** - Manual verification notes

---

## 🧠 ADVANCED TECHNIQUES REFERENCE

### Chain-of-Verification Prompt (Used in This Session)

**Source:** `/Users/damianseguin/COMPANION GUIDE- PRODUCTION PROMPTS FOR ADVANCED TECHNIQUES.txt`

**Template:**
```
[YOUR ANALYSIS REQUEST]

After providing your initial analysis, complete these verification steps:

1. List three specific ways your analysis could be incomplete, misleading, or incorrect
2. For each potential issue, cite specific evidence from [DOCUMENT/DATA] that either
   confirms or refutes the concern
3. Provide a revised analysis that incorporates verified corrections

Do not skip the verification stage. I need to see your self-critique before the final answer.
```

**When this was used:**
- Diagnosing DOM timing issues (2025-11-07 ~16:12)
- Helped distinguish between deployment issues vs code errors
- Prevented false positive from "config fix" in Attempt #2

**Other techniques in companion guide:**
- Adversarial Stress-Test Template
- Strategic Edge Case Template
- Reverse Prompting Template
- Multi-Persona Debate Template
- Deliberate Over-Instruction Template

**Full guide location:**
`/Users/damianseguin/COMPANION GUIDE- PRODUCTION PROMPTS FOR ADVANCED TECHNIQUES.txt`

---

## 🗂️ PROJECT STRUCTURE REFERENCE

```
/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/
│
├── .ai-agents/              ← START HERE for session recovery
│   ├── MASTER_INDEX_SESSION_RECOVERY.md  ← THIS FILE
│   ├── SESSION_START_PROTOCOL.md         ← MANDATORY checklist
│   ├── SESSION_RECOVERY_2025-11-07_1712.md  ← Current issue fix
│   ├── DOM_TIMING_PLAYBOOK_PROTOCOL.md   ← Prevention protocol
│   ├── DOM_TIMING_DIAGNOSTIC_2025-11-07.md
│   ├── DEPLOYMENT_STATUS_2025-11-07.md
│   ├── DEPLOYMENT_ATTEMPT_2_2025-11-07.md
│   ├── STAGE3_VERIFICATION_2025-11-05.md
│   ├── CURSOR_COMPLETION_SUMMARY_2025-11-05.md
│   ├── handoff_*.json
│   └── [other session notes]
│
├── mosaic_ui/               ← PRODUCTION frontend (Netlify)
│   ├── index.html          ← LINE 4018 NEEDS FIX
│   └── src/
│
├── frontend/                ← Frontend mirror (sync with mosaic_ui)
│   └── index.html          ← Sync after fixing mosaic_ui
│
├── api/                     ← Backend (Railway) - working, no issues
│
├── scripts/                 ← Deployment & verification
│   ├── verify_critical_features.sh  ← Run before deploy
│   ├── deploy.sh                    ← Use this, NOT raw commands
│   └── push.sh                      ← Git push wrapper
│
├── Mosaic/                  ← PS101 Continuity Kit
│   └── PS101_Continuity_Kit/
│
├── docs/                    ← Long-form documentation
│   └── README.md
│
├── CLAUDE.md                ← Project architecture overview
├── TROUBLESHOOTING_CHECKLIST.md
├── SELF_DIAGNOSTIC_FRAMEWORK.md
├── FOR_NETLIFY_AGENT_RAILWAY_FIX.md
└── URGENT_FOR_NARS_LOGS_NEEDED.md
```

---

## 🔑 ESSENTIAL COMMANDS CHEAT SHEET

### Session Start
```bash
# Change to project directory
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project

# Verify critical features
./scripts/verify_critical_features.sh

# Check recent activity
git log -5 --oneline
git status

# Check for handoffs/urgent files
ls -1t .ai-agents/handoff_*.json | head -1
ls -1 URGENT_* FOR_*_AGENT*.md 2>/dev/null
```

### Health Checks
```bash
# Backend health
curl https://what-is-my-delta-site-production.up.railway.app/health

# Production site status
curl -I https://whatismydelta.com

# Check deployed line count (should be ~4023)
curl -s https://whatismydelta.com | wc -l
```

### Deployment (Use Wrappers!)
```bash
# Deploy frontend (CORRECT)
./scripts/deploy.sh netlify

# Deploy backend (CORRECT)
./scripts/deploy.sh railway

# Deploy both (CORRECT)
./scripts/deploy.sh all

# ❌ WRONG - Don't use raw commands
# netlify deploy --prod
# git push railway-origin main
```

### Post-Deploy Verification
```bash
# Wait for CDN propagation
sleep 90

# Run verification script
./scripts/verify_live_deployment.sh

# Check specific feature
curl -s https://whatismydelta.com | grep "Phase 2.5"
```

---

## 🚨 CRITICAL RULES (From Session Start Protocol)

### NEVER Do These Without Wrapper Scripts:
- ❌ `git push railway-origin main`
- ❌ `netlify deploy --prod`
- ❌ Any deployment command directly

### ALWAYS Use Wrapper Scripts:
- ✅ `./scripts/push.sh railway-origin main`
- ✅ `./scripts/deploy.sh netlify`
- ✅ `./scripts/deploy.sh railway`

### Before ANY Code Changes:
1. Run `./scripts/verify_critical_features.sh`
2. Check TROUBLESHOOTING_CHECKLIST.md
3. Never remove auth without approval
4. Never replace files without checking feature loss
5. Follow pre-commit hooks (no --no-verify)

---

## 🎓 CONTEXT RESTORATION WORKFLOW

**If starting completely fresh (no memory of project):**

1. **Read this file** (MASTER_INDEX_SESSION_RECOVERY.md)
   - Gives you complete map of documentation
   - Shows current status
   - Provides quick start commands

2. **Run SESSION_START_PROTOCOL.md checklist**
   - Mandatory before any action
   - Runs verification scripts
   - Checks for handoffs/urgent files

3. **Read SESSION_RECOVERY document**
   - Get exact details of current issue
   - See the exact fix code
   - Understand deployment process

4. **Read DOM_TIMING_PLAYBOOK_PROTOCOL.md**
   - Understand WHY this issue occurred
   - Learn prevention for future
   - See correct patterns

5. **Read CLAUDE.md**
   - Understand project architecture
   - Learn tech stack
   - See deployment infrastructure

6. **Apply the fix** (documented in SESSION_RECOVERY)

7. **Deploy & verify** (checklists in SESSION_RECOVERY)

**Total time:** ~20 minutes to full context + ready to work

---

## 📊 DECISION TREE: What to Read When

```
START
  │
  ├─> First time on project?
  │     ├─> YES: Read Tier 1 (MANDATORY) → Tier 2 (Current Issue) → Tier 3 (Protocols)
  │     └─> NO: Continue
  │
  ├─> Session crashed and need recovery?
  │     ├─> YES: Read SESSION_RECOVERY_2025-11-07_1712.md
  │     └─> NO: Continue
  │
  ├─> New deployment/code change needed?
  │     ├─> YES: Read SESSION_START_PROTOCOL.md → TROUBLESHOOTING_CHECKLIST.md
  │     └─> NO: Continue
  │
  ├─> Debugging an error?
  │     ├─> YES: Read TROUBLESHOOTING_CHECKLIST.md → SELF_DIAGNOSTIC_FRAMEWORK.md
  │     └─> NO: Continue
  │
  ├─> Receiving handoff from another agent?
  │     ├─> YES: Read latest handoff_*.json → SESSION_START_PROTOCOL.md
  │     └─> NO: Continue
  │
  └─> General exploration/learning?
        └─> Read CLAUDE.md → docs/README.md → Browse .ai-agents/
```

---

## 🔄 BACKUP LOCATIONS

**Primary (Local - Project Directory):**
```
/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/
├── MASTER_INDEX_SESSION_RECOVERY.md (THIS FILE)
├── SESSION_RECOVERY_2025-11-07_1712.md
└── [all other session docs]
```

**Secondary (Coachvox Backups):**
```
/Users/damianseguin/coachvox_backups/
└── SESSION_RECOVERY_BACKUP_2025-11-07.md
```

**Tertiary (External Agent Share):**
- Ready to copy/paste to Gemini/ChatGPT
- Complete context in single document
- No dependencies on other files

---

## 🛠️ TOOLING & ADVANCED TECHNIQUES

### Chain-of-Verification (Used in This Session)
**When to use:** Complex diagnostics where symptoms could have multiple causes
**Location:** See "Advanced Techniques Reference" section above
**Example:** Distinguishing deployment issues from code errors

### Other Available Techniques
**File:** `/Users/damianseguin/COMPANION GUIDE- PRODUCTION PROMPTS FOR ADVANCED TECHNIQUES.txt`

**Techniques available:**
- Adversarial Stress-Test (for high-stakes decisions)
- Multi-Persona Debate (for conflicting priorities)
- Reverse Prompting (for unfamiliar domains)
- Deliberate Over-Instruction (for comprehensive analysis)
- Summary-Expand Loop (for context window management)

**When to reference:** Before complex analysis, debugging, or decision-making

---

## 📝 ISSUE TRACKING & STATUS

### Current Issue (2025-11-07)
**Status:** 🔴 ACTIVE - Fix identified but not applied
**Severity:** CRITICAL - Production completely broken
**Impact:** All users cannot use site
**ETA to Fix:** ~12 minutes once started

**Issue Details:**
- Error: `initApp is not defined`
- File: `mosaic_ui/index.html`
- Line: 4018
- Fix: Add `document.readyState` check
- Documented in: SESSION_RECOVERY_2025-11-07_1712.md

### Previous Issues (Resolved)
1. **Railway deployment failures** - Resolved (see FOR_NETLIFY_AGENT_RAILWAY_FIX.md)
2. **PostgreSQL connection issues** - Resolved (see URGENT_FOR_NARS_LOGS_NEEDED.md)
3. **Multiple DOMContentLoaded handlers** - Resolved (see CURSOR_COMPLETION_SUMMARY)

### Known Technical Debt
1. Email service for password reset (placeholder only)
2. No staging environment (direct to production)
3. No automated testing pipeline
4. API keys not rotated regularly

---

## 🧩 INTEGRATION WITH SESSION START PROTOCOL

This master index is **COMPLEMENTARY** to SESSION_START_PROTOCOL.md:

**SESSION_START_PROTOCOL.md:**
- Provides MANDATORY checklist
- Step-by-step verification process
- Operating rules and enforcement

**MASTER_INDEX (this file):**
- Navigation hub to all documentation
- Quick reference for commands
- Status snapshot
- Learning/context restoration guide

**Use together:**
1. SESSION_START_PROTOCOL for every session start (checklist)
2. MASTER_INDEX when you need to find something specific (map)

---

## 💡 TIPS FOR EFFECTIVE USE

### For Claude Code (Primary Agent)
1. Always start with SESSION_START_PROTOCOL.md
2. Use this index to navigate to specific docs as needed
3. Reference Chain-of-Verification for complex diagnostics
4. Update SESSION_RECOVERY when status changes

### For External Agents (Gemini/ChatGPT)
1. Start here (MASTER_INDEX) to get oriented
2. Follow the "First time on project" decision tree
3. Read Tier 1 docs completely before acting
4. Ask for clarification before deploying

### For Human User (Damian)
1. Share this file path to restore agent context quickly
2. Point to specific Tier 2 docs for current issues
3. Use decision tree to guide agents to right documentation
4. Update status section when issues resolve

---

## 🎯 SUCCESS CRITERIA

**You have successfully restored context when you can answer:**

- [ ] What is the production URL? (https://whatismydelta.com)
- [ ] What is currently broken? (initApp not defined)
- [ ] Which file needs fixing? (mosaic_ui/index.html line 4018)
- [ ] What is the exact fix? (Add document.readyState check)
- [ ] Which deployment command to use? (./scripts/deploy.sh netlify)
- [ ] What verification is needed post-deploy? (Browser console check)
- [ ] Where are the session start rules? (SESSION_START_PROTOCOL.md)
- [ ] What technique was used in diagnosis? (Chain-of-Verification)

**If you can't answer all of these, re-read Tier 1 documents.**

---

## 📞 HANDOFF PROTOCOL

**When handing off to another agent:**

1. Update SESSION_RECOVERY document with current status
2. Create handoff manifest: `./scripts/create_handoff_manifest.sh`
3. Point incoming agent to this MASTER_INDEX
4. Specify which Tier 2 docs are relevant to their task

**When receiving handoff:**

1. Read latest handoff_*.json
2. Read this MASTER_INDEX
3. Follow SESSION_START_PROTOCOL.md
4. Read relevant Tier 2 docs for current task

---

## 🔐 SECURITY & SAFETY NOTES

**Files that should NEVER be committed:**
- `.env` files with secrets
- Any file containing API keys
- Database credentials
- Authentication tokens

**Pre-commit hooks will block:**
- Context manager violations
- SQLite syntax in PostgreSQL code
- Silent exception swallowing
- Removing authentication without approval

**If blocked by hook:**
- Review the specific violation
- Fix the code issue
- Do NOT use `--no-verify` without explicit approval

---

## 📅 DOCUMENT MAINTENANCE

**Last Updated:** 2025-11-07 17:20 EST
**Last Updated By:** Claude Code
**Update Frequency:** After each major issue resolution or significant context change

**When to update this index:**
- ✅ New major issue identified
- ✅ Current issue status changes
- ✅ New protocol/playbook created
- ✅ Project structure changes
- ✅ New advanced technique used
- ✅ Deployment process changes

**How to update:**
- Update "Current Status Snapshot" section
- Add new files to "Documentation Map"
- Update "Issue Tracking & Status"
- Increment "Last Updated" timestamp

---

## 🚀 READY TO PROCEED?

**If you just read this document, you should now:**

1. Understand the complete documentation structure
2. Know where to find answers to specific questions
3. Have the commands you need at your fingertips
4. Understand the current issue and fix
5. Be ready to follow SESSION_START_PROTOCOL.md

**Next action:**
```bash
cat .ai-agents/SESSION_START_PROTOCOL.md
```

Then follow the checklist before doing anything else.

---

**END OF MASTER INDEX**
