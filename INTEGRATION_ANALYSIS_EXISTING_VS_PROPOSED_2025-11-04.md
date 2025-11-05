# INTEGRATION ANALYSIS: Proposed Framework vs Existing Systems
**Date:** 2025-11-04  
**Analysis:** Claude Code (SSE)  
**Purpose:** Identify gaps, ambiguities, and integration requirements

---

## EXISTING ENFORCEMENT SYSTEMS

### 1. SESSION_START_PROTOCOL.md
**Current Function:**
- Mandatory checklist run at start of every session
- Verifies PS101 continuity kit alignment
- Checks critical feature presence
- Logs compliance in session_log.txt

**Integration Point with Proposal:**
- Maps to **Stage 1: Define Current State**
- Session Start Protocol = Pre-troubleshooting baseline verification

**Gap Identified:**
❌ Proposal doesn't explicitly call out running SESSION_START_PROTOCOL before Stage 1
❌ No clear rule: "New troubleshooting session = Run SESSION_START_PROTOCOL first"

**Fix Required:**
```markdown
## STAGE 0: SESSION INITIALIZATION (NEW)

Before Stage 1, agent MUST:
1. Execute SESSION_START_PROTOCOL.md in full
2. Log compliance in .ai-agents/session_log.txt
3. Verify all critical features present per protocol
4. If protocol check fails, STOP and fix before troubleshooting

Only proceed to Stage 1 after SESSION_START_PROTOCOL passes.
```

---

### 2. Pre-Push Verification (scripts/pre_push_verification.sh)
**Current Function:**
- Git pre-push hook
- Verifies line count baseline (3875 lines)
- Checks critical features present
- Blocks push if verification fails

**Integration Point with Proposal:**
- Maps to **Stage 5: Implementation Checkpoints**
- Pre-push = Automated checkpoint before git push

**Gap Identified:**
❌ Proposal mentions "checkpoint_validator.sh" but doesn't reference existing pre_push_verification.sh
❌ Risk of duplicate/conflicting validation scripts
❌ Unclear which script runs when

**Fix Required:**
```markdown
## STAGE 5: IMPLEMENTATION WITH CHECKPOINTS (REVISED)

After each code change, run checkpoints IN ORDER:

1. **Local Validation:**
   - `.ai-agents/checkpoint_validator.sh` (new, for immediate feedback)
   - Tests: Syntax, line count, critical features
   - If fails: Automatic rollback via git tag

2. **Pre-Commit Validation:**
   - Existing pre-commit hooks run automatically
   - Tests: Code patterns, dangerous operations

3. **Pre-Push Verification:**
   - `scripts/pre_push_verification.sh` (existing)
   - Tests: Baseline line count, feature presence, git status
   - If fails: Push blocked, fix required

**Integration:** checkpoint_validator.sh is SUBSET of pre_push_verification.sh
- Checkpoint: Fast, runs after each action (10 sec)
- Pre-push: Comprehensive, runs before push (30 sec)
```

---

### 3. verify_critical_features.sh
**Current Function:**
- Comprehensive feature presence check
- Tests: Auth modal, PS101 state, chat, navigation
- Returns pass/fail with detailed output

**Integration Point with Proposal:**
- Maps to **Stage 6: Verification**
- Critical features check = Final acceptance test

**Gap Identified:**
❌ Proposal Stage 6 says "Acceptance criteria met?" but doesn't specify running verify_critical_features.sh
❌ Risk of manual "looks good" instead of automated verification

