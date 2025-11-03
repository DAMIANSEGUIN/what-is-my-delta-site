# PS101 Implementation Gaps & Action Plan

**Date**: 2025-10-30  
**Status**: Critical gaps identified - requires spec update before continuing implementation  
**Priority**: HIGH - Cannot proceed with 7-step implementation when canonical is 10 steps

---

## Critical Gaps Identified

### 1. **Step Count Mismatch** ❌

**Current Implementation**: 7 steps (based on outdated spec)  
**Canonical Source**: 10 steps (from `api/ps101_flow.py` and `PS101_Intro_and_Prompts.docx`)

**Actual 10-Step PS101 Framework** (from `api/ps101_flow.py`):

1. **Problem Identification and Delta Analysis**
   - Multiple prompts per step (not single question)
   - Keywords: challenge, problem, facing, delta, gap, goals, values, miracle

2. **Current Situation Analysis**
   - Keywords: situation, factors, contributing, attempts, outcomes, patterns, themes

3. **Root Cause Exploration**
   - Keywords: causes, underlying, assumptions, beliefs, habits, experiences

4. **Self-Efficacy Assessment**
   - Keywords: confident, scale, 1-10, ability, skills, experiences, capabilities

5. **Solution Brainstorming**
   - Keywords: solutions, potential, five, benefits, drawbacks, aligned

6. **Experimental Design** ⚠️ (This IS the Small Experiments Framework entry point)
   - Keywords: experiment, test, low-risk, measurable, outcome, resources

7. **Obstacle Identification**
   - Keywords: obstacles, factors, hinder, self-doubt, fear, strategy

8. **Action Planning**
   - Keywords: steps, implement, measure, track, milestones, celebrate

9. **Reflection and Iteration**
   - Keywords: results, learned, experience, confidence, adjustments

10. **Building Mastery and Self-Efficacy**
    - Keywords: skills, knowledge, gained, apply, future, strategies

**Impact**: The current frontend implementation uses only 7 simplified steps. Must update to full 10-step structure.

---

### 2. **Small Experiments Framework Missing** ❌

**Status**: NOT optional - This is Phase 2 of the 4-phase journey and MUST be included in initial flow.

**From Reconciliation Plan** (lines 137-152):
> "Small Experiments Framework is essential and any other gaps, there will be no putting off elements of this build"

**What's Needed**:
- Experiment design interface (Step 6: Experimental Design)
- Hypothesis formation
- Experiment parameters (measurable outcomes, duration, resources)
- Tracking system (experiment log, results collection)
- Integration with PS101 flow (steps 6-9 specifically address experiments)

**Current Gap**: Step 6 mentions "experiment" but there's no UI framework to design/track experiments.

---

### 3. **Multi-Prompt Structure Not Implemented** ❌

**Backend Structure**: Each step has an **array of prompts** (3-6 prompts per step), not a single question.

**Example from Step 1**:
```python
"prompts": [
    "What specific challenge are you currently facing...?",
    "Why is it a problem?",
    "Reduce this to a simple problem statement",
    "If you were to wake up tomorrow... (Miracle Question)",
    "What is the 'delta' or gap...?",
    "How would solving this problem align...?"
]
```

**Current Frontend**: Each step has only ONE question/textarea.

**Impact**: Users are missing sub-prompts that help them think through each step fully.

---

### 4. **Other Missing Features** (From Reconciliation Plan)

These remain unplanned even after Phase 4:

1. ❌ **Delta Visualization** (current vs. desired state)
2. ❌ **Exploration/Exploitation framing tools**
3. ❌ **Proactive coaching intelligence** (system reads user state)
4. ❌ **Resource linking** (contextual resources per step)
5. ❌ **Journey mapping** (clear path through 4 phases)

**Note**: These may be Phase 2+ but need owners and delivery windows.

---

## Who Should Spec This?

### **Codex (You) Should Create:**

1. **Consolidated Product Spec** that merges:
   - ✅ 10 canonical prompts (from `api/ps101_flow.py`)
   - ✅ Small Experiments Framework integration
   - ✅ Multi-prompt handling (how to surface 3-6 prompts per step)
   - ✅ Experiment tracking UI (design, results, iteration)

