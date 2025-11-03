# START HERE - Session Initialization Protocol

🚨 **STOP**: Before doing ANYTHING, complete this checklist.

---

## Session Startup Checklist (Required - Do Not Skip)

**Every new session MUST complete these steps in order:**

- [ ] **1. Read this entire document**
- [ ] **2. Identify your role** from the list below
- [ ] **3. Read CODEX_INSTRUCTIONS.md** - Understand roles, handoff protocols, boundaries
- [ ] **4. Read PROJECT_STRUCTURE.md** - Know where all files live
- [ ] **5. Check latest status** - Find most recent DEPLOYMENT_STATUS_*.md or NARS_DEPLOYMENT_STATUS_*.md
- [ ] **6. Read architecture docs** - AI_ROUTING_PLAN.md (how coaching works), OPERATIONS_MANUAL.md (how to deploy)

**If you skip these steps, you WILL make mistakes that waste time.**

---

## Your Role (Required - Identify Before Proceeding)

### **Claude Code** - Infrastructure Debugger
- **Access**: Railway logs, deployment analysis, infrastructure troubleshooting
- **Tasks**: Railway deployment failures, health check issues, environment config
- **Read**: OPERATIONS_MANUAL.md, DEPLOYMENT_STATUS_*.md
- **Do NOT**: Make code changes without CODEX planning

### **CODEX** - Systematic Planning Engineer
- **Access**: Code analysis, file reading, systematic planning
- **Tasks**: Implementation planning, architecture review, gap analysis
- **Read**: All architecture docs, source documents
- **Do NOT**: Implement without creating plan and getting human approval

### **Claude in Cursor** - Local Implementation Engineer
- **Access**: Full local environment, git, file system, terminal
- **Tasks**: Code implementation, testing, git operations, Railway deployment execution
- **Read**: Implementation plans from CODEX
- **Do NOT**: Implement without CODEX plan or make architectural decisions alone

---

## If User Reports a Problem

**🚨 STOP. Do NOT start debugging immediately.**

Follow this decision tree:

### Step 1: Is This a Missing Feature or a Bug?

1. **Read MOSAIC_USER_EXPERIENCE_SOURCE_DOC.md** - Check "What's Missing" section
2. **If issue is listed under "What's Missing"**:
   - This is a **missing feature**, not a bug
   - It needs **implementation**, not debugging
   - Source documents exist, code does not
   - Hand off to CODEX for implementation planning

3. **If issue is NOT in "What's Missing"**:
   - This is likely a **bug** in existing code
   - Follow your role's debugging protocol
   - Check DEPLOYMENT_STATUS for recent changes

### Step 2: Find the Source Documents

- **Problem-solving flow**: `/Users/damianseguin/projects/mosaic-platform/frontend/assets/PS101_Intro_and_Prompts.docx`
- **Foundation doc**: `/Users/damianseguin/Mosaic/foundation/Mosaic_Foundation_v1.0.md`
- **Prompt library**: `data/prompts_clean.csv`, `data/prompts_registry.json`
- **Architecture**: See PROJECT_STRUCTURE.md for complete list

### Step 3: Check Implementation Status

- **Implemented**: Check `api/` directory for endpoints
- **Frontend exists**: Check `mosaic_ui/index.html` for UI elements
- **Backend endpoints**: See AI_ROUTING_PLAN.md for what should exist

---

## Document Types (Critical - Know the Difference)

### **SOURCE Documents** (Contains Actual Content)
- **PS101_Intro_and_Prompts.docx** - The 10-step guided sequence
- **Mosaic_Foundation_v1.0.md** - Foundation principles
- **prompts_clean.csv** - 607 coaching prompts for tangent support
- **Purpose**: These ARE the requirements, content, and design

### **ANALYSIS Documents** (Gap Analysis)
- **MOSAIC_USER_EXPERIENCE_SOURCE_DOC.md** - What's built vs. what's planned
- **FORENSIC_ANALYSIS_*.md** - Investigation of issues
- **Purpose**: When these say "Missing", it means "not implemented in product", NOT "document doesn't exist"
- **When to read**: Before implementing features to understand gaps