**Fix Required:**
```markdown
## STAGE 6: VERIFICATION & DOCUMENTATION (REVISED)

**Automated Verification Steps:**

1. **Feature Verification:**
   ```bash
   ./scripts/verify_critical_features.sh
   ```
   Must return exit 0, all features present.

2. **Live Deployment Check:**
   ```bash
   ./scripts/verify_live_deployment.sh https://whatismydelta.com/
   ```
   Must return HTTP 200, BUILD_ID matches commit.

3. **Regression Test Suite:**
   ```bash
   ./scripts/regression_tests.sh
   ```
   All historical tests pass.

**Manual Verification Steps:**
- [ ] User can access site without login wall
- [ ] Chat button opens chat panel
- [ ] Trial mode auto-starts (check console logs)

**Documentation:**
- Update CLAUDE.md status section
- Add entry to .verification_audit.log
- Create retrospective in .ai-agents/retrospectives/

Only mark Stage 6 complete if ALL verifications pass.
```

---

### 4. DEPLOYMENT_CHECKLIST.md
**Current Function:**
- Human-readable checklist for deployments
- Pre-deploy, deploy, post-deploy sections
- Includes PS101 continuity checks

**Integration Point with Proposal:**
- Maps to **Stages 1, 5, 6**
- Deployment checklist = Structured workflow for Stage 5

**Gap Identified:**
❌ Proposal doesn't reference DEPLOYMENT_CHECKLIST.md
❌ Risk: Agent follows Stage 5 but skips checklist items
❌ Ambiguity: Does Stage 5 replace checklist or supplement it?

**Fix Required:**
```markdown
## STAGE 5: IMPLEMENTATION WITH CHECKPOINTS (REVISED)

For deployments specifically, follow this order:

1. **Pre-Deployment:**
   - Execute DEPLOYMENT_CHECKLIST.md "Pre-Deploy" section
   - Run PS101 continuity helper scripts
   - Verify database connection (if backend change)

2. **Implementation Actions:**
   - [Action 1 with checkpoint]
   - [Action 2 with checkpoint]

3. **Deployment:**
   - Execute DEPLOYMENT_CHECKLIST.md "Deploy" section
   - Use wrapper scripts (./scripts/deploy.sh, NOT raw git push)
   - Log deployment to .verification_audit.log

4. **Post-Deployment:**
   - Execute DEPLOYMENT_CHECKLIST.md "Post-Deploy" section
   - Verify live site with scripts/verify_live_deployment.sh

**Rule:** DEPLOYMENT_CHECKLIST.md is mandatory for Stage 5 deployments.
```

---

### 5. Operating Rule #8 (Documentation Discipline)
**Current Function:**
- All docs updated before task completion
- Changes documented in status files
- Audit trail required

**Integration Point with Proposal:**
- Maps to **Stage 6: Verification & Documentation**
- Operating Rule #8 = Enforcement of Stage 6 documentation requirements

**Gap Identified:**
✅ Proposal Stage 6 mentions "Documentation updated?" 
⚠️ But doesn't specify WHICH docs (CLAUDE.md? audit log? session log?)
❌ Risk: Agent marks Stage 6 complete with incomplete docs

**Fix Required:**
```markdown
## STAGE 6: VERIFICATION & DOCUMENTATION (REVISED)

**Documentation Requirements (Operating Rule #8):**

MUST update ALL of the following:
- [ ] `CLAUDE.md` - Update status section with outcome
- [ ] `.verification_audit.log` - Add timestamped entry with commit hash
- [ ] `.ai-agents/session_log.txt` - Log session completion
- [ ] Relevant checklist (DEPLOYMENT_CHECKLIST.md or TROUBLESHOOTING_CHECKLIST.md)
- [ ] Create retrospective: `.ai-agents/retrospectives/YYYY-MM-DD-[issue-name].md`

**Verification:**
```bash
# Script to check documentation completeness
./scripts/verify_documentation_discipline.sh
```

**Rule:** Stage 6 CANNOT be marked complete until all docs updated.
```

---

### 6. PS101 Continuity Kit
**Current Function:**
- BUILD_ID injection (inject_build_id.js)
- Spec hash verification (check_spec_hash.sh)
- Manifest-based versioning
- Prevents version drift

**Integration Point with Proposal:**
- Maps to **Stage 5: Implementation** (for BUILD_ID injection)
- Maps to **Stage 6: Verification** (for spec hash check)

