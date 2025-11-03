# 📚 Documentation Index - START HERE

**Last Updated:** 2025-10-31
**Purpose:** Single source of truth for all project documentation
**For:** Team members who need to know what documents exist and which to read

---

## 🎯 CURRENT STATE (What's Happening Right Now)

**Two separate workstreams in parallel:**

### 1. PS101 v2 → Code exists, has bugs, waiting for fixes
- ✅ **Implemented:** Cursor already coded PS101 v2 (10 steps, 42 prompts, experiments)
- ❌ **Blocked:** 3 bugs prevent deployment (browser prompts, validation, Step 10)
- 📄 **Next:** Cursor will fix bugs using checkpoint system (tomorrow)
- 📍 **Status:** PAUSED until checkpoint system approved

### 2. Checkpoint System → Just created, needs Codex review
- ✅ **Created:** 7 documents defining process for managing agents
- 🔍 **Now:** Codex reviewing system (today)
- 📄 **Next:** Use system to fix PS101 bugs (tomorrow)
- 📍 **Status:** IN REVIEW (blocking PS101 fixes)

**The Plan:**
```
TODAY: Codex reviews checkpoint system → We incorporate feedback
TOMORROW: Cursor fixes PS101 bugs using approved checkpoint system
DAY AFTER: Test & deploy PS101 v2
```

---

## 🚨 CRITICAL: Read This First

**If you're starting a new session or onboarding:**
1. Read this file (you are here)
2. Read the documents marked ⭐ START HERE in your role section below
3. Ignore all other docs unless specifically directed to them

**This index tells you:**
- ✅ What documents exist
- ✅ What each document is for
- ✅ Which are current vs obsolete
- ✅ Reading order for your role

---

## 📂 Document Organization

### By Status

| Status | Meaning | Action |
|--------|---------|--------|
| 🟢 CURRENT | Actively maintained, use this | Read if relevant to your role |
| 🟡 REFERENCE | Historical, don't update | Read only if investigating past decisions |
| 🔴 OBSOLETE | Replaced by newer doc | Ignore (or delete) |
| 🔵 IN REVIEW | Waiting for feedback | Read if you're reviewer |

---

## 👥 By Role

### For Cursor (Implementation Agent)

**⭐ START HERE:**
1. `CURSOR_FIXES_REQUIRED.md` 🟢 - **READ FIRST** - What needs to be fixed
2. `PS101_FIX_PROMPTS_TASK_BRIEF.md` 🔵 - **USE AFTER CODEX REVIEW** - How to fix Issue #1
3. `ARCHITECTURAL_DECISIONS.md` 🟢 - **READ BEFORE ANY CODE CHANGE** - Architecture rules

**Reference (read as needed):**
- `PS101_CANONICAL_SPEC_V2.md` 🟢 - Product spec for PS101 v2
- `IMPLEMENTATION_SUMMARY_PS101_V2.md` 🟢 - What was already implemented
- `AGENT_TASK_TEMPLATE.md` 🟢 - Template for future tasks

**Obsolete (ignore):**
- `CURSOR_AGENT_PROMPT_PS101_V2.md` 🔴 - Old prompt, replaced by CURSOR_FIXES_REQUIRED.md

---

### For Codex (Project Management Agent)

**⭐ START HERE:**
1. `SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md` 🔵 - **YOUR ACTION ITEM** - Review checkpoint system
2. `PROJECT_PLAN_ADJUSTMENTS.md` 🟢 - Overall project plan (you already reviewed/corrected this)

**Review these as part of checkpoint system review:**
- `AGENT_TASK_TEMPLATE.md` 🔵 - Template structure
- `PS101_FIX_PROMPTS_TASK_BRIEF.md` 🔵 - Example usage
- `ARCHITECTURAL_DECISIONS.md` 🔵 - Decision log format
- `CHECKPOINT_PLAN_IMPLEMENTATION_COMPLETE.md` 🔵 - System overview

**Reference (read as needed):**
- `TEAM_REVIEW_CHECKLIST.md` 🟢 - QA checklist for PS101 v2