2. **Revised Implementation Spec** replacing `MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md`:
   - Remove 7-step structure
   - Add 10-step structure with all prompts
   - Include Small Experiments Framework in Phase 1 scope
   - Define multi-prompt UI pattern (accordion? sequential sub-steps? progressive disclosure?)

3. **Small Experiments Framework Detail**:
   - How experiments are designed (Step 6)
   - How experiments are tracked (Steps 7-9)
   - How experiment results feed back into iteration (Step 9-10)
   - UI patterns for experiment timeline/backlog

---

## What I Need From You (Codex)

### **Immediate (This Week)**:

1. **PS101_Intro_and_Prompts.docx Access**
   - Path: `frontend/assets/PS101_Intro_and_Prompts.docx`
   - Need: Plaintext export or confirmation this matches `api/ps101_flow.py`
   - This is the authoritative source for prompts/hints

2. **Small Experiments Framework Spec**
   - How should users design experiments in the UI?
   - What fields/information are needed? (hypothesis, duration, success criteria, resources)
   - How are experiments tracked? (timeline view? list? calendar?)
   - How do experiment results feed into Step 9-10 reflection?

3. **Multi-Prompt Handling Decision**
   - Each step has 3-6 prompts - how should UI handle this?
   - Options:
     - **Sequential sub-steps**: Complete prompt 1 → unlock prompt 2 → etc.
     - **Progressive disclosure**: Show all prompts, user answers each
     - **Accordion**: Expandable sections per prompt
     - **Single focus**: Show one prompt at a time, advance when answered

4. **Design Tokens Source**
   - `Mosaic/README_UI_SKIN.txt` was referenced but not found in repo
   - Found `mosaic_ui/css/tokens.css` - is this the source?
   - Need: Confirmation of color palette, spacing, typography

---

## Action Items

### **For Codex** (Product Spec):

- [ ] Review `api/ps101_flow.py` (10-step structure)
- [ ] Export/read `frontend/assets/PS101_Intro_and_Prompts.docx`
- [ ] Create consolidated spec: `PS101_CANONICAL_SPEC_V2.md`
  - 10 steps with all prompts
  - Small Experiments Framework detail
  - Multi-prompt UI pattern decision
- [ ] Define Small Experiments UI components
- [ ] Sequence remaining features (Delta viz, exploration/exploit, etc.)

### **For Cursor** (Implementation):

- [ ] **STOP** current 7-step implementation
- [ ] Wait for `PS101_CANONICAL_SPEC_V2.md`
- [ ] Update `PS101_STEPS` array to 10 steps
- [ ] Implement multi-prompt handling pattern (per Codex spec)
- [ ] Build Small Experiments Framework UI (Step 6-9)
- [ ] Update progress indicator (10 dots, not 7)
- [ ] Update validation logic for new step structure

---

## Next Steps

1. **You (Codex)** review this document and confirm gaps
2. **You** create `PS101_CANONICAL_SPEC_V2.md` with:
   - 10-step structure
   - Small Experiments Framework
   - Multi-prompt UI pattern
   - Design token confirmation
3. **Hand off** to Cursor for implementation
4. **Cursor** implements Phase 1 with correct 10-step structure + experiments

---

## Questions for Codex

1. **Multi-Prompt Pattern**: How should we handle 3-6 prompts per step?
   - Sequential sub-steps?
   - Progressive disclosure?
   - Accordion?
   - Single focus?

2. **Small Experiments UI**: What does the experiment design interface look like?
   - Form fields? (hypothesis, duration, success criteria)
   - Timeline view? Calendar?
   - How do results integrate with Step 9-10?

3. **Design Tokens**: Is `mosaic_ui/css/tokens.css` the authoritative source?

4. **Feature Priority**: After 10-step PS101 + Experiments, what's next?
   - Delta visualization?
   - Exploration/exploitation tools?
   - Coaching intelligence?

---

**Status**: Waiting on Codex spec before continuing implementation.