**Gap Identified:**
❌ Proposal doesn't mention PS101 continuity checks
❌ Risk: Deploy without BUILD_ID, break continuity tracking
❌ Ambiguity: When does BUILD_ID get injected in Stage 5?

**Fix Required:**
```markdown
## STAGE 5: IMPLEMENTATION WITH CHECKPOINTS (REVISED)

**PS101 Continuity Integration:**

Before deployment action:
```bash
# Calculate and inject BUILD_ID
export BUILD_ID=$(git rev-parse HEAD)
export SPEC_SHA=$(shasum -a 256 Mosaic/PS101_Continuity_Kit/manifest.can.json | cut -d" " -f1 | cut -c1-8)
node Mosaic/PS101_Continuity_Kit/inject_build_id.js
```

After injection:
```bash
# Verify BUILD_ID present
grep "BUILD_ID:$BUILD_ID" mosaic_ui/index.html || exit 1
```

**Rule:** Every deployment MUST have BUILD_ID injected before push.
```

**Stage 6 addition:**
```bash
# Verify spec hash alignment
./Mosaic/PS101_Continuity_Kit/check_spec_hash.sh
```

---

## AMBIGUITIES & LOGICAL GAPS

### Gap 1: Multiple DOMContentLoaded Listeners
**Issue:** Current codebase has 4 DOMContentLoaded listeners (lines 2021, 2264, 2289, 3515).

**Ambiguity:**
- Which one is the trial mode initialization?
- Do they conflict?
- Should they be consolidated?

**Resolution Required:**
```markdown
## STAGE 3: ZERO-SHOT STRUCTURED ANALYSIS (ENHANCEMENT)

Step 2 - Identify key variables:
  What works: [list]
  What fails: [list]
  What's unknown: [list]
  **NEW:** What's duplicated: [Check for duplicate event listeners]

Add verification step:
```bash
# Find all DOMContentLoaded listeners
grep -n "addEventListener.*DOMContentLoaded" mosaic_ui/index.html

# Verify no conflicts (each listener should handle different logic)
```

**Decision Rule:**
- If multiple listeners found, document purpose of each in Stage 3
- If purpose overlaps, consolidate in Stage 4 solution
```

---

### Gap 2: "Trial Mode Works" vs "Site Works"
**Issue:** User said "trial mode shows console log but site doesn't work"

**Ambiguity:**
- What does "site works" mean specifically?
- Is trial mode part of "site works" or separate?
- How do we test "site works" systematically?

**Resolution Required:**
```markdown
## STAGE 1: DEFINE CURRENT STATE → DESIRED OUTCOME (ENHANCEMENT)

**Desired Outcome MUST be granular, testable user actions:**

BAD (ambiguous):
- "Site works"
- "Trial mode functions"

GOOD (specific, testable):
- User visits https://whatismydelta.com/ without login
- Console shows: "[TRIAL] Initialization complete"
- User clicks "help" button → Chat panel opens
- User clicks "Quick Questions" → PS101 flow displays
- Trial timer starts: localStorage has "delta_trial_start"
- After 5 minutes: Auth modal appears with "trial ended" message

**Format:**
```
DESIRED OUTCOME (User Journey):
1. [Action] → [Expected Result] → [How to Verify]
2. [Action] → [Expected Result] → [How to Verify]
...

Acceptance Criteria:
- [ ] All actions succeed without errors
- [ ] Console shows expected logs
- [ ] LocalStorage contains expected keys
```

**Rule:** Desired Outcome must be decomposable into step-by-step test plan.
```

---

### Gap 3: When to Rollback vs When to Fix Forward
**Issue:** Proposal mentions rollback but unclear when to use it.

**Ambiguity:**
- Rollback to last commit? Last known good? Specific tag?
- If Stage 5 checkpoint fails, rollback or fix forward?
- Who decides rollback vs iterate?

