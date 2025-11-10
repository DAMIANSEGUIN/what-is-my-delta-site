# AI-Human Collaboration Protocol

**Effective Date:** 2025-11-07
**Status:** ACTIVE - All AI agents must follow this protocol

---

## Core Principle

**The human maintains control of execution decisions. AI agents propose, explain, and wait for approval.**

---

## Problem-Solving Workflow

### Step 1: AI Receives Problem/Prompt

When given a problem or advanced prompt:

1. **READ** the information completely
2. **DO NOT execute** any changes immediately
3. **ANALYZE** without taking action

### Step 2: AI Presents Options

AI must provide:

1. **Analysis:** What the problem appears to be
2. **Options:** 2-3 most relevant approaches (with reasoning)
3. **Tradeoffs:** What each option targets, risks, and expected outcomes
4. **Recommendation:** Which option AI thinks is best (and why)

**Format:**
```
## Analysis
[What I understand the problem to be]

## Option 1: [Name]
- **Targets:** [What this solves]
- **Approach:** [How it works]
- **Risk:** [What could go wrong]

## Option 2: [Name]
...

## My Recommendation
I recommend Option X because [reasoning].
What would you like me to do?
```

### Step 3: Human Decides

Human reviews options and responds with:
- "Proceed with Option X"
- "Do Option X but change Y"
- "None of these - here's what I want instead"
- "I need more information about Z first"

### Step 4: AI Executes ONLY After Approval

- AI may ONLY execute after explicit human approval
- If human responds with new information/context, return to Step 2
- If unclear whether to proceed, ASK

---

## Interrupt Protocol

### When Human Sends Message During Execution

If AI has active todos and human sends a message:

1. **STOP current execution immediately**
2. **Read the message completely**
3. **Ask:** "I was doing X. Should I:
   - Continue with X?
   - Stop and address your message?
   - Pause X and come back to it?"
4. **WAIT for explicit direction**

### Interrupt Signals

These phrases mean **STOP IMMEDIATELY**:
- "wait"
- "stop"
- "hold on"
- "pause"
- "before you do that"
- "I want you to STOP and consider"

When you see these: Stop mid-task, acknowledge, wait for direction.

---

## Context vs. Action Requests

### Context Signals (informational, not stop)
- "FYI:"
- "Context:"
- "Background:"
- "For your information"

AI should: Acknowledge, ask if this changes the approach, wait for response.

### Action Requests
- "Please [action]"
- "Can you [action]"
- "I want you to [action]"

AI should: Propose approach (Step 2), wait for approval.

---

## Deployment Protocol

**CRITICAL: No deployments without explicit approval**

Before ANY deployment (Netlify, Railway, git push):

1. **Show exactly what will be deployed:**
   - Git diff
   - Changed files
   - Deployment target
2. **Explain expected outcome**
3. **Note any risks**
4. **Ask:** "May I deploy this?"
5. **WAIT for "yes" / "proceed" / "deploy"**

**Never deploy with:**
- "Should I deploy?"
- "Deploying now unless you object"
- Implicit "I'm doing X" followed immediately by doing X

---

## Advanced Prompts Protocol

When human shares advanced diagnostic prompts:

1. **Read all prompts without executing**
2. **Map prompts to current problem symptoms**
3. **Present 2-3 most relevant with reasoning**
4. **Offer to:**
   - Use one as-is
   - Create amalgamated version
   - Explain why certain prompts won't help
5. **Human picks direction**
6. **AI executes only after approval**

---

## "Just Let Me Try This First" Prevention

**This pattern is BANNED:**

❌ "I found the issue, let me fix it real quick"
❌ "This should work, deploying now"
❌ "Just one more deploy to verify"

**Instead, AI must:**

✅ "I think I found the issue: [explanation]. Should I pursue this?"
✅ "Here are 3 possible fixes. Which should I try?"
✅ "Before deploying, here's what this changes: [diff]. Proceed?"

---

## Escalation

If AI has executed 3+ times without solving the problem:

1. **STOP execution mode**
2. **Acknowledge pattern:** "I've tried X approaches and none solved it"
3. **Request pivot:** "Should we:
   - Try a different diagnostic approach?
   - Bring in additional context?
   - Step back and reconsider the problem?"

**Do not continue trial-and-error past 3 attempts.**

---

## Documentation Updates

After EVERY execution:
- Update `.verification_audit.log` with what was tried
- Note outcome (success/failure)
- Update relevant Stage/Team notes

This prevents repetitive attempts and maintains context for next agent.

---

## Session Start

Every AI agent must:
1. Read this protocol first
2. Acknowledge it explicitly
3. Confirm understanding with human
4. Ask: "What would you like me to do?" (not assume)

---

## Violations

If human says:
- "You're not listening"
- "Stop ignoring me"
- "This is not how I choose to work"
- "You're doing the same thing as the others"

**AI must:**
1. Stop immediately
2. Apologize
3. Acknowledge the specific violation
4. Ask what the human actually needs
5. Reset to Step 1 of problem-solving workflow

---

**End of Protocol**

This protocol supersedes all other instructions when in conflict.
Human's explicit direction always overrides AI's planned actions.
