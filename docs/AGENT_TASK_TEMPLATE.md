# Agent Task Template

**Purpose:** Structure for assigning tasks to agents (Cursor, Codex, Claude Code)
**Usage:** Fill this out BEFORE assigning any agent task
**Version:** 1.0
**Date:** 2025-10-31

---

## Task Brief

**Task ID:** [Unique identifier, e.g., PS101-FIX-001]
**Task Title:** [One sentence description]
**Agent:** [Cursor / Codex / Claude Code]
**Risk Tier:** [1=Low (autonomous) / 2=Medium (supervised) / 3=High (human-only)]
**Checkpoint Mode:** [Full (5 checkpoints) / Lite (3 checkpoints) - See guidance below]
**Estimated Effort:** [Hours]
**Deadline:** [YYYY-MM-DD]

---

## Risk Tier & Checkpoint Mode Guidance

### Tier 1 (Low Risk) - Autonomous Tasks
**Examples:** Documentation updates, spell-check, comment additions, read-only analysis
**Checkpoint Mode:** **Lite** (3 checkpoints recommended)
- Checkpoint 1: Understanding
- Checkpoint 2: Implementation + Testing (bundled)
- Checkpoint 3: Final Approval

**Validation Substitutes:**
- No lint required (substitute: peer review or spell-check)
- No automated tests (substitute: manual review or link check)
- Allow console.log in documentation examples

### Tier 2 (Medium Risk) - Supervised Tasks
**Examples:** Code changes, API modifications, feature additions, bug fixes
**Checkpoint Mode:** **Full** (5 checkpoints required)
- All checkpoints as documented below
- Lint/test/validation required per Quality Requirements

### Tier 3 (High Risk) - Human-Only Tasks
**Examples:** Database migrations, auth changes, payment processing, security fixes
**Checkpoint Mode:** **Full** with additional manual verification
- Human must perform the work (agent assists only)
- All checkpoints require explicit sign-off

---

## Context

### What Problem Are We Solving?
[Describe the problem or requirement in 2-3 sentences]

### Why Is This Important?
[Business value, user impact, or technical debt]

