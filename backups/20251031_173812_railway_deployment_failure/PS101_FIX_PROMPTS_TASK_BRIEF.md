# PS101 v2 Fix Browser Prompts - Agent Task Brief

**Task ID:** PS101-FIX-001
**Task Title:** Replace browser prompt()/confirm() dialogs with inline forms
**Agent:** Cursor
**Risk Tier:** 2 (Medium - Supervised with checkpoints)
**Estimated Effort:** 1-2 hours
**Deadline:** 2025-11-01

---

## Task Brief

### What Problem Are We Solving?
Current PS101 v2 implementation uses browser `prompt()` and `confirm()` dialogs for collecting obstacle and action data (lines 3014-3051 in frontend/index.html). This blocks the UI, is not accessible to screen readers, and provides poor mobile UX.

### Why Is This Important?
- **Accessibility:** Screen readers cannot navigate browser prompts
- **User Experience:** Dialogs block entire UI, feel clunky
- **Mobile:** Poor experience on mobile devices
- **Professionalism:** Browser prompts don't match Peripheral Calm aesthetic
- **Deployment blocker:** P0 issue preventing PS101 v2 production deploy

### Current State
- `Add Obstacle` button (line 3011) triggers browser `prompt()` for label, `confirm()` for type, `prompt()` for strategy
- `Add Action` button (line 3033) triggers browser `prompt()` for label, due date, accountability
- Users cannot Tab navigate, screen readers announce poorly, mobile keyboards cover prompts

### Desired End State
- Inline forms appear below buttons when clicked
- Forms use HTML inputs styled with Peripheral Calm aesthetic
- Tab navigation works correctly
- Screen readers can navigate all fields
- Mobile UX improved with proper input types
- Validation shows inline errors (no `alert()`)

---

## Inputs

