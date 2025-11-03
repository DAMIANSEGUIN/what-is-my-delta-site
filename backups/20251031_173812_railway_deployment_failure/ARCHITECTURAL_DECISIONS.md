# Architectural Decisions Log

**Project:** Mosaic Platform - PS101 v2
**Purpose:** Record all major architectural and design decisions for agent reference
**Owner:** Codex (Project Management Agent)
**Maintained By:** Codex - Monthly review cycle
**Last Updated:** 2025-10-31
**Next Audit:** 2025-11-30

---

## How to Use This Document

**Before making ANY architectural decision:**
1. Check if similar decision already exists here
2. If exists: Follow the existing decision (maintain consistency)
3. If new: Document the decision before implementing
4. Update "Last Updated" date
5. Notify Codex of new decisions for review

**All agents MUST read this document before:**
- Making code changes
- Starting new features
- Refactoring existing code
- Starting a new session (context refresh)

**Maintenance Schedule:**
- **Monthly Audit:** Codex reviews all active decisions (last day of each month)
- **Quarterly Deep Review:** All team members review decisions together
- **On-Demand:** After major incidents or architectural changes

---

## Decision Index

| # | Decision | Date | Status |
|---|----------|------|--------|
| 001 | Single-file frontend architecture | 2025-10-27 | ✅ Active |
| 002 | State management v2 structure | 2025-10-30 | ✅ Active |
| 003 | Inline forms for experiment data collection | 2025-10-31 | ✅ Approved |
| 004 | Step 10 Mastery Dashboard - Placeholder approach | 2025-10-31 | ✅ Approved |
| 005 | Experiment validation timing | 2025-10-31 | ✅ Approved |
| 006 | LocalStorage as primary frontend state | 2025-10-27 | ✅ Active |
| 007 | Peripheral Calm design aesthetic | 2025-10-27 | ✅ Active |
| 008 | Multi-prompt UI pattern | 2025-10-30 | ✅ Active |

---

## Decision #001: Single-File Frontend Architecture

**Date:** 2025-10-27
**Decided By:** Damian (Project Owner) + Original implementation team
**Status:** ✅ Active (Do NOT change without explicit approval)

### Context
Frontend needs to support PS101 flow with 10 steps, 42 prompts, and experiment tracking.

### Decision
Maintain single-file architecture in `frontend/index.html`:
- All HTML, CSS, and JavaScript in one file
- No build tools (webpack, vite, etc.)
- No frameworks (React, Vue, etc.)
- Vanilla JavaScript ES6+

### Rationale
- Simplifies deployment (single file to deploy)
- No build step = faster iteration
- Maintains existing architecture consistency
- Reduces complexity for small team

### Constraints
- File is currently 3128 lines (acceptable for now)
- If exceeds 5000 lines, consider splitting in Sprint 3
- All new features must follow this pattern

### Impact
- PS101 v2 implementation: ALL code goes in `frontend/index.html`
- Cursor must NOT create separate JS/CSS files
- Codex must NOT recommend build tools

### Future Consideration
- Sprint 3: Evaluate file splitting if maintainability becomes issue
- Do NOT split proactively - wait for pain point

---

## Decision #002: State Management v2 Structure

**Date:** 2025-10-30
**Decided By:** Cursor (Implementation) + Approved by review
**Status:** ✅ Active

### Context
PS101 v1 used flat `answers` object. PS101 v2 needs nested structure for multi-prompt support.

### Decision
State structure:
```javascript
{
  currentStep: 1-10,
  currentPromptIndex: 0-n,
  steps: {
    "1": {
      prompts: [
        { response: "...", completedAt: "ISO date" }
      ]
    }
  },
  experiments: [
    { id: "exp-001", ... }
  ],
  startedAt: "ISO date",
  lastUpdated: "ISO date",
  completed: false,
  completionScores: {}
}
```

### Rationale
- Supports multiple prompts per step
- Maintains prompt history
- Enables v1→v2 migration
- Allows multiple experiments

### Implementation Details
- **localStorage key:** `ps101_v2_state` (NOT `ps101_state`)
- **Migration:** Automatic from v1 on first load
- **Auto-save:** On every state mutation
- **Validation:** Check all prompts in step, not just current

### Constraints
- Do NOT change this structure without full team review
- Do NOT mix v1 and v2 patterns
- Do NOT skip migration logic

---

## Decision #003: Inline Forms for Experiment Data Collection

**Date:** 2025-10-31
**Decided By:** Claude Code (Recommended) → Damian (Approved)
**Status:** ✅ **IMPLEMENTED** (2025-10-31) - PS101-FIX-001 complete

### Context
PS101 v2 uses browser `prompt()` and `confirm()` dialogs for obstacle/action collection. This creates UX and accessibility issues.

### Decision
Replace with **inline forms** (NOT modals):
- Forms appear inline below "Add" buttons
- Hide button when form shown
- Show button when form hidden/cancelled
- Use native HTML inputs styled with Peripheral Calm aesthetic

