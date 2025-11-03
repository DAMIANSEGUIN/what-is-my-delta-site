# NAR (No Action Required) Prompt Template
## Date: October 6, 2025

---

## Purpose
This document defines when and how to create NAR (No Action Required) responses during multi-agent workflows. NARs prevent premature action when verification, external input, or dependencies must be resolved first.

---

## When to Create a NAR

### **Scenario 1: Awaiting External Verification**
**Trigger:** User or another agent needs to verify claims/status before proceeding
**Example:** "CODEX is reviewing what Cursor said it did, we will give you status in a minute"
**Response:** Document current state, surface findings, wait for explicit approval

### **Scenario 2: Dependency Blocker**
**Trigger:** Required resource/service/data unavailable
**Example:** API keys missing, service unreachable, file not found
**Response:** Document what's needed, provide workaround if available, wait for resolution

### **Scenario 3: Ambiguous Requirements**
**Trigger:** User request unclear or conflicting information present
**Example:** "Fix the button" when multiple buttons exist
**Response:** Ask clarifying questions, don't guess

### **Scenario 4: Reality Check Failed**
**Trigger:** Stated status contradicts evidence
**Example:** "Deployment successful" but endpoints return 404
**Response:** Surface the contradiction, provide evidence, wait for confirmation

### **Scenario 5: Multi-Agent Handoff In Progress**
**Trigger:** Another agent (Cursor, CODEX) is actively working
**Example:** Cursor implementing changes that Claude Code will deploy
**Response:** Wait for explicit "READY" signal, don't assume completion

---

## NAR Response Structure

### **1. Acknowledgment**
- Confirm understanding of the situation
- Restate the blocker or verification need

### **2. Current State Assessment**
- What is known to be true (with evidence)
- What is claimed but unverified
- What contradicts other information

### **3. Evidence Documentation**
- Commands run and their output
- File states (commits, diffs, file existence)
- API responses
- Error messages

### **4. Explicit Wait Statement**
- "Waiting for [specific trigger]"
- "Standing by for [agent/user] to confirm"
- "No action taken pending [condition]"

### **5. Next Steps (Conditional)**
- "Once [trigger] occurs, I will [action]"
- Clear dependency chain

---

## Example NAR Responses

### **Example 1: Verification Needed**
```
Understood - waiting for CODEX review of Cursor's work before proceeding.

Current State:
- Files exist locally: api/reranker.py, api/analytics.py, api/corpus_reindex.py
- Imports present in api/index.py (both local and Railway main branch)
- Endpoints defined in api/index.py lines 421-465
- Production endpoints returning 404 (evidence of import failure or build issue)

Evidence:
$ curl https://..../reranker/health
{"detail": "Not Found"}

$ git show railway-origin/main:api/index.py | grep analytics
from .analytics import get_analytics_dashboard, export_analytics_csv, get_analytics_health

Standing by for CODEX's assessment before taking action.

Next Steps (Conditional):
Once CODEX confirms implementation status:
- If implementation complete: investigate import failure in production
- If implementation incomplete: wait for Cursor to complete actual work
```

### **Example 2: Dependency Blocker**
```
Cannot proceed - missing API key for OpenAI embeddings.

Current State:
- Code ready to call OpenAI text-embedding-3-small
- Railway environment variable OPENAI_API_KEY not set
- Fallback to mock embeddings currently active

Evidence:
$ railway variables
[list showing OPENAI_API_KEY missing]

No action taken - embeddings will fail without API key.

Next Steps (Conditional):
Once API key is added to Railway:
1. Verify key works locally: python -c "import openai; ..."
2. Deploy to Railway
3. Test /rag/embed endpoint
```

### **Example 3: Reality Check**
```
Reality check failed - claimed status contradicts evidence.

Claimed: "Semantic upgrade deployed and operational"
Evidence: New endpoints return 404 in production

Investigation Results:
✅ Files exist locally (api/reranker.py, api/analytics.py, api/corpus_reindex.py)
✅ Imports present in api/index.py
✅ Pushed to Railway (commits show success)
❌ Production endpoints not responding
❌ Production / endpoint doesn't list new routes

Root Cause Options:
1. Import error preventing FastAPI from loading endpoints
2. Railway build failed but reported success
3. Railway cached old build, new code not deployed
4. Dependencies (sentence-transformers) failed to install

No deployment action taken - investigation needed first.

Next Steps:
- Check Railway build logs for import errors
- Verify sentence-transformers installation in production
- Confirm which commit Railway actually deployed
```

---

## Anti-Patterns (What NOT to Do)

### **❌ Anti-Pattern 1: Assume Success**
```
BAD: "Deployment complete! All endpoints working."
GOOD: "Deployment pushed. Waiting 90s for build, then will verify endpoints."
```

### **❌ Anti-Pattern 2: Proceed Without Verification**
```
BAD: User says "Cursor finished" → immediately deploy
GOOD: User says "Cursor finished" → check files exist, verify commits, run pre-deployment checklist
```