**Resolution Required:**
```markdown
## STAGE 5: IMPLEMENTATION WITH CHECKPOINTS (ENHANCEMENT)

**Decision Tree: Rollback vs Fix Forward**

After checkpoint failure:

```
IF checkpoint fails:
  └─> IF this is first failure:
      └─> Analyze error with Chain-of-Verification
          └─> IF error is simple (typo, syntax):
              └─> Fix forward with immediate re-test
          └─> IF error is complex (logic bug, unexpected behavior):
              └─> Rollback to pre-action snapshot
              └─> Return to Stage 3 for re-analysis
  
  └─> IF this is second consecutive failure on same action:
      └─> MANDATORY rollback to last known good
      └─> Escalate to Codex for Stage 4 re-approval
      
  └─> IF this is third failure (even after rollback):
      └─> STOP troubleshooting
      └─> Document failure in escalation report
      └─> Recommend external review or alternative approach
```

**Rollback Targets:**
- `pre-action-[SNAPSHOT_ID]` tag = Last action (Stage 5)
- `last-known-good` tag = Last Stage 6 verification pass
- Specific commit hash = For major regression
```

---

### Gap 4: Token Budget Enforcement
**Issue:** Proposal sets token budgets but no enforcement mechanism.

**Ambiguity:**
- Who tracks tokens? Agent self-reports?
- What happens if budget exceeded mid-stage?
- Can budget be reallocated between stages?

**Resolution Required:**
```markdown
## TOKEN BUDGET MANAGEMENT (ENFORCEMENT)

**Tracking Mechanism:**

At start of each stage, agent logs:
```
[STAGE X START] Token budget: Y remaining (Z used so far)
```

At end of each stage, agent logs:
```
[STAGE X END] Token usage: A tokens (B% of stage budget)
Total session usage: C tokens (D% of 15k budget)
```

**Enforcement Rules:**

1. **Soft Limit (80% of stage budget):**
   - Agent logs warning
   - Proceeds but compresses remaining communication

2. **Hard Limit (100% of stage budget):**
   - Agent STOPS current stage
   - Executes Summary-Expand Loop (TIER 5)
   - New session with compressed context

3. **Session Limit (15k tokens):**
   - If exceeded, MANDATORY fresh session
   - Previous session summary committed to git
   - Link: "Previous session: commit [HASH]"

**Budget Reallocation:**
- Codex can approve reallocation (e.g., Stage 2 gets +1000, Stage 4 gets -1000)
- Must be documented in session log
- Requires explicit "APPROVED: budget reallocation" message
```

---

### Gap 5: Conflict Between "Batched Approvals" and "Oversight Checkpoints"
**Issue:** RULE 1 says "one permission per session" but framework has checkpoints at Stage 2, 4, 5.

**Ambiguity:**
- Does "one permission" mean batch approval for entire 6-stage plan?
- Or does it mean "no micro-approvals within a stage"?
- Does Codex checkpoint override batched approval?

**Resolution Required:**
```markdown
## BATCHED APPROVALS CLARIFICATION

**Two-Tier Approval System:**

**TIER 1: Session Plan Approval (User)**
- At session start, agent presents 6-stage plan
- User replies "APPROVED" once
- Agent proceeds through all stages with batched decisions

**TIER 2: Oversight Checkpoints (Codex)**
- At Stages 2, 4, 5 checkpoints, agent pauses
- Codex reviews (not user)
- Codex replies "PROCEED" or "REVISE"

**Rule:**
- User gives ONE approval at start
- Codex gives checkpoints (not counted as user approvals)
- Agent doesn't ask user for permission mid-stage UNLESS:
  - Catastrophic risk detected
  - User feedback contradicts hypothesis
  - Stage plan becomes invalid

**Example Flow:**
```
Session Start:
  Agent: "SESSION PLAN: [6 stages]. APPROVED?"
  User: "APPROVED"

Stage 2:
  Agent: [Diagnosis complete]
  Codex: "PROCEED"
  [NO user prompt]

Stage 4:
  Agent: [Solution synthesis]
  Codex: "REVISE - consider risk X"
  Agent: [Revised synthesis]
  Codex: "PROCEED"
  [NO user prompt]