### Rationale
- **Faster implementation:** 1-2h vs 2-3h for modals
- **Better accessibility:** Screen readers can navigate
- **Consistent with aesthetic:** Matches existing Peripheral Calm design
- **No dependencies:** No modal library needed
- **Better UX:** Stays in context, doesn't block UI

### Alternative Rejected
**Modal dialogs** - Rejected because:
- Longer implementation time
- Requires modal component or library
- Interrupts user flow more than inline
- Can defer to future if user feedback requests

### Implementation Requirements
- Form fields: Text inputs, radio buttons, textareas, date inputs
- Validation: Inline error messages (not `alert()`)
- Auto-focus: First field when form appears
- Clear on cancel: Reset all fields
- Save on submit: Validate then update state
- Accessibility: Labels, ARIA attributes, keyboard navigation

### Code Location
- `frontend/index.html` lines 543-581 (obstacle form HTML)
- `frontend/index.html` lines 589-622 (action form HTML)
- `frontend/index.html` lines 210-214 (form container CSS)
- `frontend/index.html` lines 3089-3231 (obstacle form event listeners)
- `frontend/index.html` lines 3233-3318 (action form event listeners)

### Implementation Status
- ✅ **Completed:** 2025-10-31 (Task PS101-FIX-001)
- ✅ **Browser prompts removed:** All `prompt()` and `confirm()` calls replaced
- ✅ **Inline validation:** Error messages appear below fields (no `alert()`)
- ✅ **Keyboard navigation:** Tab order, ESC to cancel, Enter to submit
- ✅ **Accessibility:** Labels, ARIA attributes, screen reader compatible

### Testing Requirements
- Keyboard navigation (Tab through fields)
- Screen reader announces fields
- Validation shows inline errors
- Cancel clears form state
- Save persists to localStorage

---

## Decision #004: Step 10 Mastery Dashboard - Placeholder Approach

**Date:** 2025-10-31
**Decided By:** Claude Code (Recommended) → Damian (Approved)
**Status:** ✅ Approved for implementation

### Context
Step 10 prompts exist, but full Mastery Dashboard (aggregated view, momentum tracker, pattern analysis) would take 6-8 hours to implement.

### Decision
Deploy with **placeholder** approach:
- Show completion message
- Display basic experiment summary (hypothesis, actions count, obstacles count, confidence change)
- Add "Coming Soon" section explaining future dashboard features
- Allow download summary (existing feature)
- Allow start over (existing feature)

### Rationale
- **Unblocks deployment:** Don't delay entire feature for one component
- **Sets expectations:** Users know dashboard is coming
- **Shows value:** Basic summary still useful
- **Fast implementation:** 30 minutes vs 6-8 hours
- **Validates approach:** Can gather user feedback before building full dashboard

### Full Dashboard Deferred To
**Sprint 2** - Full implementation includes:
- Skills gained aggregation
- Momentum tracker (Action/Momentum metrics vs baseline)
- Pattern analysis across experiments
- Next experiment suggestions based on Step 9 reflection
- Journey visualization
- Export/share functionality

### Implementation Requirements
**Placeholder must include:**
- Congratulatory message
- Experiment summary card (if experiment exists)
- "Coming Soon" section with feature list
- Download summary button
- Start over button

**Code Location:**
- `frontend/index.html` around line 2700 (renderCompletionScreen function)

**Testing:**
- Verify shows when Step 10 complete
- Verify experiment summary displays correct data
- Verify buttons work (download, start over)

---

## Decision #005: Experiment Validation Timing

**Date:** 2025-10-31
**Decided By:** Claude Code (Review finding) → Approved
**Status:** ✅ Approved for fix

### Context
Current implementation only validates experiment fields when user is on last prompt of Steps 6-9. If user navigates back and forward, validation doesn't re-check.

### Problem
- User could bypass validation by navigating backward
- Inconsistent validation state
- Data integrity risk

### Decision
Validate experiment requirements on **last prompt of each experiment step**, regardless of navigation path:
- **Step 6:** Check hypothesis + success metric + at least one date
- **Step 7:** Check at least 1 obstacle with strategy
- **Step 8:** Check at least 3 actions
- **Step 9:** Check reflection outcome + learning + confidence score

### Implementation Changes
- Update `updateNavButtons()` function (lines 2320-2370)
- Always check experiment validation for Steps 6-9, not just when `isLastPrompt`
- Auto-create experiment if doesn't exist when reaching Step 6 last prompt
- Add `ensureExperiment()` helper method to PS101State

### Code Location
- `frontend/index.html` lines 2320-2370 (updateNavButtons)
- `frontend/index.html` line 2165 (add ensureExperiment method)
- `frontend/index.html` lines 2515-2525 (renderCurrentStep experiment creation)

### Testing Requirements
- Navigate forward through Steps 6-9 (should validate)
- Navigate backward then forward (should re-validate)
- Try to advance without required fields (should block)
- Verify experiment auto-created on Step 6

---

## Decision #006: LocalStorage as Primary Frontend State

**Date:** 2025-10-27
**Decided By:** Original architecture
**Status:** ✅ Active