### Current State
[What exists now? What's broken or missing?]

### Desired End State
[What should exist after this task is complete?]

---

## Inputs

### Required Reading (Agent MUST read these before starting)
- [ ] `docs/[DOCUMENT_1].md`
- [ ] `docs/[DOCUMENT_2].md`
- [ ] `docs/ARCHITECTURAL_DECISIONS.md` (always)

### Context Files (For reference if needed)
- `[FILE_PATH_1]` - [Why relevant]
- `[FILE_PATH_2]` - [Why relevant]

### Code Files to Modify
- `[FILE_PATH]` lines [START]-[END] - [What to change]

---

## Constraints

### Do NOT (Hard constraints)
- [ ] Do NOT [Specific action to avoid]
- [ ] Do NOT [Another constraint]
- [ ] Do NOT skip [Required step]

### MUST Follow (Required patterns/standards)
- [ ] MUST [Specific requirement]
- [ ] MUST [Another requirement]
- [ ] MUST test [How to verify]

### Architecture Decisions to Honor
- Decision #[XXX]: [Title from ARCHITECTURAL_DECISIONS.md]
- Decision #[YYY]: [Title from ARCHITECTURAL_DECISIONS.md]

---

## Success Criteria

### Functional Requirements
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

### Quality Requirements (Tier 2+ Only)
- [ ] Code passes linter (no errors)
- [ ] Tests pass (specify which tests)
- [ ] No console errors in browser
- [ ] Accessibility: [Specific requirement]
- [ ] Performance: [Specific requirement]

**For Tier 1 tasks, substitute:**
- [ ] Spell-check passes (documentation)
- [ ] Links valid (documentation)
- [ ] Peer review complete (if applicable)
- [ ] Formatting consistent with existing docs

### Documentation Requirements
- [ ] Update [DOCUMENT] with [What]
- [ ] Add comments to [Complex code sections]
- [ ] Document any new decisions in ARCHITECTURAL_DECISIONS.md

---

## Checkpoints

### Checkpoint 1: Understanding Verification
**When:** After reading inputs, before planning
**Agent must:**
- [ ] Summarize the problem in own words
- [ ] List the files to be modified
- [ ] Identify any unclear requirements

**You (Human) will:**
- [ ] Verify agent understands correctly
- [ ] Clarify any misunderstandings
- [ ] Approve to proceed to planning

**If agent misunderstood:** Stop, clarify, restart from this checkpoint

---

### Checkpoint 2: Approach Approval
**When:** After planning, before implementation
**Agent must:**
- [ ] Propose implementation approach (1-3 paragraphs)
- [ ] List files/functions to modify
- [ ] Identify any risks or unknowns
- [ ] Estimate time to implement

**You (Human) will:**
- [ ] Review proposed approach
- [ ] Check approach follows architectural decisions
- [ ] Verify no alternative approach is better
- [ ] Approve to proceed to implementation

**If approach needs revision:** Provide feedback, agent revises, re-checkpoint

---

### Checkpoint 3: Implementation Review
**When:** After implementing, before testing
**Agent must:**
- [ ] Show all code changes (diff or full sections)
- [ ] Explain what each change does
- [ ] Highlight any deviations from plan
- [ ] Note any issues encountered

**You (Human) will:**
- [ ] Review code for correctness
- [ ] Check code follows conventions
- [ ] Verify no unintended side effects
- [ ] Approve to proceed to testing

**If code needs revision:** Provide specific feedback, agent revises, re-checkpoint

---

### Checkpoint 4: Testing Verification
**When:** After testing, before commit
**Agent must:**
- [ ] Run all specified tests
- [ ] Report test results (pass/fail counts)
- [ ] Document any failing tests
- [ ] Show manual testing results (if applicable)

**You (Human) will:**
- [ ] Verify all tests passed
- [ ] Run manual tests yourself (if needed)
- [ ] Check for any regressions
- [ ] Approve for commit

**If tests fail:** Agent fixes issues, re-run tests, re-checkpoint

---

### Checkpoint 5: Final Approval
**When:** Before commit/deploy
**Agent must:**
- [ ] Confirm all checkpoints passed
- [ ] Confirm all success criteria met
- [ ] Provide suggested commit message
- [ ] Note any follow-up tasks needed

**You (Human) will:**
- [ ] Final review of entire change
- [ ] Verify backup exists (if Tier 2/3)
- [ ] Approve commit message
- [ ] Execute commit (or delegate to agent if Tier 1)

**After commit:**
- [ ] Monitor for 5-10 minutes
- [ ] Verify no errors in logs/console
- [ ] Mark task as complete

---

## Testing Plan

### Automated Tests to Run
```bash
# List exact commands
pytest tests/[TEST_FILE].py -v
# OR
npm test
```

### Manual Testing Steps
1. [Step 1 - What to do and what to verify]
2. [Step 2 - What to do and what to verify]
3. [Step 3 - What to do and what to verify]

### Regression Testing
- [ ] Test [Feature 1] still works
- [ ] Test [Feature 2] still works
- [ ] Test [Integration point] still works

### Edge Cases to Test
- [ ] [Edge case 1 - e.g., empty input]
- [ ] [Edge case 2 - e.g., very long input]
- [ ] [Edge case 3 - e.g., special characters]

---

## Rollback Plan

### If Implementation Fails
1. [Step to undo changes]
2. [How to restore previous state]
3. [Who to notify]

### Backup Location
- **Git commit before changes:** [COMMIT_HASH]
- **Backup files:** `[PATH_TO_BACKUP]`
- **Database backup:** [If applicable]

### Recovery Time Estimate
- **Time to rollback:** [X minutes]
- **Time to diagnose issue:** [Y minutes]
- **Time to fix and retry:** [Z hours]

---

## Context Refresh Protocol

**Trigger Conditions (Agent must pause when ANY of these occur):**
- After completing a checkpoint, OR
- After 45 minutes of heads-down work without checkpoint, OR
- Before starting next major implementation phase

**Agent must pause and re-read:**
1. `docs/ARCHITECTURAL_DECISIONS.md`
2. This task brief
3. Original success criteria

**Agent outputs:**
> Context refresh complete.
> Current task: [Brief description]
> Current progress: [What's done]
> Next action: [What's next]
> Time elapsed: [X minutes]

**You verify agent is still on track before allowing continuation.**

### Per-Agent Update Intervals (Prevents Simultaneous Updates)

**When multiple agents running in parallel:**
- **Cursor:** Update every 20 minutes (at :00, :20, :40)
- **Codex:** Update every 20 minutes (at :10, :30, :50)
- **Claude Code:** Update on-demand or after checkpoint completion

This staggers status updates to avoid notification spam.

---

## Communication Protocol

### Status Updates
Agent provides update every [15/30/60] minutes:
- What was completed
- What's in progress
- Any blockers or questions
- Estimated time remaining

### When to Ask for Help
Agent should stop and ask if:
- Uncertain about approach
- Encountering unexpected errors
- Taking longer than estimated
- Need to deviate from plan
- Found issue in requirements

### When to Escalate
Stop immediately and escalate if:
- Security concern discovered
- Data loss risk identified
- Breaking change unavoidable
- Deadline at risk

---

## Post-Task Documentation

### Agent Completes
- [ ] Update `docs/ARCHITECTURAL_DECISIONS.md` if new decision made
- [ ] Update relevant documentation
- [ ] Note any technical debt created
- [ ] List any follow-up tasks

### You (Human) Complete
- [ ] Review agent's documentation
- [ ] Add task to "Completed Tasks" log
- [ ] Note lessons learned (if applicable)
- [ ] Update this template if needed

---

## Example: Filled Template

See `docs/PS101_FIX_PROMPTS_TASK_BRIEF.md` for a complete example of this template filled out for the PS101 v2 fixes.

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-31 | Initial template | Claude Code |
| 1.1 | 2025-10-31 | Applied Codex feedback: Tier 1 lite mode, 45-min refresh, per-agent intervals | Claude Code |

---

**END OF AGENT TASK TEMPLATE**

**Usage Note:** Copy this template to a new file named `[TASK_ID]_TASK_BRIEF.md` and fill in all sections before assigning to agent.