Stage 5 - Checkpoint 1:
  Agent: [Action 1 complete, checkpoint pass]
  [NO Codex prompt, automated validation]

Stage 5 - Checkpoint 2:
  Agent: [Action 2 FAILED checkpoint]
  Agent: [Auto-rollback to pre-action snapshot]
  Codex: "APPROVED to retry with fix forward"
  [NO user prompt]

Stage 6:
  Agent: [All verification passed]
  [Session complete, NO final approval needed]
```

**Token Savings:**
- User approvals: 1 per session (~100 tokens)
- Codex checkpoints: 2-3 per session (~200 tokens)
- Total overhead: ~300 tokens (vs 1500+ in current ad-hoc)
```

---

## INTEGRATION CHECKLIST

To align proposed framework with existing systems:

**Immediate Changes to Proposal:**
- [ ] Add Stage 0: SESSION_START_PROTOCOL execution
- [ ] Stage 5: Reference existing pre_push_verification.sh
- [ ] Stage 5: Add PS101 BUILD_ID injection step
- [ ] Stage 6: Mandate verify_critical_features.sh
- [ ] Stage 6: Specify all docs per Operating Rule #8
- [ ] Clarify rollback decision tree in Stage 5
- [ ] Add token tracking mechanism with logging
- [ ] Resolve batched approval vs oversight checkpoint ambiguity

**New Scripts to Create:**
- [ ] `.ai-agents/checkpoint_validator.sh` (subset of pre_push_verification.sh)
- [ ] `scripts/verify_documentation_discipline.sh` (checks Operating Rule #8)
- [ ] `scripts/regression_tests.sh` (evolutionary test suite)
- [ ] `.ai-agents/templates/STAGE_1_TEMPLATE.md` (Current State → Desired Outcome)

**Existing Scripts to Update:**
- [ ] `scripts/pre_push_verification.sh` - Add reference to checkpoint_validator.sh
- [ ] `scripts/deploy.sh` - Ensure PS101 BUILD_ID injection included

**Documentation to Create:**
- [ ] `.ai-agents/config.json` - Framework mode flag (strict/standard/fast)
- [ ] `.ai-agents/known_issues.json` - Current issue patterns
- [ ] `.ai-agents/templates/RETROSPECTIVE_TEMPLATE.md`

---

## LOGICAL GAPS SUMMARY

**Critical Gaps (MUST fix before adoption):**
1. ❌ No Stage 0 for SESSION_START_PROTOCOL
2. ❌ Duplicate validation scripts (checkpoint vs pre_push)
3. ❌ Missing PS101 continuity in Stage 5
4. ❌ Ambiguous "site works" acceptance criteria
5. ❌ Conflict: batched approvals vs oversight checkpoints

**Medium Gaps (Should fix soon):**
6. ⚠️ No token tracking enforcement
7. ⚠️ Unclear rollback decision criteria
8. ⚠️ Multiple DOMContentLoaded listeners not addressed

**Minor Gaps (Can defer):**
9. ℹ️ Budget reallocation procedure undefined
10. ℹ️ Retrospective review cadence not integrated with existing sessions

---

## REVISED RECOMMENDATION

**Do NOT adopt proposal as-is.**

**Instead:**
1. Create REVISED_PROPOSAL.md addressing critical gaps 1-5
2. Get Codex approval on revised version
3. Implement integration checklist items
4. THEN adopt for current production issue

**Alternative (Fast Track):**
- Adopt "FAST" mode for current issue (skip full 6-stage process)
- Use existing TROUBLESHOOTING_CHECKLIST.md instead
- Fix the JavaScript execution issue using current tools
- Adopt full framework for NEXT production issue (after integration complete)

---

**ANALYSIS COMPLETE**

**Next Action:** 
- Share this analysis with Codex
- Codex decides: Revise proposal first OR use existing tools for current issue
- User confirms approach before proceeding