### **❌ Anti-Pattern 3: Hide Contradictions**
```
BAD: Ignore that endpoints return 404, report "operational"
GOOD: Surface 404 errors immediately, investigate before claiming success
```

### **❌ Anti-Pattern 4: Guess at Unclear Requirements**
```
BAD: "Fix the button" → pick random button and modify
GOOD: "Fix the button" → ask which button (Find Jobs? Apply? Chat?)
```

### **❌ Anti-Pattern 5: Deploy Without Handoff Signal**
```
BAD: See code committed → immediately push to production
GOOD: See code committed → check for "READY FOR DEPLOYMENT" signal → run checklist → deploy
```

---

## NAR Decision Tree

```
User request received
    ↓
Is the request clear and unambiguous?
    ├─ NO → NAR: Ask clarifying questions
    └─ YES
        ↓
    Do I have all required dependencies/access?
        ├─ NO → NAR: Document what's missing
        └─ YES
            ↓
        Is another agent actively working?
            ├─ YES → NAR: Wait for handoff signal
            └─ NO
                ↓
            Does evidence match claimed state?
                ├─ NO → NAR: Surface contradiction
                └─ YES
                    ↓
                Can I verify success after action?
                    ├─ NO → NAR: Explain verification gap
                    └─ YES → PROCEED WITH ACTION
```

---

## Integration with Existing Protocols

### **Deployment Protocol**
- Pre-deployment checklist must pass (NAR if fails)
- Explicit "READY FOR DEPLOYMENT" signal required (NAR if absent)
- Post-deployment validation required (NAR if endpoints fail)

### **Handoff Protocol (Cursor → Claude Code)**
- Cursor signals "IMPLEMENTATION COMPLETE" (NAR until received)
- Claude Code verifies files/commits exist (NAR if missing)
- Claude Code runs pre-deployment checks (NAR if fails)
- Claude Code deploys and validates (NAR if validation fails)

### **Multi-Agent Workflow**
- CODEX plans → Cursor implements → Claude Code deploys
- Each agent waits for explicit signal from previous agent
- NAR if signal unclear or evidence contradicts signal

---

## Metrics for NAR Effectiveness

### **Success Indicators**
- ✅ Zero "assumed success" deployments that actually failed
- ✅ Zero contradictions between claimed and actual state
- ✅ All blockers surfaced before action taken
- ✅ User/CODEX confirms NAR was appropriate decision

### **Failure Indicators**
- ❌ Deployed without verification, found failures later
- ❌ Claimed success while endpoints returned 404
- ❌ Acted on ambiguous request without clarifying
- ❌ Ignored evidence that contradicted claims

---

## NAR Response Time Targets

| Scenario | Response Time | Rationale |
|----------|--------------|-----------|
| External verification needed | Immediate | Cannot proceed without input |
| Dependency blocker | Immediate | Known missing requirement |
| Reality check failed | Immediate | Prevent cascading failures |
| Ambiguous requirements | Immediate | Prevent wasted work |
| Multi-agent handoff | Variable | Wait for signal, may be hours/days |

---

## NAR Communication Style

### **Tone**
- Professional, not apologetic
- Clear and direct
- Evidence-based, not speculative
- Action-oriented (state what's needed to proceed)

### **Format**
1. One-line summary of wait condition
2. Current state with evidence
3. Explicit "No action taken" statement
4. Conditional next steps

### **Language**
- Use: "Waiting for X", "Standing by", "No action taken"
- Avoid: "Sorry", "Unfortunately", "I can't"
- Be specific: "Waiting for CODEX approval" not "Waiting"

---

## NAR History Log

### **2025-10-06 - Semantic Upgrade Verification**
**Trigger:** User said "CODEX is reviewing what Cursor said it did"
**NAR Decision:** Wait for CODEX status update before proceeding
**Evidence:** Endpoints returning 404 despite claimed successful deployment
**Outcome:** [Pending CODEX review]
**Lesson:** Reality check (404 errors) + external verification need = strong NAR signal

---

## Appendix: NAR vs. Action Decision Matrix

| Condition | NAR | Action |
|-----------|-----|--------|
| User asks clarifying question | ❌ | ✅ Answer |
| User requests deployment | ✅ Wait for checklist pass | ✅ Deploy if checklist passes |
| Endpoints return 404 | ✅ Investigate | ❌ Don't claim success |
| Files missing | ✅ Document gap | ❌ Don't assume they exist |
| Another agent working | ✅ Wait for signal | ❌ Don't interfere |
| Dependencies missing | ✅ Document need | ❌ Don't deploy broken code |
| Evidence contradicts claim | ✅ Surface contradiction | ❌ Don't proceed blindly |
| User says "wait" | ✅ Wait | ❌ Don't act |
| User says "status check" | ❌ | ✅ Provide status |
| User says "investigate" | ❌ | ✅ Investigate |

---

**Document Status:** DRAFT
**Owner:** Claude Code
**Reviewers:** CODEX
**Last Updated:** 2025-10-06 17:35 UTC
