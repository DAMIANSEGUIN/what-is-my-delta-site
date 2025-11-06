# Codex Reset Protocol

**Date:** 2025-11-05  
**Status:** Active

---

## Purpose

Invoke "Codex Reset Protocol" whenever an agent drifts or loses context. Both agents (Terminal Codex + Codex Agent) will reset and re-align.

---

## Process

When "Codex Reset Protocol" is invoked:

1. **Both agents re-run session start protocol:**
   - Execute `.ai-agents/SESSION_START_PROTOCOL.md` Steps 1–5
   - Step 1: Identify yourself
   - Step 2: Run critical feature verification
   - Step 2b: Confirm PS101 continuity kit alignment
   - Step 3: Check for handoff
   - Step 4: Review recent activity
   - Step 5: Declare readiness

2. **Restate Present State → Desired Outcome:**
   - Terminal Codex: Restate current repo state and what needs to be achieved
   - Codex Agent: Restate current production state and what evidence needs to be captured

3. **Re-log the session:**
   - Write new entry to `.ai-agents/session_log.txt`
   - Include timestamp, agent name, and reset reason

4. **Resume work with fresh context:**
   - Both agents proceed with aligned understanding
   - Reference staging notes (source of truth) for current state

---

## When to Invoke

**Invoke Codex Reset Protocol when:**
- Agent drifts from assigned task
- Context confusion or conflicting instructions
- Agent makes changes that don't align with staging notes
- Agent loses track of Present State → Desired Outcome
- Multiple agents working on same issue without coordination

**Invocation:** Simply say "Codex Reset Protocol" and both agents will reset

---

## Agent-Specific Actions

### Terminal Codex

**On Reset:**
1. Re-run session start protocol (Steps 1–5)
2. Read current staging notes:
   - `.ai-agents/STAGE1_CURRENT_STATE_YYYY-MM-DD.md`
   - `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md`
   - `.ai-agents/STAGE3_VERIFICATION_YYYY-MM-DD.md`
3. Restate: "Present State: [repo state] → Desired Outcome: [goal]"
4. Log reset in `.ai-agents/session_log.txt`
5. Resume work based on staging notes

### Codex Agent (Browser)

**On Reset:**
1. Re-run session start protocol (Steps 1–5)
2. Read current staging notes:
   - `.ai-agents/STAGE1_CURRENT_STATE_YYYY-MM-DD.md`
   - `.ai-agents/STAGE2_ACTION_PLAN_YYYY-MM-DD.md`
   - `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md`
3. Restate: "Present State: [production state] → Desired Outcome: [evidence to capture]"
4. Log reset in `.ai-agents/session_log.txt`
5. Resume evidence capture based on staging notes

---

## Staging Notes as Source of Truth

**Critical:** After reset, both agents must reference staging notes for current state:
- `.ai-agents/STAGE1_CURRENT_STATE_YYYY-MM-DD.md` – Problem statement
- `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md` – Evidence and diagnosis
- `.ai-agents/STAGE3_VERIFICATION_YYYY-MM-DD.md` – Verification results
- `.ai-agents/TEAM_NOTE_*.md` – Team communication

**No side channels** – All instructions, outstanding tasks, and handoffs live in staging notes.

---

## Example Reset Log Entry

```
[2025-11-05T18:50:00Z] Codex Reset Protocol invoked
[2025-11-05T18:50:01Z] Terminal Codex: Reset - Agent drifted from auth button fix task
[2025-11-05T18:50:01Z] Terminal Codex: Present State → Repo has auth button fix committed, ready to deploy
[2025-11-05T18:50:01Z] Terminal Codex: Desired Outcome → Deploy fix and verify with Codex Agent
[2025-11-05T18:50:02Z] Codex Agent: Reset - Re-aligning with Terminal Codex
[2025-11-05T18:50:02Z] Codex Agent: Present State → Production missing auth button
[2025-11-05T18:50:02Z] Codex Agent: Desired Outcome → Capture evidence after Terminal Codex deploys fix
[2025-11-05T18:50:03Z] Both agents aligned, resuming work
```

---

**Status:** Active  
**Last Updated:** 2025-11-05