**Obsolete (ignore):**
- `TEAM_ANNOUNCEMENT_PS101_V2.md` 🔴 - Old announcement, replaced by SHARE_PROJECT_PLAN_ADJUSTMENTS.md
- `TEAM_EMAIL_SHORT.md` 🔴 - Old email, replaced by SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md
- `TEAM_EMAIL_READY_TO_SHARE.md` 🔴 - Old email, replaced by SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md

---

### For Claude Code (Troubleshooting SSE - Me)

**⭐ START HERE (on every new session):**
1. `SESSION_START_README.md` 🟢 - **READ FIRST** - Session startup checklist
2. `ARCHITECTURAL_DECISIONS.md` 🟢 - Current decisions (prevents drift)
3. `PROJECT_PLAN_ADJUSTMENTS.md` 🟢 - Current project status

**Reference (read as needed):**
- `TROUBLESHOOTING_CHECKLIST.md` 🟢 - Error classification and debugging
- `SELF_DIAGNOSTIC_FRAMEWORK.md` 🟢 - Architecture-specific error prevention

---

### For Damian (Project Owner)

**⭐ START HERE:**
1. `PROJECT_PLAN_ADJUSTMENTS.md` 🟢 - **READ FIRST** - Overall status and action items
2. `SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md` 🔵 - **SHARE WITH CODEX** - Checkpoint review request

**When reviewing PS101 v2:**
- `CURSOR_FIXES_REQUIRED.md` 🟢 - What needs fixing (3 issues)
- `TEAM_REVIEW_CHECKLIST.md` 🟢 - How to test after fixes

**When monitoring agent work:**
- `PS101_FIX_PROMPTS_TASK_BRIEF.md` 🔵 - Cursor's current task (after Codex review)
- `ARCHITECTURAL_DECISIONS.md` 🟢 - Rules agents must follow

---

## 📋 All Documents (Alphabetical)

### A

**`AGENT_TASK_TEMPLATE.md`** 🟢
- **Status:** Current
- **Purpose:** Reusable template for all agent tasks
- **Who needs it:** All agents (Cursor/Codex/Claude Code)
- **When to read:** When creating new agent tasks
- **Dependencies:** None

**`ARCHITECTURAL_DECISIONS.md`** 🟢 **[IMPORTANT]**
- **Status:** Current
- **Purpose:** Log of all architectural decisions (prevents agent drift)
- **Who needs it:** All agents (mandatory reading)
- **When to read:** Before any code changes, at start of every session
- **Dependencies:** None

---

### C

**`CHECKPOINT_PLAN_IMPLEMENTATION_COMPLETE.md`** 🟢
- **Status:** Current
- **Purpose:** Overview of checkpoint system for agent task management
- **Who needs it:** Damian (to understand system), Codex (to review)
- **When to read:** To understand how checkpoint system works
- **Dependencies:** References AGENT_TASK_TEMPLATE.md, PS101_FIX_PROMPTS_TASK_BRIEF.md

**`CURSOR_AGENT_PROMPT_PS101_V2.md`** 🔴 **[OBSOLETE]**
- **Status:** Obsolete (replaced)
- **Purpose:** Old instructions for PS101 v2 implementation
- **Who needs it:** No one
- **When to read:** Never (historical reference only)
- **Replaced by:** CURSOR_FIXES_REQUIRED.md

**`CURSOR_FIXES_REQUIRED.md`** 🟢 **[IMPORTANT]**
- **Status:** Current
- **Purpose:** Technical guide for fixing PS101 v2 blocking issues (3 issues documented)
- **Who needs it:** Cursor (to implement fixes), Damian (to review)
- **When to read:** Before starting PS101 v2 fixes
- **Dependencies:** References ARCHITECTURAL_DECISIONS.md

---

### D

**`DEVELOPMENT_PROCESS_REVIEW.md`** 🟡
- **Status:** Reference (historical)
- **Purpose:** Retrospective on PS101 v2 development process
- **Who needs it:** Team reviewing process improvements
- **When to read:** When analyzing what worked/didn't work
- **Dependencies:** None

---

### I

**`IMPLEMENTATION_SUMMARY_PS101_V2.md`** 🟢
- **Status:** Current
- **Purpose:** Technical summary of what was implemented in PS101 v2
- **Who needs it:** Cursor (context), QA (what to test)
- **When to read:** When need to understand what exists
- **Dependencies:** References PS101_CANONICAL_SPEC_V2.md