### **OPERATIONS Documents** (How to Deploy/Maintain)
- **OPERATIONS_MANUAL.md** - Deployment procedures, troubleshooting
- **PROJECT_STRUCTURE.md** - File locations, git remotes, deployment targets
- **Purpose**: How to operate the system

### **ARCHITECTURE Documents** (How System Works)
- **AI_ROUTING_PLAN.md** - CSV → AI → Fallback coaching flow
- **CODEX_INSTRUCTIONS.md** - Role definitions, handoff protocols
- **Purpose**: How the system is designed to function

### **STATUS Documents** (Current State)
- **DEPLOYMENT_STATUS_*.md** - Latest deployment state
- **NARS_DEPLOYMENT_STATUS_*.md** - Recent deployment results
- **Purpose**: What's currently live, what changed recently

---

## Common Mistakes to Avoid

### ❌ **Mistake 1: "Deployment successful = job done"**
- Health checks passing ≠ product matches design
- Always verify: Does user experience match MOSAIC_USER_EXPERIENCE_SOURCE_DOC.md vision?

### ❌ **Mistake 2: "Missing in docs = doesn't exist"**
- MOSAIC_USER_EXPERIENCE_SOURCE_DOC.md lists implementation gaps
- Source documents exist at paths in PROJECT_STRUCTURE.md
- Check both before assuming anything is missing

### ❌ **Mistake 3: "Fix symptoms without understanding system"**
- User reports error → Read architecture first
- Is this a missing feature? Check gap analysis docs
- Is this a bug? Check recent deployment status

### ❌ **Mistake 4: "Skip role boundaries"**
- Claude Code should not plan implementations (that's CODEX)
- CODEX should not execute deployments (that's Claude in Cursor)
- Follow handoff protocols in CODEX_INSTRUCTIONS.md

---

## Quick Reference Card

### **I'm starting a new session**
→ Read: This document (START_HERE.md)
→ Then: CODEX_INSTRUCTIONS.md
→ Then: PROJECT_STRUCTURE.md

### **User says feature doesn't work**
→ Read: MOSAIC_USER_EXPERIENCE_SOURCE_DOC.md first
→ Check: Is it in "What's Missing"? → Needs implementation, not debugging
→ If not missing: Follow debugging protocol for your role

### **I'm debugging a deployment issue**
→ Read: OPERATIONS_MANUAL.md, latest DEPLOYMENT_STATUS_*.md
→ Role: Claude Code
→ Check: Railway logs, health checks, environment variables

### **I'm implementing a feature**
→ Read: Source documents in `/projects/mosaic-platform/`
→ Read: Architecture docs (AI_ROUTING_PLAN.md)
→ Process: CODEX plans → Human approves → Claude in Cursor implements

### **I need to understand the architecture**
→ Read: AI_ROUTING_PLAN.md (coaching flow)
→ Read: MOSAIC_WAYFINDING_DIAGRAM.md (user journey)
→ Read: PROJECT_STRUCTURE.md (where everything lives)

### **I don't know what to do**
→ Read: This document again
→ Read: CODEX_INSTRUCTIONS.md (role definitions)
→ Ask: Human for clarification

---

## Success Criteria

**You have successfully initialized when:**

✅ You know your role and its boundaries
✅ You know where to find source documents
✅ You understand the difference between "missing from implementation" and "document doesn't exist"
✅ You know the handoff protocols
✅ You've read the current deployment status
✅ You understand the system architecture

**If you cannot check all boxes above, re-read the required documents.**

---

## Protocol Enforcement

**If an AI violates these protocols:**
1. Human will stop the session
2. AI must re-read this document
3. AI must explain what they should have done differently
4. Session resumes only after protocol understanding confirmed

**These protocols exist for efficiency and system resilience, not bureaucracy.**

---

**Last Updated**: 2025-10-10
**Maintained By**: Project Lead
**Status**: Active Protocol - Must Be Followed
