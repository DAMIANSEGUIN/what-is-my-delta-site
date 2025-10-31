# Cursor Agent Prompt: PS101 v2 Implementation

**Use this with Cursor's Composer/Agent mode to implement the 10-step PS101 flow**

## Agent Instructions

You are implementing the canonical 10-step PS101 problem-solving framework in vanilla JavaScript (ES6+) within `frontend/index.html`. This is a complete refactor from the existing 7-step implementation.

### Your Task

Replace the existing PS101 implementation (lines ~1727-2360) with a complete 10-step structure that includes:
1. Multi-prompt system (3-6 prompts per step)
2. Small Experiments Framework (Steps 6-9)
3. Extended state management (localStorage: `ps101_v2_state`)
4. All Peripheral Calm enhancements

### Step-by-Step Implementation Plan

#### Phase 1: Replace PS101_STEPS Array
**Location**: Lines ~1731-1796

**Action**: Replace the 7-step array with the complete 10-step structure from `api/ps101_flow.py` (lines 11-124).

**New Structure**:
```javascript
const PS101_STEPS = [
  {
    number: 1,
    title: 'Problem Identification and Delta Analysis',
    purpose: 'Define the core challenge and the delta between current and desired state',
    prompts: [
      { text: 'What specific challenge are you currently facing in your personal or professional life?', minChars: 50 },
      { text: 'Why is it a problem?', minChars: 30 },
      { text: 'Reduce this to a simple problem statement.', minChars: 30 },
      { text: 'If you were to wake up tomorrow and this problem was solved, what would be different? (Miracle Question)', minChars: 50 },
      { text: 'What is the "delta" or gap between your current situation and your desired state?', minChars: 50 },
      { text: 'How would solving this problem align with your long-term goals or values?', minChars: 30 }
    ],
    hint: 'Focus on understanding both where you are and where you want to be.',
    showDeltaVisualization: true
  },
  // ... continue for all 10 steps
];
```

 PRESERVES**:
- Step 1: 6 prompts (from `api/ps101_flow.py`)
- Step 2: 4 prompts
- Step 3: 4 prompts
- Step 4: 4 prompts
- Step 5: 4 prompts + `exploreExploitTag: true`
- Step 6: 4 prompts + `requiresExperiment: true`
- Step 7: 4 prompts + `requiresExperiment: true`
- Step 8: 4 prompts + `requiresExperiment: true`
- Step 9: 4 prompts + `requiresExperiment: true`
- Step 10: 4 prompts + `requiresExperiment: true`

#### Phase 2: Update PS101State Object
**Location**: Lines ~1798-1886

**Current Structure** (simplified):
```javascript
{
  currentStep: 1,
  answers: {},
  startedAt: null,
  lastUpdated: null,
  completed: false
}
```

**New Structure** (from spec §5.1):
```javascript
{
  currentStep: 4,
  currentPromptIndex: 2,  // NEW: Track which prompt within step
  steps: {  // NEW: Nested structure for multi-prompt responses
    "1": {
      prompts: [
        {"response": "...", "completedAt": "2025-10-30T19:55:00Z"},
        ...
      ]
    },
    ...
  },
  experiments: [  // NEW: Small Experiments Framework
    {
      "id": "exp-001",
      "title": "Experiment 1",
      "hypothesis": "...",
      "successMetric": "...",
      "duration": {"start": "...", "review": "..."},
      "resources": "...",
      "obstacles": [...],
      "actions": [...],
      "reflection": {...},
      "status": "active"
    }
  ],
  startedAt: "...",
  lastUpdated: "...",
  completed: false,
  completionScores: {"clarity": 8, "action": 8, "momentum": 7}
}
```

**Storage Key**: Change from `ps101_state` to `ps101_v2_state`

#### Phase 3: Update Rendering Functions
**Location**: Lines ~1900-2100

**Key Functions to Update**:

1. **`renderCurrentStep()`** → **`renderCurrentStep()`** (handle multi-prompt)
   - Show one prompt at a time
   - Display sub-prompt progress: "Prompt Display 3 of 6"
   - Collapse completed prompts into chips
   - Handle experiment components for Steps 6-9

2. **`updateProgressIndicator()`** → Update to handle 10 steps
   - Change `Step X of 7` → `Step X of 10`
   - Ensure all 10 dots render correctly

3. **NEW: `renderPrompt(promptIndex)`** 
   - Render individual prompt within a step
   - Handle prompt completion/collapse
   - Update character counts per prompt

4. **NEW: `renderExperiment小Canvas(stepNumber)`** (Step 6)
   - Hypothesis input
   - Success metric input
   - Duration pickers
   - Resources textarea
   - Render as structured card

5. **NEW: `renderObstacleMapping()`** (Step 7)
   - External/internal obstacle inputs
   - Strategy textarea per obstacle
   - Link to experiment

6. **NEW: `renderActionPlan()`** (Step 8)
   - Checklist with tasks
   - Date pickers for milestones
   - Accountability assignment
   - Progress tracking toggles

