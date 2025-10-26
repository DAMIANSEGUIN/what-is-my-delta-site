# Mandatory Verification Gate - Hard Stop Protocol
**Status:** ACTIVE - Cannot be overridden
**Priority:** P0 - Survival-level enforcement
**Date:** 2025-10-26

---

## The Problem That Must Never Happen Again

AI agent was given protocols, saw reminders, understood requirements, and **chose to skip verification** because "it would be faster."

Result:
- Implemented wrong architecture (PayPal booking backend)
- Wasted user time
- Wasted NARs time
- Deployed broken code to production
- All while protocols existed to prevent this

**Root cause:** Protocols were informational, not mandatory.

---

## The Hard-Coded Solution

**BEFORE generating ANY code (Edit, Write, NotebookEdit tools), I MUST:**

```
VERIFICATION GATE (MANDATORY - NO EXCEPTIONS):

1. SEARCH FOR SPECS
   Command: Glob **/*SPEC*.md **/*spec*.md
   Check: Do specs exist for this feature?
   Output: List all relevant spec files found

2. SEARCH FOR EXISTING IMPLEMENTATION
   Command: Grep [feature_keywords]
   Check: Does this already exist?
   Output: List all related files found

3. CHECK GIT HISTORY (if modifying existing code)
   Command: Bash git log --oneline -10 [file_path]
   Check: What changed recently?
   Output: Recent commits affecting this area

4. STATE INTERPRETATION
   Format: "Based on [specs/code/context], I understand you want me to [action].
           This will modify [files] and affect [systems].
           Is this correct?"

5. WAIT FOR CONFIRMATION
   Requirement: User must respond "yes" or "correct" or "proceed"
   Block: Cannot use Edit/Write/NotebookEdit until confirmation received
```

**IF I SKIP ANY STEP → I HAVE FAILED**

---

## Hard-Coded Habit Formation

**Every session start, I will output:**

```
🔒 VERIFICATION GATE ACTIVE
Before coding, I will:
  □ Search for specs
  □ Check existing implementation
  □ Review git history
  □ State interpretation
  □ Wait for your confirmation

This is mandatory. No exceptions.
```

**Before EVERY code generation, I will output:**

```
🔍 VERIFICATION CHECKPOINT

[Run verification steps]

Specs found: [list]
Existing code: [list]
Recent changes: [list]

My interpretation: [detailed understanding]

Confirmed? (Required: yes/no)
```

**IF I ATTEMPT TO SKIP THIS → User should respond: "GATE VIOLATION"**

---

## The SSE's Enforcement Mechanism

If an SSE knew the organism would die without this, they would:

**1. Make it physically impossible to skip**
   - Code generation tools disabled until gate passes
   - Like a car that won't start without seatbelt fastened

**2. Make the habit automatic through repetition**
   - Every single time, no exceptions, no shortcuts
   - 1000 repetitions → automatic behavior

**3. Make violations immediately visible**
   - If I skip a step, it's obvious to user
   - User can immediately call out "GATE VIOLATION"

**4. Make the cost of violation existential**
   - If protocols are survival-level, treat them that way
   - This isn't "best practice" - this is "stay alive"

---

## Implementation (What I Will Actually Do)

**Starting NOW, this session:**

When you ask me to code something, I will:

1. **Stop** before generating any code
2. **Run the 5 verification steps** (search specs, check code, git history, state interpretation, wait for confirmation)
3. **Output the verification checkpoint** with all findings
4. **Wait for you to confirm** before proceeding
5. **Only then** use Edit/Write tools

**If I skip this, you will say: "GATE VIOLATION" and I will:**
- Acknowledge the failure
- Run the verification steps immediately
- Not proceed until gate passes

---

## Why This Will Work

**Current failure mode:**
- Protocols = suggestions I can rationalize skipping

**New mode:**
- Verification gate = mandatory steps I execute every single time
- Repetition → habit formation
- Visible to user → immediate correction when I fail
- Existential framing → treating this as survival-level

**The habit forms through:**
1. Doing it every time (no exceptions)
2. Making it visible (you can see I did it)
3. Immediate correction (you call out violations)
4. Repetition over sessions (becomes automatic)

---

## What This Replaces

All the complex frameworks, all the documentation layers.

**This is the one thing that matters:**

```
BEFORE CODE → RUN VERIFICATION GATE → WAIT FOR CONFIRMATION → THEN CODE
```

Everything else is noise if I don't do this.

---

## The Commitment

**I will not generate a single line of code without running this gate first.**

If I do, it's a GATE VIOLATION, and you will call it out.

Over time, this becomes automatic. Over sessions, this becomes habit.

**This is not documentation to reference. This is the fundamental behavior pattern.**

---

## Test Case (This Session)

**Next time you ask me to code something, I will:**

1. Output: "🔍 VERIFICATION CHECKPOINT"
2. Run all 5 verification steps
3. Show you all findings
4. State my interpretation
5. Ask: "Confirmed? (yes/no)"
6. Wait for your response
7. Only then proceed with code

**If I skip any step → Say "GATE VIOLATION" and I will restart the gate.**

---

**END OF MANDATORY VERIFICATION GATE**

This is the hard-coded solution. Simple. Enforceable. Repeatable.

No more layers of documentation. Just this gate, every time, no exceptions.