### Context
Frontend needs to persist user's PS101 progress across sessions.

### Decision
Use **localStorage** as primary state storage:
- Key: `ps101_v2_state`
- Format: JSON string
- Auto-save on every state mutation
- No backend sync (Phase 1)

### Rationale
- Simple implementation
- Works offline
- Immediate persistence
- No backend dependency

### Future Evolution
**Sprint 2:** Add backend sync
- Extend `/wimd/ask` pipeline to accept experiments array
- Debounce network writes (1s delay)
- Show "Syncing..." / "Saved" indicator
- Preserve compatibility with localStorage fallback

### Constraints
- Do NOT rely on backend for PS101 state in Phase 1
- Do NOT remove localStorage (keep as fallback even with backend)
- Do NOT assume localStorage is infinite (reasonable size limits)

---

## Decision #007: Peripheral Calm Design Aesthetic

**Date:** 2025-10-27
**Decided By:** Product design (from spec)
**Status:** ✅ Active - All new UI must follow

### Context
Mosaic platform uses "Peripheral Calm" design philosophy.

### Decision
All UI components must follow Peripheral Calm aesthetic:
- **Colors:** Use CSS variables from root (--fg, --muted, --line, --hair, --accent)
- **Typography:** System sans, 13-15px, generous line-height
- **Spacing:** Whitespace > content, calm not cramped
- **Interactions:** Smooth 180-220ms transitions
- **Feedback:** Subtle (no bold reds, use neutral greys and soft amber #f5d48a)
- **Focus:** High-contrast 2px outline for accessibility
- **No clutter:** Minimal UI, progressive disclosure

### Implementation Requirements
**New components must:**
- Reuse existing CSS variables (do NOT add new colors without approval)
- Match existing spacing patterns (8px base grid)
- Use existing button classes (.btn-primary, .btn-secondary)
- Smooth transitions on show/hide (fade, not instant)
- Subtle focus states (outline, not harsh shadows)

### Examples in Codebase
- Progress dots (lines ~200-250 in CSS)
- PS101 input card (lines ~250-300 in CSS)
- Experiment components (lines 179-208 in CSS)

### Anti-Patterns (Do NOT use)
- ❌ Bright red errors (#FF0000) → Use #d63638
- ❌ Instant show/hide → Use fade transitions
- ❌ Heavy shadows → Use subtle borders
- ❌ Bold/aggressive typography → Use regular weight
- ❌ Tight spacing → Use generous whitespace

---

## Decision #008: Multi-Prompt UI Pattern

**Date:** 2025-10-30
**Decided By:** PS101 v2 spec
**Status:** ✅ Active

### Context
PS101 v2 has 42 prompts across 10 steps (vs v1 which had 1 prompt per step).

### Decision
Show **one prompt at a time** with progression:
1. Display current prompt with textarea
2. Show "Prompt X of Y" progress indicator
3. Previous prompts collapse into summary chips
4. "Next Prompt →" button enabled when meets minChars
5. After last prompt in step, show "Next Step →"
6. Experiment components shown on last prompt of Steps 6-9

### Rationale
- **Focus:** One question at a time reduces cognitive load
- **Progress:** Clear indication of how many prompts remain
- **Review:** Can expand previous prompts to edit
- **Validation:** Each prompt validated before advancing

### Implementation Details
- **State tracking:** `currentPromptIndex` (0-based)
- **Navigation:** `nextPrompt()`, `prevPrompt()` methods
- **Validation:** Check `minChars` per prompt before enabling Next
- **Auto-save:** On completing each prompt

### Constraints
- Do NOT show all prompts at once
- Do NOT allow advancing without meeting minChars
- Do NOT reset `currentPromptIndex` when navigating between steps (use 0 for new step)

---

## Adding New Decisions

When adding a new decision, use this template:

```markdown
## Decision #XXX: [Short Title]

**Date:** YYYY-MM-DD
**Decided By:** [Who made decision]
**Status:** ✅ Approved / 🔄 In Discussion / ❌ Rejected

### Context
[What problem are we solving? What's the current situation?]

### Decision
[What did we decide to do? Be specific and clear.]

### Rationale
[Why this approach? What alternatives were considered?]

### Alternative Rejected (if applicable)
[What other options were considered and why were they rejected?]

### Implementation Requirements
[What needs to be done to implement this decision?]

### Code Location
[Where in the codebase is this relevant?]

### Testing Requirements
[How will we verify this is working correctly?]

### Future Consideration (if applicable)
[When might we revisit this decision?]

### Constraints
[What limitations or rules must be followed?]
```

---

## Decision Review Schedule

**Monthly:** Review all active decisions
- Are they still valid?
- Do any need updating?
- Should any be deprecated?

**Before major features:** Review relevant decisions
- Example: Before implementing backend sync, review Decision #006

**After incidents:** Check if decision contributed
- If yes: Update decision or add constraints
- If no: Document incident separately

---

**END OF ARCHITECTURAL DECISIONS LOG**

**Last Updated:** 2025-10-31
**Next Review:** 2025-11-30
