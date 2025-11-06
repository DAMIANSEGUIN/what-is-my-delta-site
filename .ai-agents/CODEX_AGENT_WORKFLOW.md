# Codex Agent Workflow – Two-Agent Tandem Model

**Date:** 2025-11-05  
**Status:** Active  
**Model:** Terminal Codex + Codex Agent (Browser-Based)

---

## Overview

We run **two Codex agents in tandem**:

1. **Terminal Codex** – Handles repo work (coding, scripts, docs)
2. **Codex Agent** – Browser-based, traces real user flows in production

**Purpose:**
- Eliminate manual browser checks
- Provide hard data for Terminal Codex to act on
- Reduce context regressions between sessions
- Enable faster diagnoses with captured artifacts
- Tighten guardrails and keep team aligned without manual mediation

---

## Workflow Integration

### Deployment Rhythm

1. **Stage 1 Summary** → Initial problem statement
2. **Stage 2 Evidence via Codex Agent** → Browser probes capture evidence (BEFORE code edits)
   - Codex Agent opens WhatIsMyDelta in fresh session
   - Runs DevTools checklist (initializer, auth modal, chat network, API base)
   - Logs console/network output into `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md`
3. **Terminal Codex Implements Fixes** → Reads Stage 2 evidence, implements fixes, runs verify scripts, updates Stage 3
   - **No waiting on human relays** – Terminal Codex acts directly on Codex Agent evidence
4. **Stage 3 Verification** → Local checks + Codex Agent confirmation

### Stage 2: Evidence Capture

**Trigger:** After deployment or when production issue detected

**Codex Agent Actions:**
1. Opens WhatIsMyDelta in isolated browser session
2. Runs DevTools probes:
   - `typeof window.initApp` check
   - Auth modal state (`document.getElementById('authModal')?.style.display`)
   - Chat network calls (Network tab for `/wimd` requests)
   - `__API_BASE` configuration check
   - Console error capture
   - Network request/response logging
3. Captures evidence into `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`

**Output:**
- Hard data (console logs, network requests, element states)
- No manual interpretation needed
- Terminal Codex can act immediately on evidence

### Stage 3: Verification

**Local Verification:**
- `./scripts/verify_live_deployment.sh`
- `./scripts/verify_critical_features.sh`

**Codex Agent Confirmation:**
- Re-run probes on live site
- Confirm fixes are working
- Update diagnosis doc with verification results

---

## Benefits

1. **Faster Diagnoses**
   - Hard data instead of manual checks
   - No context loss between sessions
   - Evidence captured automatically

2. **Fewer Context Regressions**
   - Each session inherits captured artifacts
   - No need to re-run manual browser checks
   - Evidence persists in diagnosis docs

3. **Cleaner Handoffs**
   - Next session has complete evidence
   - Terminal Codex stays focused on repo changes
   - Cursor acts on hard data, not assumptions

4. **Role Separation**
   - **Codex Agent:** Browser-based evidence capture
   - **Terminal Codex:** Repo changes, scripts, logs
   - **Cursor:** Acts on Codex Agent data

---

## Usage

### Triggering Codex Agent

**After Deployment:**
```bash
# 1. Deploy
./scripts/deploy.sh netlify

# 2. Wait for deploy (~3 min)

# 3. Trigger Codex Agent for Stage 2 evidence capture
#    (Codex Agent will probe live site and update diagnosis doc)
```

**For Stage 2 Diagnosis:**
- Codex Agent runs automatically when Stage 2 is triggered
- Captures evidence into `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md`
- **Terminal Codex reads evidence from Stage docs and implements fixes immediately**
- No human relay needed – Terminal Codex acts on hard data

**For Stage 3 Verification:**
- Codex Agent confirms fixes are working
- Updates diagnosis doc with verification results
- Provides final confirmation before closing incident

---

## Evidence Captured

**DevTools Probes:**
- `typeof window.initApp` → Function existence check
- `document.getElementById('authModal')?.style.display` → Modal visibility
- Network tab → `/wimd` request status (200/202/error)
- `window.__API_BASE` → API configuration
- Console errors → JavaScript runtime issues
- Network requests/responses → API integration status

**Output Format:**
- Structured evidence in diagnosis doc
- Console logs with timestamps
- Network request details (URL, method, status, response)
- Element state snapshots

---

## Integration Points

**Diagnosis Documents:**
- `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md` → Evidence section auto-populated
- `.ai-agents/STAGE3_VERIFICATION_2025-11-05.md` → Codex Agent confirmation results

**Handoff Documents:**
- `.ai-agents/SESSION_RESTART_HANDOFF_2025-11-05.md` → References Codex Agent workflow
- `.ai-agents/NEXT_SESSION_START_HERE.md` → Quick reference for Codex Agent usage

---

## Codex Reset Protocol

**When to invoke:** Whenever an agent drifts or loses context

**Process:**
1. Both agents (Terminal Codex + Codex Agent) re-run `.ai-agents/SESSION_START_PROTOCOL.md` Steps 1–5
2. Restate **Present State → Desired Outcome**
3. Re-log the session in `.ai-agents/session_log.txt`
4. Resume work with fresh context

**Invocation:** Simply say "Codex Reset Protocol" and both agents will reset

---

## Staging Notes as Source of Truth

**Critical:** Keep staging notes current – they are the shared source of truth

**Files to maintain:**
- `.ai-agents/STAGE1_CURRENT_STATE_YYYY-MM-DD.md` – Problem statement
- `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md` – Evidence and diagnosis
- `.ai-agents/STAGE3_VERIFICATION_YYYY-MM-DD.md` – Verification results
- `.ai-agents/TEAM_NOTE_*.md` – Team communication

**No side channels needed** – All instructions, outstanding tasks, and handoffs live in staging notes

---

## Team Roles

**Codex Agent (Browser-Based):**
- Runs Mosaic through real user flows in isolated session
- Captures DevTools evidence (initializer, auth modal, chat network, API base)
- Updates `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md` with evidence
- Provides hard data for Terminal Codex to act on

**Terminal Codex:**
- Reads Codex Agent evidence from Stage 2 diagnosis docs
- Implements fixes/tests based on hard data
- Runs verify scripts
- Updates Stage 3 verification docs
- Focuses on repo changes, scripts, logs
- **No waiting on human relays** – acts directly on Codex Agent evidence

**Cursor:**
- Triggers Codex Agent when needed
- Reviews Codex Agent evidence before proceeding
- Coordinates between Terminal Codex and Codex Agent

**CIT:**
- Reviews Codex Agent evidence for accuracy
- Validates diagnosis based on captured data

**Codex (Review):**
- Reviews Stage 2 diagnosis with Codex Agent evidence
- Approves fixes based on hard data
- Signs off on incident closure

---

**Status:** Active  
**Last Updated:** 2025-11-05

