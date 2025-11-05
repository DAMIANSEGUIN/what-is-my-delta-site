# PROPOSAL: Structured Troubleshooting Framework with Team Oversight
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