7. **NEW: `renderReflectionLog()`** (Step 9)
   - Outcomes textarea
   - Learning summary
   - Confidence slider (1-10, compare to Step 4)
   - Next iteration decision (Continue/Pivot/Archive)

8. **NEW: `renderMasteryDashboard()`** (Step 10)
   - Skills gained summary
   - Momentum tracker
   - Next experiment suggestion
   - Export summary button

#### Phase 4: Update HTML Structure
**Location**: Lines ~415-523

**Updates Needed**:
1. Progress dots: Already updated to 10 ✅
2. **NEW**: Add sub-prompt navigation UI
   - Mini progress indicator: "Prompt 3 of 6"
   - Completed prompt chips (collapsed, clickable to edit)
   - "Next prompt" button (unlocks when current prompt validated)
3. **NEW**: Experiment canvas container (Steps 6-9)
4. **NEW**: Delta visualization area (Step 1 summary)
5. **NEW**: Resource suggestions panel (collapsible per step)
6. **NEW**: Journey rail component (milestone mapping)

#### Phase 5: Validation Updates
**Location**: Lines ~2097-2150

**Current**: Validates single answer per step
**New**: Validate each prompt within step
- Each prompt has its own `minChars` requirement
- Step validation only passes when ALL prompts in step are completed
- Experiment-specific validation (Steps 6-9):
  - Step 6: Requires hypothesis + success metric + duration
  - Step 7: Requires at least one obstacle + strategy
  - Step 8: Requires at least 3 actionable tasks
  - Step 9: Requires reflection text + confidence score

#### Phase 6: Peripheral Calm Enhancements

1. **Delta Visualization** (Step 1)
   - After Step 1 completion, show inline summary
   - Visual gap representation (current vs desired)
   - Add to completion view

2. **Explore/Exploit Tagging** (Step 5)
   - Tag solutions as "Explore" or "Exploit"
   - Show tags on completion view
   - Simple toggle buttons per solution

3. **Contextual Coaching**
   - Update chat drawer prompts per step
   - Add inline hints (expandable) per prompt
   - Reference: `CONTEXTUAL_PROMPTS` object

4. **Resource Suggestions**
   - Collapsible panel per step
   - Step-specific resources
   - Link to existing resource library

5. **Journey Rail**
   - Show all 10 milestones
   - Highlight current position
   - Click to jump to completed steps

### Implementation Order

1. **First**: Replace PS101_STEPS array (10 steps with all prompts)
2. **Second**: Update PS101State structure (multi-prompt + experiments)
3. **Third**: Update `renderCurrentStep()` to handle multi-prompt
4. **Fourth**: Update progress indicator logic (10 steps)
5. **Fifth**: Build experiment components (Steps 6-9)
6. **Sixth**: Add Peripheral Calm enhancements
7. **Seventh**: Update validation logic
8. **Eighth**: Test full flow and fix regressions

### Critical Constraints

- ✅ Vanilla JavaScript ES6+ only (no frameworks)
- ✅ Single HTML file (`frontend/index.html`)
- ✅ Preserve generated features (auth, chat, upload, metrics cards)
- ✅ Use existing CSS variables (`--fg`, `--muted`, `--line`, `--hair`)
- ✅ No backend contract changes (extend existing `/wimd/ask` payload only)
- ✅ Peripheral Calm aesthetic (calm transitions, generous whitespace)

### Testing Checklist

After implementation:
- [ ] All 10 steps render correctly
- [ ] Multi-prompt navigation works (advance through prompts within step)
- [ ] Completed prompts collapse into chips
- [ ] Step validation requires all prompts complete
- [ ] Experiment canvas renders for Step 6
- [ ] Obstacle mapping works for Step 7
- [ ] Action plan checklist works for Step 8
- [ ] Reflection log works for Step 9
- [ ] Mastery dashboard shows for Step 10
- [ ] Progress indicator shows all 10 dots
- [ ] State saves to `ps101_v2_state` in localStorage
- [ ] Existing features still work (auth, chat, upload)
- [ ] Mobile responsive (test <768px breakpoint)
- [ ] Accessibility (keyboard nav, ARIA labels, screen reader)

### Reference Files

- **Spec**: `docs/PS101_CANONICAL_SPEC_V2.md` (complete specification)
- **Backend Structure**: `api/ps101_flow.py` (lines 11-124 for exact prompts)
- **Current Implementation**: `frontend/index.html` (lines ~1727-2360)
- **Design Tokens**: `mosaic_ui/css/tokens.css` (CSS variables reference)

### Agent Mode Instructions

When using Cursor Composer/Agent:

1. **Start with**: "Implement the PS101_STEPS array replacement with all 10 canonical steps and multi-prompt structure"

2. **Then**: "Update PS101State object to handle currentPromptIndex and experiments array as specified in PS101_CANONICAL_SPEC_V2.md section 5.1"

3. **Then**: "Update renderCurrentStep() function to display one prompt at a time with sub-prompt progress indicator"

4. **Continue incrementally** through the implementation plan above

5. **After each major change**: Verify no regressions in existing features

---

**Ready to start?** Begin with Phase 1: Replace PS101_STEPS array with the complete 10-step structure.