---

### P

**`PROJECT_PLAN_ADJUSTMENTS.md`** 🟢 **[IMPORTANT]**
- **Status:** Current (with Codex corrections applied)
- **Purpose:** Consolidated action plan integrating review findings and operational gaps
- **Who needs it:** All team members (overall project status)
- **When to read:** To understand current priorities and blockers
- **Dependencies:** References all other docs

**`PS101_CANONICAL_SPEC_V2.md`** 🟢
- **Status:** Current (authoritative spec)
- **Purpose:** Product specification for PS101 v2 (10-step flow, experiments framework)
- **Who needs it:** Cursor (implementation reference), Codex (requirements)
- **When to read:** When clarifying requirements
- **Dependencies:** None (this is source of truth)

**`PS101_FIX_PROMPTS_TASK_BRIEF.md`** 🔵 **[IN REVIEW]**
- **Status:** In review (waiting for Codex feedback on checkpoint system)
- **Purpose:** Specific task brief for Cursor to fix Issue #1 (browser prompts)
- **Who needs it:** Cursor (to execute), Damian (to monitor checkpoints)
- **When to read:** After Codex approves checkpoint system
- **Dependencies:** Requires AGENT_TASK_TEMPLATE.md, ARCHITECTURAL_DECISIONS.md

**`PS101_GAPS_AND_ACTION_PLAN.md`** 🟡
- **Status:** Reference (superseded)
- **Purpose:** Original gap analysis before fixes documented
- **Who needs it:** Historical context only
- **When to read:** If investigating why certain decisions were made
- **Superseded by:** CURSOR_FIXES_REQUIRED.md

---

### S

**`SESSION_START_README.md`** 🟢 **[IMPORTANT for Claude Code]**
- **Status:** Current
- **Purpose:** Startup checklist for Claude Code sessions (prevents context loss)
- **Who needs it:** Claude Code (me)
- **When to read:** At start of EVERY session
- **Dependencies:** References all other docs

**`SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md`** 🔵 **[ACTION REQUIRED]**
- **Status:** In review (waiting for Codex)
- **Purpose:** Request for Codex to review checkpoint system before use
- **Who needs it:** Codex (to review), Damian (to share with Codex)
- **When to read:** NOW - This is current action item
- **Dependencies:** References AGENT_TASK_TEMPLATE.md and 3 other docs

**`SHARE_PROJECT_PLAN_ADJUSTMENTS.md`** 🟢
- **Status:** Current
- **Purpose:** Executive summary of PROJECT_PLAN_ADJUSTMENTS.md for sharing
- **Who needs it:** Team members who need quick overview
- **When to read:** For quick status update
- **Dependencies:** Summarizes PROJECT_PLAN_ADJUSTMENTS.md

---

### T

**`TEAM_ANNOUNCEMENT_PS101_V2.md`** 🔴 **[OBSOLETE]**
- **Status:** Obsolete (replaced)
- **Purpose:** Original team announcement (outdated)
- **Who needs it:** No one
- **Replaced by:** SHARE_PROJECT_PLAN_ADJUSTMENTS.md

**`TEAM_EMAIL_READY_TO_SHARE.md`** 🔴 **[OBSOLETE]**
- **Status:** Obsolete (replaced)
- **Purpose:** Old email draft
- **Who needs it:** No one
- **Replaced by:** SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md

**`TEAM_EMAIL_SHORT.md`** 🔴 **[OBSOLETE]**
- **Status:** Obsolete (replaced)
- **Purpose:** Old email draft
- **Who needs it:** No one
- **Replaced by:** SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md

**`TEAM_REVIEW_CHECKLIST.md`** 🟢
- **Status:** Current
- **Purpose:** Comprehensive QA checklist for PS101 v2 review
- **Who needs it:** QA, Damian (for testing after fixes)
- **When to read:** When testing PS101 v2
- **Dependencies:** References IMPLEMENTATION_SUMMARY_PS101_V2.md

---

## 🗂️ By Topic

