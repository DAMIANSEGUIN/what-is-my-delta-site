# PROPOSAL: Structured Troubleshooting Framework with Team Oversight
> **Status Note (2025-11-05):** Superseded by `REVISED_TROUBLESHOOTING_FRAMEWORK_2025-11-05.md`, which integrates this proposal with existing enforcement protocols. Retain this file for historical reference only.
**Date:** 2025-11-04  
**Proposed by:** Claude Code (SSE)  
**For Review:** Codex (Oversight)  
**Context:** Multiple production issues, firefighting without structure

---

## PROBLEM STATEMENT

**Current State:**
- Production site (https://whatismydelta.com/) has multiple non-functional elements
- JavaScript executes partially (first console.log works, rest fails silently)
- Login modal exists but hidden, unclear if functional
- Chat button non-responsive
- Trial mode initialization incomplete
- **Root cause unknown** - no systematic diagnosis performed
- Team has spent hours firefighting without reaching Desired Outcome

**Why This Keeps Failing:**
1. No clear "Current State → Desired Outcome" definition
2. Agents firefighting symptoms instead of diagnosing architecture
3. No oversight/verification between steps
4. No shared framework for troubleshooting

---

## PROPOSED SOLUTION

### Framework Selection (from Nate's Production Prompts)

I recommend **3 techniques** from the companion guide:

#### 1. **Chain-of-Verification Template** (TIER 1)
**Why:** Forces explicit enumeration of what could be wrong before proceeding
**Application:** Before any code change, agent must:
- List 3 ways the diagnosis could be incomplete/wrong
- Cite specific evidence confirming or refuting each concern
- Provide revised diagnosis incorporating verified corrections

**Example for current issue:**
```
Initial diagnosis: "JavaScript execution stops at localStorage call"

Verification:
1. Could be wrong because: No browser debugger confirmation
   Evidence: Only have console.log output, not execution state
   Revised: Need to test with try-catch boundary to capture actual error

2. Could be wrong because: Multiple DOMContentLoaded listeners may conflict
   Evidence: Found 4 DOMContentLoaded listeners in code (grep shows lines 2021, 2264, 2289, 3515)
   Revised: Test if other listeners are blocking trial init

3. Could be wrong because: Chat button may be unrelated to JavaScript execution
   Evidence: No test of actual button event handlers performed
   Revised: Separate "trial init" from "chat functionality" diagnosis
```

#### 2. **Zero-Shot Chain-of-Thought Structure** (TIER 3)
**Why:** Forces sequential reasoning instead of jumping to solutions
**Application:** Every troubleshooting task follows this structure:

```
Step 1 - Define the scope:
  Current State: [Specific, testable]
  Desired Outcome: [Specific, measurable]
  
Step 2 - Identify key variables:
  What works? What doesn't? What's unknown?
  
Step 3 - Analyze relationships:
  How do working/broken components interact?
  
Step 4 - Consider edge cases:
  What browsers? What localStorage states? What network conditions?
  
Step 5 - Synthesize diagnosis:
  Root cause hypothesis with evidence
  
Verification check: What would prove this diagnosis wrong?

Action Plan: [Specific, testable steps]
```

#### 3. **Multi-Persona Debate** (TIER 4)
**Why:** Surface conflicting technical priorities before committing to solution
**Application:** For any proposed fix, simulate debate between:

**Persona 1: Deployment Engineer (Claude Code)**
- Priority: Ship working code to production quickly
- Argues for: Minimal changes, fail-open design, deploy now

**Persona 2: Quality Assurance (Codex Oversight)**
- Priority: Root cause understanding, prevent regression
- Argues for: Full architecture audit, test coverage, systematic diagnosis

**Persona 3: End User Advocate (Cursor/NARs)**
- Priority: Actual user experience, functional completeness
- Argues for: All buttons work, trial mode functions, no login wall

**Output:** Synthesis that addresses all three perspectives with explicit tradeoffs

---

## REVISED PROPOSITION

**Your original:**
> "we need a self-correction prompt... create a meta prompt... choose a claude skill(s)... framework has to define Current State and Desired Outcome... clear goal to achieve now"

**My revision:**

### Meta-Prompt for Structured Troubleshooting (All Team Members)

```markdown
# TROUBLESHOOTING SESSION: [ISSUE NAME]

## STAGE 1: DEFINE CURRENT STATE → DESIRED OUTCOME

**Current State** (measurable):
- What is broken? (specific URLs, features, error messages)
- What evidence? (logs, screenshots, test results)
- What is unknown? (gaps in diagnosis)

**Desired Outcome** (testable):
- What should work? (specific user actions succeeding)
- How to verify? (acceptance criteria)
- Timeline: When must this be resolved?

**Alignment Check:** All team members acknowledge above before proceeding.

---

## STAGE 2: CHAIN-OF-VERIFICATION DIAGNOSIS

**Initial Hypothesis:** [Your diagnosis]

**Verification Checks:**
1. Three ways this could be wrong:
   - [Potential error 1 + evidence]
   - [Potential error 2 + evidence]
   - [Potential error 3 + evidence]

2. Revised diagnosis incorporating verification:
   [Updated hypothesis]

**Oversight Review:** Codex confirms diagnosis before proceeding to Stage 3.

---

## STAGE 3: ZERO-SHOT STRUCTURED ANALYSIS

Step 1 - Define scope: [Architecture layer: UI/API/DB/Integration]
Step 2 - Identify variables: [What works / What fails / What's unknown]
Step 3 - Analyze relationships: [Component interactions]
Step 4 - Consider edge cases: [Browser/network/state variations]
Step 5 - Synthesize root cause: [Evidence-based conclusion]

Verification: What would prove this wrong? [Falsifiability test]

**Oversight Review:** Codex validates reasoning chain.

---

## STAGE 4: MULTI-PERSONA SOLUTION DEBATE

**Deployment Engineer (Fast Fix):**
[Argues for quick ship with minimal risk]

**Quality Engineer (Thorough Fix):**
[Argues for complete diagnosis and testing]

**User Advocate (Complete Fix):**
[Argues for full functionality, no compromises]

**Synthesis:**
[Solution addressing all concerns with explicit tradeoffs]

**Oversight Review:** Codex approves synthesis or requests iteration.

---

## STAGE 5: IMPLEMENTATION WITH CHECKPOINTS

Action 1: [Specific, testable step]
  → Test: [How to verify this worked]
  → Rollback: [If test fails, revert how?]

Action 2: [Next step, dependent on Action 1 success]
  → Test: [Verification]
  → Rollback: [Revert procedure]

**Oversight Review:** Codex confirms each checkpoint before next action.

---

## STAGE 6: VERIFICATION & DOCUMENTATION

Outcome achieved? [Yes/No with evidence]
Acceptance criteria met? [Checklist from Stage 1]
Regression risk? [What could break? How monitored?]
Documentation updated? [What files changed, why?]

**Final Review:** All team members confirm resolution.
```

---

## IMPLEMENTATION PLAN

### Roles & Responsibilities

**Claude Code (SSE - Systems & Software Engineering):**
- Execute troubleshooting using above framework
- Cannot proceed past Stage 2 without Codex approval
- Documents all verification checks and evidence
- Proposes solutions in Multi-Persona debate format

**Codex (Oversight & Architecture):**
- Reviews Stage 2 diagnosis before proceeding
- Validates Stage 3 reasoning chain
- Approves or iterates Stage 4 synthesis
- Confirms each Stage 5 checkpoint
- Final sign-off on Stage 6 verification

**Cursor (Code Review & Implementation):**
- Reviews actual code changes proposed in Stage 4
- Validates implementation quality in Stage 5
- Tests acceptance criteria in Stage 6

**NARs (User Experience & Validation):**
- Confirms Desired Outcome in Stage 1 matches user needs
- Represents User Advocate persona in Stage 4
- Performs final UAT in Stage 6

### For Current Issue

**Immediate Next Step:**
1. I (Claude Code) will create STAGE 1 document defining Current State → Desired Outcome
2. Post to repository for team review
3. No further code changes until Codex approves Stage 1
4. Proceed through framework with checkpoints

---

## ASSESSMENT OF THIS SOLUTION

**Strengths:**
- Forces explicit alignment on goals before action
- Prevents firefighting by requiring verification
- Built-in oversight prevents runaway diagnosis
- Uses proven production-grade prompting techniques
- Creates audit trail for future troubleshooting

**Weaknesses:**
- Slower than current ad-hoc approach (by design)
- Requires all team members to adopt framework
- Adds coordination overhead
- May be over-engineering for simple issues

**When to Use:**
- ✅ Production issues with unknown root cause (like current)
- ✅ Multiple failed fix attempts
- ✅ High-stakes changes with regression risk
- ❌ Simple, well-understood bugs with clear fixes

**Risk Mitigation:**
- If framework takes >2 hours without resolution, escalate to external review
- Emergency bypass: any team member can call "rollback to last known good" and restart

---

## RECOMMENDATION

**Adopt this framework immediately for the current production issue.**

Timeline:
- Next 15 min: Claude Code creates Stage 1 document
- Codex reviews and approves/revises Stage 1
- Next 30 min: Execute Stages 2-3 with verification
- Codex checkpoint before Stage 4
- Next 45 min: Stages 4-6 with oversight

**Total time budget: 90 minutes** to resolution or escalation decision.

If framework proves effective, adopt as standard operating procedure for all production troubleshooting.

---

**END PROPOSAL**

**Next Action:** Await Codex review and approval to proceed with Stage 1.

---

## ADDENDUM: TOKEN EFFICIENCY & COMMUNICATION PROTOCOL

### Hard-Coded Communication Rules

**RULE 1: Batched Decision Points (One Permission Per Session)**

Default mode: **Batch all decisions into a single permission request per session.**

**Implementation:**
```
At session start, agent presents:

**SESSION PLAN**
I will execute the following without further approval:
1. [Action 1 with expected outcome]
2. [Action 2 with expected outcome]  
3. [Action 3 with expected outcome]

**CHECKPOINT REQUIRED** if:
- Any action fails verification test
- Evidence contradicts initial hypothesis
- User feedback indicates wrong direction

Do you approve this plan? Reply "APPROVED" or specify revisions.
```

**Exceptions requiring immediate stop:**
- ⚠️ **CATASTROPHIC RISK**: Potential data loss without retrievable backup
  - Examples: Dropping database tables, deleting git history, overwriting files without .bak
  - Action: STOP, get explicit approval, verify backup exists
  
- ⚠️ **BREAKING CHANGE**: Modification that could break production
  - Examples: Changing API contracts, altering database schema, modifying authentication flow
  - Action: STOP, present multi-persona risk assessment, get approval

**Token Savings:** Reduces back-and-forth from ~500 tokens per approval to ~100 tokens for batch plan.

---

**RULE 2: Compressed Status Updates**

Use structured status format instead of conversational explanations:

**Verbose (wasteful):**
```
I've completed the first step of adding the try-catch block to the initialization 
code. This should help us catch any errors that might be occurring. Now I'm going 
to move on to the next step which is testing whether this works...
```
**Tokens:** ~45

**Compressed (efficient):**
```
✅ Step 1 complete: try-catch added
→ Next: Test initialization
```
**Tokens:** ~12

**Implementation:**
All status updates use this format:
```
✅ [completed action]: [outcome]
⚠️ [warning/issue]: [impact]  
→ Next: [upcoming action]
🔴 BLOCKED: [blocker description]
```

**Token Savings:** 70% reduction in status update overhead.

---

**RULE 3: Evidence-First Communication**

Replace explanations with evidence, then synthesize.

**Verbose:**
```
I think the problem might be related to the way we're handling localStorage 
because I noticed in the code that we're trying to access it in a certain way 
that could potentially cause issues...
```
**Tokens:** ~38

**Evidence-First:**
```
Evidence:
- localStorage.getItem() at line 2023
- Execution stops after line 2022
- No error in catch block

Hypothesis: Silent exception in localStorage access
Test: Add logging before/after getItem call
```
**Tokens:** ~28

**Implementation:**
Structure all technical communication as:
```
Evidence: [Observable facts]
Hypothesis: [Theory explaining evidence]
Test: [How to verify/refute]
```

**Token Savings:** 25-40% reduction per technical discussion.

---

**RULE 4: Reusable Verification Templates**

Pre-define verification checks as templates to avoid regenerating.

**Standard Deployment Verification Template:**
```
DEPLOY_CHECK:
1. Syntax: node --check [file] → [✅/❌]
2. Build: [command] → [exit code]
3. Live: curl [endpoint] → [status]
4. Feature: [user action] → [expected result]
```

**Agent simply fills in results:**
```
DEPLOY_CHECK (commit abc1234):
1. Syntax: node --check mosaic_ui/index.html → ✅
2. Build: npm run build → exit 0
3. Live: curl https://whatismydelta.com/ → 200
4. Feature: Click chat button → [PENDING USER TEST]
```

**Token Savings:** 60% reduction for repetitive verification tasks.

**Repository Location:** Store templates in `.ai-agents/templates/` for reference.

---

**RULE 5: Differential Communication (Changes Only)**

When providing updates, report only deltas from previous state.

**Verbose:**
```
The site has these features working: login modal, registration form, trial mode, 
and the three main sections. However, the chat button is still not working, and 
we're still investigating the JavaScript execution issue...
```
**Tokens:** ~35

**Differential:**
```
DELTA since last update:
+ Added: try-catch logging
- Still broken: chat button
○ Unchanged: trial mode logic
```
**Tokens:** ~15

**Token Savings:** 55% reduction in progress reports.

---

### Token Budget Management

**Per-Session Allocation:**
- **Stage 1 (Planning):** 2,000 tokens max
  - Includes: Current State definition, Desired Outcome, approval request
  
- **Stage 2-3 (Diagnosis):** 5,000 tokens max
  - Includes: Chain-of-Verification, Zero-Shot analysis, evidence gathering
  
- **Stage 4 (Solution):** 3,000 tokens max  
  - Includes: Multi-Persona debate, synthesis, approval request
  
- **Stage 5 (Implementation):** 4,000 tokens max
  - Includes: Code changes, deployment, checkpoint confirmations
  
- **Stage 6 (Verification):** 1,000 tokens max
  - Includes: Test results, final documentation

**Total Session Budget:** 15,000 tokens (well under 200k limit)

**If Budget Exceeded:**
1. Use Summary-Expand Loop (TIER 5 from companion guide)
2. Start fresh session with compressed context
3. Link sessions via git commit hashes for continuity

---

### Self-Correction & Evolution Protocols

**PROTOCOL 1: Retrospective After Each Issue Resolution**

After Stage 6 completion, agent generates:

```
## RETROSPECTIVE: [Issue Name]

What worked:
- [Technique/approach that was effective]

What failed:
- [Approach that wasted time/tokens]

Lessons for next time:
- [Specific improvement to framework]
- [New template to add to .ai-agents/templates/]

Framework evolution proposal:
- [Modification to 6-stage process]
- [New rule to add to communication protocol]
```

**Storage:** `.ai-agents/retrospectives/YYYY-MM-DD-[issue-name].md`

**Review cadence:** Codex reviews monthly, incorporates improvements into framework

---

**PROTOCOL 2: Feature Flag for Framework Strictness**

Allow graduated enforcement based on issue severity:

```javascript
// .ai-agents/config.json
{
  "frameworkMode": "strict",  // Options: "strict" | "standard" | "fast"
  "tokenBudgetEnforced": true,
  "checkpointsRequired": ["stage2", "stage4"],  // Which stages need approval
  "autoRollbackEnabled": true
}
```

**Modes:**
- **strict:** All 6 stages, all checkpoints (current proposal)
- **standard:** Stages 1,2,4,6 with checkpoints only at 2 and 4
- **fast:** Stages 1,5,6 only (for trivial bugs with clear fixes)

**Decision criteria:**
```
Use STRICT if:
- Unknown root cause
- Multiple failed fix attempts  
- Production user impact

Use STANDARD if:
- Clear diagnosis
- Low regression risk
- Isolated component

Use FAST if:  
- Obvious typo/syntax error
- No user impact
- Fully reversible change
```

---

**PROTOCOL 3: Automated Checkpoint Validation**

Instead of manual "does this look good?" checkpoints, use automated tests:

```bash
# .ai-agents/checkpoint_validator.sh

#!/bin/zsh
# Runs after each Stage 5 action

echo "=== Checkpoint Validation ==="

# 1. Syntax check
if ! node --check mosaic_ui/index.html 2>/dev/null; then
  echo "❌ CHECKPOINT FAILED: Syntax error"
  exit 1
fi

# 2. Lint check (if applicable)
# eslint mosaic_ui/index.html --quiet || exit 1

# 3. Line count sanity check (prevent accidental deletion)
CURRENT_LINES=$(wc -l < mosaic_ui/index.html)
EXPECTED_MIN=3000
if [ $CURRENT_LINES -lt $EXPECTED_MIN ]; then
  echo "❌ CHECKPOINT FAILED: File too short ($CURRENT_LINES < $EXPECTED_MIN)"
  exit 1
fi

# 4. Critical feature presence check
if ! grep -q "id=\"authModal\"" mosaic_ui/index.html; then
  echo "❌ CHECKPOINT FAILED: Auth modal removed"
  exit 1
fi

echo "✅ All checkpoint validations passed"
exit 0
```

**Integration:** Agent runs this script after each code change. If exit code ≠ 0, automatic rollback.

**Token Savings:** Eliminates "did that work?" conversation loops.

---

**PROTOCOL 4: Cached Diagnosis Patterns**

Build knowledge base of diagnosed issues to avoid re-diagnosing similar problems:

```
# .ai-agents/known_issues.json
{
  "js_silent_failure": {
    "symptoms": ["console.log shows first line only", "no error in console"],
    "diagnosis_steps": [
      "Check for syntax error with node --check",
      "Search for Unicode artifacts (tool▁call markers)",
      "Verify try-catch boundaries exist"
    ],
    "common_causes": [
      "Corrupted text from copy-paste",
      "Mismatched quotes/braces", 
      "Scope conflict in IIFE"
    ],
    "test_commands": [
      "node --check [file]",
      "grep -n 'tool▁call\\|▁' [file]"
    ]
  }
}
```

**Usage:** When symptoms match a known pattern, agent can say:
```
Symptom matches known issue: js_silent_failure
Skipping Stage 2-3 diagnosis (cached)
Proceeding directly to Stage 4 with established solution pattern
```

**Token Savings:** Can eliminate entire diagnosis phase for repeat issues (5,000+ tokens).

---

### Resilience & Self-Correction Mechanisms

**MECHANISM 1: Automatic State Snapshots**

Before any Stage 5 action:
```bash
# Create snapshot
SNAPSHOT_ID=$(git rev-parse --short HEAD)
git tag -a "pre-action-$SNAPSHOT_ID" -m "Snapshot before [action description]"

# After action, if validation fails:
git reset --hard "pre-action-$SNAPSHOT_ID"
git tag -d "pre-action-$SNAPSHOT_ID"
```

**Benefit:** Zero-risk experimentation. Any action can be undone in 1 command.

---

**MECHANISM 2: Graceful Degradation Design**

All features should fail open, not closed:

**Bad (fail closed):**
```javascript
if (!sessionId) {
  showAuthModal();  // Blocks user
  return;  // Stops execution
}
// Rest of app
```

**Good (fail open):**
```javascript
try {
  if (sessionId) {
    loadUserData();
  } else {
    startTrialMode();  // Fallback allows usage
  }
} catch(error) {
  console.error('Auth error:', error);
  // Continue execution - user can still use site
}
// Rest of app runs regardless
```

**Principle:** Prefer degraded functionality over complete failure.

---

**MECHANISM 3: Evolutionary Test Suite**

After each fix, add test case to prevent regression:

```bash
# scripts/regression_tests.sh (grows over time)

#!/bin/zsh
echo "=== Regression Test Suite ==="

# Test 1: JS syntax (added after syntax error incident)
node --check mosaic_ui/index.html || exit 1

# Test 2: No Unicode artifacts (added after tool▁call incident)  
if grep -q '▁' mosaic_ui/index.html; then
  echo "FAIL: Unicode artifacts found"
  exit 1
fi

# Test 3: Auth modal exists (added after modal deletion incident)
if ! grep -q 'id="authModal"' mosaic_ui/index.html; then
  echo "FAIL: Auth modal missing"
  exit 1
fi

# (Future tests added here as issues are discovered and fixed)

echo "All regression tests passed"
```

**Evolution:** Each resolved issue adds a new test. Framework learns from mistakes.

---

## IMPLEMENTATION CHECKLIST

To activate this protocol:

**Immediate (today):**
- [ ] Add `.ai-agents/templates/` directory with standard templates
- [ ] Create `.ai-agents/checkpoint_validator.sh` script
- [ ] Add token budget tracking to session start messages
- [ ] Codex confirms batched-approval workflow acceptable

**This week:**
- [ ] Create `.ai-agents/known_issues.json` from recent incidents
- [ ] Implement `regression_tests.sh` with current 3 tests
- [ ] Add retrospective template to `.ai-agents/templates/`

**Ongoing:**
- [ ] After each issue: Add test to regression suite
- [ ] Monthly: Codex reviews retrospectives, updates framework
- [ ] Quarterly: Evaluate token savings, adjust budgets

---

**PROTOCOL STATUS:** Proposed, awaiting Codex approval.

**Next Action:** Codex reviews full proposal (original + addendum), approves or requests revisions.