### Required Reading (MUST read before starting)
- [ ] `docs/CURSOR_FIXES_REQUIRED.md` (lines 15-202 - complete implementation guide)
- [ ] `docs/ARCHITECTURAL_DECISIONS.md` (Decision #003 - Inline forms approved)
- [ ] `docs/PS101_CANONICAL_SPEC_V2.md` (Section 4.2 Obstacle Mapping, 4.3 Action Plan)

### Context Files
- `frontend/index.html` lines 476-546 - Existing experiment components HTML (add forms here)
- `frontend/index.html` lines 179-208 - Experiment components CSS (reference for styling)
- `frontend/index.html` lines 3010-3052 - Event listeners to replace

### Code Files to Modify
- `frontend/index.html` lines ~546 - Add obstacle form HTML
- `frontend/index.html` lines ~546 - Add action form HTML
- `frontend/index.html` lines 3010-3030 - Replace obstacle event listeners
- `frontend/index.html` lines 3032-3052 - Replace action event listeners

---

## Constraints

### Do NOT
- [ ] Do NOT use modal dialogs (Decision #003: inline forms approved)
- [ ] Do NOT add external libraries or dependencies
- [ ] Do NOT use `alert()` for validation (use inline error messages)
- [ ] Do NOT create separate JS/CSS files (Decision #001: single-file architecture)
- [ ] Do NOT change experiment data structure
- [ ] Do NOT modify PS101State methods (addObstacle, addAction)

### MUST Follow
- [ ] MUST use Peripheral Calm aesthetic (Decision #007)
- [ ] MUST use existing CSS variables (--fg, --muted, --line, etc.)
- [ ] MUST match existing form styling patterns
- [ ] MUST auto-focus first field when form appears
- [ ] MUST clear form fields on cancel
- [ ] MUST validate before saving
- [ ] MUST test keyboard navigation (Tab order)
- [ ] MUST test screen reader announcements (basic check)

### Architecture Decisions to Honor
- Decision #001: Single-file frontend architecture
- Decision #003: Inline forms for experiment data collection
- Decision #007: Peripheral Calm design aesthetic

---

## Success Criteria

### Functional Requirements
- [ ] Add Obstacle button shows inline form (obstacle form hidden by default)
- [ ] Form includes: text input (label), radio buttons (external/internal), textarea (strategy)
- [ ] Save button validates inputs and calls `PS101State.addObstacle()`
- [ ] Cancel button hides form and clears fields
- [ ] Add Action button shows inline form (action form hidden by default)
- [ ] Form includes: text input (label), text input (due), text input (accountability)
- [ ] Save button validates and calls `PS101State.addAction()`
- [ ] Obstacles and actions render correctly in lists after adding
- [ ] Remove buttons still work for both obstacles and actions

### Quality Requirements
- [ ] Code passes no linter errors
- [ ] No browser console errors
- [ ] Keyboard navigation works (Tab through fields, Enter to submit, Esc to cancel)
- [ ] Screen readers announce field labels (test with VoiceOver/NVDA basic check)
- [ ] Forms match Peripheral Calm aesthetic (neutral colors, generous spacing, calm transitions)
- [ ] Validation errors show inline below fields (not alert())
- [ ] Auto-focus works when form appears

### Documentation Requirements
- [ ] No new architectural decisions (following existing Decision #003)
- [ ] Add inline code comments for complex form logic
- [ ] Note in commit message: "Implements Decision #003 - Inline forms"

---

## Checkpoints

### Checkpoint 1: Understanding Verification ✋ STOP HERE FIRST

**Agent must output:**
```
I understand this task requires:
1. Adding two inline forms (obstacle + action) to HTML around line 546
2. Styling them with existing CSS variables to match Peripheral Calm
3. Replacing event listeners in lines 3010-3052 to show/hide forms
4. Validating inputs and showing inline errors (not alert())
5. Testing keyboard navigation and basic screen reader compatibility

Files to modify:
- frontend/index.html (HTML for forms, event listeners)

Architectural constraints:
- Must use inline forms (not modals) per Decision #003
- Must maintain single-file architecture per Decision #001
- Must match Peripheral Calm aesthetic per Decision #007

Questions/clarifications: [Any uncertainties]
```

**Damian:** Review agent's understanding, clarify if needed, then approve to proceed.

---

### Checkpoint 2: Approach Approval ✋ STOP HERE BEFORE CODING

**Agent must output:**
```
Implementation approach:

1. HTML Addition (after line 546):
   - Add `<div id="add-obstacle-form" class="hidden">` with:
     - Text input for obstacle label
     - Radio buttons for type (external/internal)
     - Textarea for strategy
     - Save and Cancel buttons
   - Add `<div id="add-action-form" class="hidden">` with:
     - Text input for action label
     - Text input for due date
     - Text input for accountability
     - Save and Cancel buttons

2. CSS Styling (inline or in existing style block):
   - Use existing form patterns from experiment components
   - Match padding, margins, borders from existing inputs
   - Use CSS variables for colors
   - Add fade transition for show/hide

3. JavaScript Event Listeners (lines 3010-3052):
   - Obstacle button: Show form, hide button, focus first input
   - Obstacle cancel: Hide form, show button, clear inputs
   - Obstacle save: Validate (require label + strategy), show inline error if missing, call addObstacle if valid
   - Action button: Show form, hide button, focus first input
   - Action cancel: Hide form, show button, clear inputs
   - Action save: Validate (require label), call addAction

4. Validation approach:
   - Check required fields on save click
   - If missing: Add red text below field (e.g., "Please describe the obstacle")
   - Auto-remove error after 5 seconds or on input change
   - If valid: Save data, clear form, hide form, show button, re-render list

Estimated time: 1.5 hours
Risks: None identified (straightforward implementation)
```

**Damian:** Review approach, check it follows architectural decisions, approve or request changes.

---

### Checkpoint 3: Implementation Review ✋ STOP AFTER CODING

**Agent must:**
- [ ] Show HTML additions (full form markup)
- [ ] Show CSS changes (if any inline styles needed)
- [ ] Show event listener replacements (full functions)
- [ ] Explain what each change does
- [ ] Note any deviations from approved approach

**Damian will:**
- [ ] Read all code changes
- [ ] Check forms match Peripheral Calm style
- [ ] Verify validation logic is sound
- [ ] Check no unintended side effects
- [ ] Approve to proceed to testing

**If issues found:** Agent fixes, re-checkpoint before testing.

---

### Checkpoint 4: Testing Verification ✋ STOP AFTER TESTING

**Agent must complete and report:**

**Manual Tests:**
1. ✅/❌ Click "Add Obstacle" - form appears, button hides
2. ✅/❌ Tab through obstacle form - reaches all fields in order
3. ✅/❌ Try to save with empty label - inline error shows
4. ✅/❌ Fill valid data and save - obstacle appears in list
5. ✅/❌ Click cancel - form hides, fields clear, button reappears
6. ✅/❌ Click "Add Action" - form appears, button hides
7. ✅/❌ Tab through action form - reaches all fields
8. ✅/❌ Save with valid data - action appears in list
9. ✅/❌ Remove obstacle - disappears from list
10. ✅/❌ Remove action - disappears from list
11. ✅/❌ Reload page - obstacles and actions persist
12. ✅/❌ Check console - no errors

**Accessibility Check:**
1. ✅/❌ Tab order logical
2. ✅/❌ Focus visible (outline shows)
3. ✅/❌ Labels associated with inputs
4. ✅/❌ Error messages readable

**Agent reports:** "All tests passed" or "Test X failed with error Y"

**Damian will:**
- [ ] Verify test results make sense
- [ ] Run manual tests yourself
- [ ] Check for any regressions
- [ ] Approve for commit

---

### Checkpoint 5: Final Approval ✋ STOP BEFORE COMMIT

**Agent confirms:**
- [ ] All checkpoints passed
- [ ] All success criteria met
- [ ] No console errors
- [ ] Keyboard navigation works
- [ ] Forms match Peripheral Calm aesthetic

**Suggested commit message:**
```
Fix PS101 v2 Issue #1: Replace browser prompts with inline forms

- Add inline forms for obstacle and action collection
- Forms use HTML inputs styled with Peripheral Calm aesthetic
- Implement inline validation (no alert())
- Support keyboard navigation and screen readers
- Implements Decision #003 from ARCHITECTURAL_DECISIONS.md

Closes: PS101-FIX-001
```

**Damian:**
- [ ] Final review
- [ ] Verify backup exists: `backups/20251031_095426_ps101_v2_implementation/`
- [ ] Approve commit message
- [ ] Execute commit: `git add frontend/index.html && git commit -m "[message]"`

**After commit:**
- [ ] Monitor browser console for 5 minutes
- [ ] Test on live page (if deployed)
- [ ] Mark task PS101-FIX-001 as complete

---

## Testing Plan

### Automated Tests
None available (frontend-only, manual testing required)

### Manual Testing Steps
1. **Obstacle form test:**
   - Navigate to PS101 Step 7
   - Click "Add Obstacle" button
   - Verify form appears, button hides
   - Try to save with empty label → Should show inline error
   - Fill: label="Time constraints", type=External, strategy="Block 30-min slots"
   - Click Save
   - Verify obstacle appears in list with external badge
   - Verify form closes, button reappears

2. **Action form test:**
   - Navigate to PS101 Step 8
   - Click "Add Action" button
   - Verify form appears, button hides
   - Try to save with empty label → Should show inline error
   - Fill: label="Schedule daily standup", due="2025-11-05", accountability="Team lead"
   - Click Save
   - Verify action appears in checklist
   - Verify form closes, button reappears

3. **Keyboard navigation test:**
   - Open obstacle form
   - Press Tab repeatedly
   - Verify: label input → external radio → internal radio → strategy textarea → Save button → Cancel button → (Tab out)

4. **Cancel test:**
   - Open obstacle form
   - Fill some data
   - Click Cancel
   - Verify: form hides, fields cleared, button shows

5. **Persistence test:**
   - Add obstacle
   - Add action
   - Reload page
   - Verify both still present

### Edge Cases
- [ ] Very long obstacle label (>200 chars) - should handle gracefully
- [ ] Special characters in inputs (quotes, HTML tags) - should escape properly
- [ ] Rapid clicking Add button - should not create duplicate forms
- [ ] Form open, navigate away, come back - form state should reset

---

## Rollback Plan

### If Implementation Fails
1. `git checkout frontend/index.html` (undo changes)
2. Restore from backup: `cp backups/20251031_095426_ps101_v2_implementation/frontend/index.html frontend/`
3. Notify Damian of issue

### Backup Location
- **Pre-fix backup:** `backups/20251031_095426_ps101_v2_implementation/frontend/index.html`
- **Git commit before:** Check `git log -1` before making changes

### Recovery Time
- **Rollback:** <1 minute (git checkout)
- **Diagnose:** 10-30 minutes (check console errors, review code)
- **Fix and retry:** 30-60 minutes (depends on issue)

---

## Context Refresh Protocol

**If task exceeds 30 minutes:**

Agent must pause and output:
```
Context refresh:
- Current task: PS101-FIX-001 - Replace browser prompts with inline forms
- Progress: [HTML added / Event listeners updated / Testing in progress]
- Next action: [What comes next]
- Time elapsed: [X minutes]
- Re-read: ARCHITECTURAL_DECISIONS.md Decision #003, CURSOR_FIXES_REQUIRED.md lines 15-202
```

Damian: Verify still on track, approve continuation.

---

## Communication Protocol

### Status Updates
Agent provides update every **30 minutes**:
- Completed: [What's done]
- In progress: [Current work]
- Blockers: [None / Issue description]
- Time remaining: [Estimate]

### When to Ask for Help
Stop and ask if:
- Unsure how to style forms to match Peripheral Calm
- Can't figure out how to show inline validation errors
- Event listeners not firing correctly
- Console errors that are unclear
- Taking longer than 2 hours

### When to Escalate
Stop immediately if:
- Breaking existing functionality (obstacles/actions not saving)
- Cannot undo changes (git issues)
- Security concern (code injection risk)
- Data structure must change (would require full refactor)

---

## Post-Task Documentation

### Agent Completes
- [x] Decision #003 already documents inline forms approach
- [x] No new decisions needed
- [x] Add inline comments to complex form show/hide logic ✅ (added to lines 3093-3318)
- [x] Note follow-up task: PS101-FIX-002 (validation timing) ✅ (documented in PROJECT_PLAN_ADJUSTMENTS.md)
- [x] Established inline validation protocol ✅ (created `docs/PS101_INLINE_VALIDATION_PROTOCOL.md`)

### Damian Completes
- [ ] Update PROJECT_PLAN_ADJUSTMENTS.md: Mark Issue #1 as complete
- [ ] Update PS101_FIX_PROMPTS_TASK_BRIEF.md with actual time taken
- [ ] If lessons learned: Update AGENT_TASK_TEMPLATE.md

---

## Additional Notes

**Code Snippets Reference:**
Full implementation code provided in `docs/CURSOR_FIXES_REQUIRED.md` lines 67-202. Agent can use as starting point but must adapt to fit codebase context.

**Styling Reference:**
Existing experiment components (lines 179-208) show the CSS patterns to follow. Use same spacing, colors, transitions.

**Validation Pattern:**
Current validation uses `alert()` in some places - this task establishes the pattern of inline validation that should be used throughout.

---

**END OF TASK BRIEF**

**Status:** Ready for agent assignment
**Next Step:** Damian assigns to Cursor, Cursor starts at Checkpoint 1