### PS101 v2 Implementation
**Current workflow:**
1. `PS101_CANONICAL_SPEC_V2.md` 🟢 - The spec
2. `IMPLEMENTATION_SUMMARY_PS101_V2.md` 🟢 - What was built
3. `CURSOR_FIXES_REQUIRED.md` 🟢 - What needs fixing (3 issues)
4. `PS101_FIX_PROMPTS_TASK_BRIEF.md` 🔵 - How to fix Issue #1 (after Codex review)
5. `TEAM_REVIEW_CHECKLIST.md` 🟢 - How to test

**Status:** Code exists but has 3 bugs. Waiting for checkpoint system review, then Cursor fixes.

### Checkpoint System (Agent Management)
**Current workflow:**
1. `SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md` 🔵 - **START: Codex reviews this**
2. `AGENT_TASK_TEMPLATE.md` 🟢 - Template structure
3. `PS101_FIX_PROMPTS_TASK_BRIEF.md` 🔵 - Example usage
4. `ARCHITECTURAL_DECISIONS.md` 🟢 - Decision log
5. `CHECKPOINT_PLAN_IMPLEMENTATION_COMPLETE.md` 🟢 - System overview

**Status:** Complete and ready for Codex review. Will be used starting tomorrow.

### Project Planning
**Current workflow:**
1. `PROJECT_PLAN_ADJUSTMENTS.md` 🟢 - Master plan (with Codex corrections)
2. `SHARE_PROJECT_PLAN_ADJUSTMENTS.md` 🟢 - Executive summary

**Status:** Current, incorporates all latest findings.

### Operations & Troubleshooting
**Current docs (in root, not docs/):**
- `TROUBLESHOOTING_CHECKLIST.md` 🟢
- `SELF_DIAGNOSTIC_FRAMEWORK.md` 🟢
- `OPERATIONS_MANUAL.md` 🟢
- `SESSION_START_README.md` 🟢

---

## 🧹 Cleanup Recommendations

### Delete These (Obsolete)
```bash
rm docs/CURSOR_AGENT_PROMPT_PS101_V2.md
rm docs/TEAM_ANNOUNCEMENT_PS101_V2.md
rm docs/TEAM_EMAIL_READY_TO_SHARE.md
rm docs/TEAM_EMAIL_SHORT.md
```

### Archive These (Reference)
```bash
mkdir -p docs/archive
mv docs/DEVELOPMENT_PROCESS_REVIEW.md docs/archive/
mv docs/PS101_GAPS_AND_ACTION_PLAN.md docs/archive/
```

---

## 🎯 Current Action Items (What Needs to Happen Now)

### TODAY (2025-10-31)
1. ⏳ **Codex reviews checkpoint system** - `SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md`
2. ⏳ **Incorporate Codex feedback** - Update checkpoint docs if needed

### TOMORROW (2025-11-01)
3. ⏳ **Cursor fixes PS101 Issue #1** - Using `PS101_FIX_PROMPTS_TASK_BRIEF.md`
4. ⏳ **Cursor fixes PS101 Issue #2** - Create new task brief
5. ⏳ **Cursor fixes PS101 Issue #3** - Create new task brief

### AFTER ALL FIXES (2025-11-02)
6. ⏳ **Test PS101 v2** - Using `TEAM_REVIEW_CHECKLIST.md`
7. ⏳ **Deploy PS101 v2** - If all tests pass

---

## 📞 Who to Ask

**Questions about:**
- **PS101 v2 fixes** → Read `CURSOR_FIXES_REQUIRED.md` first, then ask Damian
- **Checkpoint system** → Read `CHECKPOINT_PLAN_IMPLEMENTATION_COMPLETE.md` first, then ask Damian
- **Architecture decisions** → Read `ARCHITECTURAL_DECISIONS.md` (answers likely there)
- **Project status** → Read `PROJECT_PLAN_ADJUSTMENTS.md`
- **Which doc to read** → This file (you're here)

---

## 🔄 Maintenance

**This index should be updated:**
- When new documents created
- When documents become obsolete
- When document status changes (current → reference → obsolete)
- When action items change

**Owner:** Claude Code (me) maintains this during sessions
**Review:** Monthly or when onboarding new agent

---

**Last Updated:** 2025-10-31
**Next Review:** 2025-11-30

**END OF DOCUMENTATION INDEX**
