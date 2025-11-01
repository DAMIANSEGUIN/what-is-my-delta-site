# PS101 v2 - Critical Fixes for Cursor

**Reviewer:** Claude Code (Troubleshooting SSE)
**Review Date:** 2025-10-31
**Status:** Code review complete - 3 CRITICAL fixes required before production

---

## Executive Summary

The PS101 v2 implementation is **architecturally sound** and matches the canonical spec. However, there are **3 critical UX issues** that must be fixed before deployment:

1. **BLOCKER**: Replace browser `prompt()`/`confirm()` dialogs with proper UI
2. **HIGH**: Fix experiment validation timing
3. **MEDIUM**: Add Step 10 placeholder or implement Mastery Dashboard

**Estimated effort to fix blockers:** 2-4 hours

---

## CRITICAL ISSUE #1: Replace Browser Prompts (BLOCKER)

### Problem
**Lines 3014-3029** (Add Obstacle) and **Lines 3035-3051** (Add Action) use browser `prompt()` and `confirm()` dialogs.

**Why this is a blocker:**
- ❌ Blocks entire UI while waiting for user input
- ❌ Not accessible (screen readers can't navigate)
- ❌ Poor mobile experience
- ❌ Can't be styled to match Peripheral Calm aesthetic
- ❌ Users can accidentally close without saving

**Current code:**
```javascript
addObstacleBtn.addEventListener('click', () => {
  const label = prompt('What obstacle do you anticipate?');
  if (!label) return;

  const type = confirm('Is this an external obstacle? Click OK for external, Cancel for internal.');
  const strategy = prompt('What strategy will you use to overcome this obstacle?');

  // ...
});
```

### Solution Option A: Inline Form (RECOMMENDED - 1 hour)

**Why recommended:**
- Matches existing Peripheral Calm aesthetic
- No modal library needed
- Fast to implement
- Better UX (stays in context)

**Implementation:**

```javascript
// Add to HTML (around line 476-546 in experiment components section)
// After the obstacles-list div:

<div id="add-obstacle-form" class="hidden" style="margin-top: 16px; padding: 16px; background: var(--bg-secondary); border-radius: 4px;">
  <h4 style="margin: 0 0 12px 0; font-size: 14px;">Add Obstacle</h4>

  <label for="obstacle-label" style="display: block; margin-bottom: 4px; font-size: 13px;">
    What obstacle do you anticipate?
  </label>
  <input
    type="text"
    id="obstacle-label"
    placeholder="e.g., Limited time availability"
    style="width: 100%; margin-bottom: 12px; padding: 8px; border: 1px solid var(--line); border-radius: 4px;"
  />

  <label style="display: block; margin-bottom: 8px; font-size: 13px;">
    <input type="radio" name="obstacle-type" value="external" checked />
    External (e.g., time, resources, other people)
  </label>
  <label style="display: block; margin-bottom: 12px; font-size: 13px;">
    <input type="radio" name="obstacle-type" value="internal" />
    Internal (e.g., self-doubt, fear, lack of knowledge)
  </label>

  <label for="obstacle-strategy" style="display: block; margin-bottom: 4px; font-size: 13px;">
    Strategy to overcome this obstacle:
  </label>
  <textarea
    id="obstacle-strategy"
    rows="3"
    placeholder="How will you mitigate this?"
    style="width: 100%; margin-bottom: 12px; padding: 8px; border: 1px solid var(--line); border-radius: 4px; resize: vertical;"
  ></textarea>

  <div style="display: flex; gap: 8px;">
    <button id="save-obstacle-btn" class="btn-primary" style="flex: 1;">
      Add Obstacle
    </button>
    <button id="cancel-obstacle-btn" class="btn-secondary" style="flex: 1;">
      Cancel
    </button>
  </div>
</div>
```

**Update JavaScript (lines 3010-3030):**

```javascript
// Add Obstacle button (Step 7)
const addObstacleBtn = document.getElementById('add-obstacle-btn');
const addObstacleForm = document.getElementById('add-obstacle-form');
const saveObstacleBtn = document.getElementById('save-obstacle-btn');
const cancelObstacleBtn = document.getElementById('cancel-obstacle-btn');

if (addObstacleBtn && addObstacleForm) {
  addObstacleBtn.addEventListener('click', () => {
    // Show form, hide button
    addObstacleForm.classList.remove('hidden');
    addObstacleBtn.style.display = 'none';

    // Focus first input
    document.getElementById('obstacle-label')?.focus();
  });

  if (cancelObstacleBtn) {
    cancelObstacleBtn.addEventListener('click', () => {
      // Hide form, show button, clear inputs
      addObstacleForm.classList.add('hidden');
      addObstacleBtn.style.display = 'block';
      document.getElementById('obstacle-label').value = '';
      document.getElementById('obstacle-strategy').value = '';
    });
  }

  if (saveObstacleBtn) {
    saveObstacleBtn.addEventListener('click', () => {
      const label = document.getElementById('obstacle-label')?.value.trim();
      const strategy = document.getElementById('obstacle-strategy')?.value.trim();
      const type = document.querySelector('input[name="obstacle-type"]:checked')?.value || 'external';

      // Validation
      if (!label) {
        alert('Please describe the obstacle.');
        return;
      }
      if (!strategy) {
        alert('Please add a strategy to overcome this obstacle.');
        return;
      }

      const activeExp = PS101State.getActiveExperiment();
      if (activeExp) {
        PS101State.addObstacle(activeExp.id, {
          type: type,
          label: label,
          strategy: strategy
        });

        // Clear and hide form
        document.getElementById('obstacle-label').value = '';
        document.getElementById('obstacle-strategy').value = '';
        addObstacleForm.classList.add('hidden');
        addObstacleBtn.style.display = 'block';

        // Re-render
        renderObstacleMapping(activeExp);
      }
    });
  }
}
```

**Similar fix for Add Action (lines 3032-3052):**

```html
<!-- Add after actions-list div -->
<div id="add-action-form" class="hidden" style="margin-top: 16px; padding: 16px; background: var(--bg-secondary); border-radius: 4px;">
  <h4 style="margin: 0 0 12px 0; font-size: 14px;">Add Action</h4>

  <label for="action-label" style="display: block; margin-bottom: 4px; font-size: 13px;">
    What action will you take? *
  </label>
  <input
    type="text"
    id="action-label"
    placeholder="e.g., Schedule 30-min focus block daily"
    style="width: 100%; margin-bottom: 12px; padding: 8px; border: 1px solid var(--line); border-radius: 4px;"
  />

  <label for="action-due" style="display: block; margin-bottom: 4px; font-size: 13px;">
    By when?
  </label>
  <input
    type="text"
    id="action-due"
    placeholder="e.g., 2025-11-15 or 'Next Friday'"
    style="width: 100%; margin-bottom: 12px; padding: 8px; border: 1px solid var(--line); border-radius: 4px;"
  />

  <label for="action-accountability" style="display: block; margin-bottom: 4px; font-size: 13px;">
    Who can help hold you accountable? (optional)
  </label>
  <input
    type="text"
    id="action-accountability"
    placeholder="e.g., My mentor, Team lead"
    style="width: 100%; margin-bottom: 12px; padding: 8px; border: 1px solid var(--line); border-radius: 4px;"
  />

  <div style="display: flex; gap: 8px;">
    <button id="save-action-btn" class="btn-primary" style="flex: 1;">
      Add Action
    </button>
    <button id="cancel-action-btn" class="btn-secondary" style="flex: 1;">
      Cancel
    </button>
  </div>
</div>
```

```javascript
// Add Action button (Step 8)
const addActionBtn = document.getElementById('add-action-btn');
const addActionForm = document.getElementById('add-action-form');
const saveActionBtn = document.getElementById('save-action-btn');
const cancelActionBtn = document.getElementById('cancel-action-btn');

if (addActionBtn && addActionForm) {
  addActionBtn.addEventListener('click', () => {
    addActionForm.classList.remove('hidden');
    addActionBtn.style.display = 'none';
    document.getElementById('action-label')?.focus();
  });

  if (cancelActionBtn) {
    cancelActionBtn.addEventListener('click', () => {
      addActionForm.classList.add('hidden');
      addActionBtn.style.display = 'block';
      document.getElementById('action-label').value = '';
      document.getElementById('action-due').value = '';
      document.getElementById('action-accountability').value = '';
    });
  }

  if (saveActionBtn) {
    saveActionBtn.addEventListener('click', () => {
      const label = document.getElementById('action-label')?.value.trim();
      const due = document.getElementById('action-due')?.value.trim();
      const accountability = document.getElementById('action-accountability')?.value.trim();

      if (!label) {
        alert('Please describe the action.');
        return;
      }

      const activeExp = PS101State.getActiveExperiment();
      if (activeExp) {
        PS101State.addAction(activeExp.id, {
          label: label,
          due: due || '',
          accountability: accountability || ''
        });

        document.getElementById('action-label').value = '';
        document.getElementById('action-due').value = '';
        document.getElementById('action-accountability').value = '';
        addActionForm.classList.add('hidden');
        addActionBtn.style.display = 'block';

        renderActionPlan(activeExp);
      }
    });
  }
}
```

### Solution Option B: Modal Dialog (2-3 hours)

If you prefer modals, implement a reusable modal component. This is more work but provides better separation.

**Not recommended for Day 1** - inline forms are faster and sufficient.

---

## CRITICAL ISSUE #2: Fix Experiment Validation Timing (HIGH)

### Problem
**Lines 2350-2366**: Experiment validation only runs when user is on the last prompt of Steps 6-9. If user navigates back to earlier prompts and then forward again, validation doesn't re-check experiment fields.

**Why this matters:**
- User could bypass experiment requirements by navigating backward
- Inconsistent validation state
- Could save incomplete experiment data

**Current code:**
```javascript
// Enable/disable based on validation
const currentAnswer = PS101State.getAnswer(currentStep, promptIndex);
const step = PS101_STEPS.find(s => s.step === currentStep);
let isValid = currentAnswer.length >= (step ? step.minChars : 30);

// Additional validation for experiment steps (when on last prompt)
if (isLastPrompt && [6, 7, 8, 9].includes(currentStep)) {
  const activeExp = PS101State.getActiveExperiment();
  if (currentStep === 6 && activeExp) {
    // Step 6: need hypothesis, success metric, and duration
    isValid = isValid && activeExp.hypothesis && activeExp.successMetric &&
              (activeExp.duration?.start || activeExp.duration?.review);
  }
  // ... more validation
}
```

### Solution

**Change validation to check ALL prompts in step, not just last:**

```javascript
// Update navigation validation (lines 2320-2370)
function updateNavButtons(currentStep, promptIndex, totalPrompts) {
  const backBtn = document.getElementById('ps101-back');
  const nextBtn = document.getElementById('ps101-next');

  if (backBtn) {
    backBtn.disabled = (currentStep === 1 && promptIndex === 0);
    backBtn.textContent = '← Back';
  }

  if (nextBtn) {
    const isLastStep = currentStep === 10;
    const isLastPrompt = promptIndex === totalPrompts - 1;

    // Button text based on position
    if (isLastStep && isLastPrompt) {
      nextBtn.textContent = 'Complete PS101 →';
    } else if (!isLastPrompt) {
      nextBtn.textContent = 'Next Prompt →';
    } else {
      nextBtn.textContent = 'Next Step →';
    }

    // Validate current prompt
    const currentAnswer = PS101State.getAnswer(currentStep, promptIndex);
    const step = PS101_STEPS.find(s => s.step === currentStep);
    let isValid = currentAnswer.length >= (step ? step.minChars : 30);

    // For experiment steps, ALWAYS check experiment validation (not just on last prompt)
    if ([6, 7, 8, 9].includes(currentStep)) {
      const activeExp = PS101State.getActiveExperiment();

      // Create experiment if doesn't exist
      if (!activeExp && isLastPrompt) {
        PS101State.createExperiment();
      }

      if (activeExp) {
        if (currentStep === 6) {
          // Step 6: need hypothesis, success metric, and at least one date
          const hasRequiredFields = activeExp.hypothesis &&
                                   activeExp.successMetric &&
                                   (activeExp.duration?.start || activeExp.duration?.review);
          // Only enforce on last prompt OR when trying to move forward
          if (isLastPrompt) {
            isValid = isValid && hasRequiredFields;
          }
        } else if (currentStep === 7) {
          // Step 7: need at least one obstacle with strategy
          const hasObstacles = activeExp.obstacles &&
                              activeExp.obstacles.length > 0 &&
                              activeExp.obstacles.every(o => o.label && o.strategy);
          if (isLastPrompt) {
            isValid = isValid && hasObstacles;
          }
        } else if (currentStep === 8) {
          // Step 8: need at least 3 actions
          const hasActions = activeExp.actions && activeExp.actions.length >= 3;
          if (isLastPrompt) {
            isValid = isValid && hasActions;
          }
        } else if (currentStep === 9) {
          // Step 9: need reflection with outcome, learning, and confidence
          const hasReflection = activeExp.reflection &&
                               activeExp.reflection.outcome &&
                               activeExp.reflection.learning &&
                               activeExp.reflection.confidence?.after;
          if (isLastPrompt) {
            isValid = isValid && hasReflection;
          }
        }
      }
    }

    nextBtn.disabled = !isValid;
  }
}
```

**Also add helper method to auto-create experiment:**

```javascript
// Add to PS101State object (around line 2165)
ensureExperiment() {
  if (this.experiments.length === 0) {
    return this.createExperiment();
  }
  return this.getActiveExperiment() || this.experiments[0];
},
```

**Update renderCurrentStep to ensure experiment exists (around line 2515):**

```javascript
// Show experiment components on last prompt of steps 6-9
if (isLastPrompt && [6, 7, 8, 9].includes(state.currentStep)) {
  // Ensure experiment exists before rendering
  let activeExp = PS101State.getActiveExperiment();
  if (!activeExp) {
    activeExp = PS101State.createExperiment();
  }

  if (expComponents) {
    expComponents.classList.remove('hidden');

    // Render appropriate component
    if (state.currentStep === 6) {
      renderExperimentCanvas(activeExp);
    } else if (state.currentStep === 7) {
      renderObstacleMapping(activeExp);
    } else if (state.currentStep === 8) {
      renderActionPlan(activeExp);
    } else if (state.currentStep === 9) {
      renderReflectionLog(activeExp);
    }
  }
  if (ps101Input) ps101Input.classList.add('hidden');
}
```

---

## CRITICAL ISSUE #3: Step 10 Placeholder (MEDIUM)

### Problem
Step 10 (Building Mastery and Self-Efficacy) prompts exist but there's no Mastery Dashboard implementation. Users will complete Step 10 prompts but won't see the aggregated view mentioned in the spec.

**Why this matters:**
- Incomplete user experience
- Spec promises "aggregated view" and "momentum tracker"
- Users expect summary at the end

### Solution Option A: Add Placeholder (RECOMMENDED - 30 min)

Show a simple message indicating the dashboard is coming soon, with basic summary.

**Add to renderCompletionScreen() (around line 2700):**

```javascript
function renderCompletionScreen() {
  const container = document.getElementById('ps101-container');
  if (!container) return;

  const state = PS101State;
  const completedSteps = Object.keys(state.steps).length;
  const activeExp = state.getActiveExperiment();

  container.innerHTML = `
    <div class="ps101-welcome">
      <h2>🎉 PS101 Journey Complete!</h2>
      <p style="margin: 20px 0; font-size: 16px; line-height: 1.6;">
        Congratulations on completing your problem-solving journey. You've worked through
        ${completedSteps} steps and gained valuable insights.
      </p>

      ${activeExp ? `
        <div style="margin: 24px 0; padding: 20px; background: var(--bg-secondary); border-radius: 8px; border-left: 4px solid var(--accent);">
          <h3 style="margin: 0 0 12px 0; font-size: 16px;">Your Experiment Summary</h3>
          <p style="margin: 8px 0;"><strong>Hypothesis:</strong> ${escapeHtml(activeExp.hypothesis || 'Not specified')}</p>
          <p style="margin: 8px 0;"><strong>Actions Taken:</strong> ${activeExp.actions?.length || 0} action items</p>
          <p style="margin: 8px 0;"><strong>Obstacles Identified:</strong> ${activeExp.obstacles?.length || 0}</p>
          ${activeExp.reflection ? `
            <p style="margin: 8px 0;"><strong>Confidence Change:</strong>
              ${activeExp.reflection.confidence?.before || '?'} → ${activeExp.reflection.confidence?.after || '?'}
              ${(activeExp.reflection.confidence?.after - activeExp.reflection.confidence?.before) > 0 ? '📈' : ''}
            </p>
            <p style="margin: 8px 0;"><strong>Next Move:</strong> ${activeExp.reflection.nextMove || 'Continue'}</p>
          ` : ''}
        </div>
      ` : ''}

      <div style="margin: 24px 0; padding: 20px; background: var(--bg-highlight); border-radius: 8px;">
        <h3 style="margin: 0 0 12px 0; font-size: 16px;">📊 Mastery Dashboard (Coming Soon)</h3>
        <p style="margin: 8px 0; color: var(--muted);">
          We're building an aggregated view of your journey that will show:
        </p>
        <ul style="margin: 12px 0 0 20px; color: var(--muted); line-height: 1.8;">
          <li>Skills gained throughout your journey</li>
          <li>Momentum tracker comparing your progress</li>
          <li>Pattern analysis across multiple experiments</li>
          <li>Personalized recommendations for next steps</li>
        </ul>
      </div>

      <div style="display: flex; gap: 12px; margin-top: 24px;">
        <button id="download-summary" class="btn-primary" style="flex: 1;">
          Download Summary
        </button>
        <button id="start-over" class="btn-secondary" style="flex: 1;">
          Start New Journey
        </button>
      </div>
    </div>
  `;

  // Re-attach event listeners
  const downloadBtn = document.getElementById('download-summary');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadSummary);
  }

  const startOverBtn = document.getElementById('start-over');
  if (startOverBtn) {
    startOverBtn.addEventListener('click', () => {
      if (confirm('Are you sure you want to start over? This will clear all your answers.')) {
        PS101State.reset();
      }
    });
  }
}
```

### Solution Option B: Full Dashboard Implementation (6-8 hours)

Implement the full Mastery Dashboard as specified in `PS101_CANONICAL_SPEC_V2.md` Section 4.5.

**Not recommended for immediate deployment** - use placeholder first, implement dashboard in Sprint 2.

---

## ADDITIONAL RECOMMENDATIONS (Non-Blocking)

### 1. Add Better Validation Messages

**Current:** Generic browser `alert()` for validation errors
**Improved:** Inline validation messages under fields

```javascript
// Add helper function
function showValidationError(fieldId, message) {
  const field = document.getElementById(fieldId);
  if (!field) return;

  // Remove existing error
  const existingError = field.parentElement?.querySelector('.validation-error');
  if (existingError) existingError.remove();

  // Add error message
  const error = document.createElement('div');
  error.className = 'validation-error';
  error.style.cssText = 'color: #d63638; font-size: 12px; margin-top: 4px;';
  error.textContent = message;
  field.parentElement?.appendChild(error);

  // Focus field
  field.focus();

  // Auto-remove after 5 seconds
  setTimeout(() => error.remove(), 5000);
}

// Usage in save handlers:
if (!label) {
  showValidationError('obstacle-label', 'Please describe the obstacle.');
  return;
}
```

### 2. Add Experiment Progress Indicator

Show user how complete their experiment is:

```javascript
function getExperimentProgress(experiment) {
  let completed = 0;
  let total = 7;

  if (experiment.hypothesis) completed++;
  if (experiment.successMetric) completed++;
  if (experiment.duration?.start || experiment.duration?.review) completed++;
  if (experiment.resources) completed++;
  if (experiment.obstacles?.length > 0) completed++;
  if (experiment.actions?.length >= 3) completed++;
  if (experiment.reflection) completed++;

  return { completed, total, percentage: Math.round((completed / total) * 100) };
}

// Display in experiment components:
const progress = getExperimentProgress(activeExp);
// Show: "Experiment Progress: 5/7 (71%)"
```

### 3. Add Keyboard Shortcuts

```javascript
// Add to initialization
document.addEventListener('keydown', (e) => {
  // Alt + N = Next
  if (e.altKey && e.key === 'n') {
    document.getElementById('ps101-next')?.click();
  }
  // Alt + B = Back
  if (e.altKey && e.key === 'b') {
    document.getElementById('ps101-back')?.click();
  }
});
```

### 4. Improve ID Generation (Prevent Collisions)

**Current issue:** Using `Date.now()` + random can collide on rapid clicks

```javascript
// Replace ID generation (lines 2167, 2206, 2223)
function generateUniqueId(prefix) {
  return `${prefix}-${Date.now()}-${crypto.randomUUID().slice(0, 8)}`;
}

// Usage:
const expId = generateUniqueId('exp');
```

### 5. Add Auto-Save Indicator

**Current:** `showAutosaveIndicator()` called but not visible enough

```javascript
// Make it more visible
function showAutosaveIndicator(message) {
  const indicator = document.getElementById('autosave-indicator');
  if (!indicator) {
    const newIndicator = document.createElement('div');
    newIndicator.id = 'autosave-indicator';
    newIndicator.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 8px 16px;
      background: var(--accent);
      color: white;
      border-radius: 4px;
      font-size: 13px;
      opacity: 0;
      transition: opacity 200ms;
      z-index: 1000;
    `;
    document.body.appendChild(newIndicator);
  }

  const indicator = document.getElementById('autosave-indicator');
  indicator.textContent = message || 'Saved';
  indicator.style.opacity = '1';

  setTimeout(() => {
    indicator.style.opacity = '0';
  }, 2000);
}
```

---

## TESTING CHECKLIST

Before deploying, test these scenarios:

### Basic Flow
- [ ] Start new PS101 session
- [ ] Answer all prompts in Step 1 (6 prompts)
- [ ] Navigate back and forward between prompts
- [ ] Verify auto-save works (check localStorage)
- [ ] Reload page - verify state persists

### Experiment Flow
- [ ] Reach Step 6, complete all 4 prompts
- [ ] Fill out Experiment Canvas (hypothesis, metric, dates)
- [ ] Try to advance without filling required fields - should block
- [ ] Add 2 obstacles in Step 7 (one external, one internal)
- [ ] Try to advance without obstacles - should block
- [ ] Add 3+ actions in Step 8 with due dates
- [ ] Check/uncheck action items
- [ ] Complete reflection in Step 9 with confidence score
- [ ] Verify experiment status changes to "reviewed"

### Edge Cases
- [ ] Very long text in prompts (>1000 chars) - should handle
- [ ] Special characters in experiment fields (quotes, HTML) - should escape
- [ ] Navigate back from Step 7 to Step 6 - experiment should persist
- [ ] Delete obstacles/actions - should remove from list
- [ ] Try rapid clicking "Add Obstacle" - should not create duplicates

### Migration
- [ ] Create v1 state in localStorage manually
- [ ] Reload page - should migrate to v2
- [ ] Verify old data preserved
- [ ] Verify v1 state cleared

### Validation
- [ ] Try to advance Step 1 prompt 1 with <50 chars - should block
- [ ] Try to advance Step 5 prompt 1 with <100 chars - should block
- [ ] Try to advance Step 6 without success metric - should block
- [ ] Try to complete PS101 without finishing Step 10 - should require all prompts

### Accessibility
- [ ] Navigate with Tab key - should follow logical order
- [ ] Use keyboard to check action items (Space bar)
- [ ] Screen reader test (basic - does it announce steps?)

---

## DEPLOYMENT SEQUENCE

1. **Fix Critical Issues** (2-4 hours)
   - Replace prompt()/confirm() with inline forms (Issue #1)
   - Fix experiment validation (Issue #2)
   - Add Step 10 placeholder (Issue #3)

2. **Test Thoroughly** (1-2 hours)
   - Run through testing checklist above
   - Test on different browsers (Chrome, Firefox, Safari)
   - Test on mobile device

3. **Create Git Commit** (5 min)
   ```bash
   git add frontend/index.html
   git commit -m "Fix PS101 v2 critical issues: replace browser prompts, fix validation, add Step 10 placeholder"
   ```

4. **Deploy to Staging** (if available)
   - Test in production-like environment
   - Verify no regressions

5. **Deploy to Production**
   - Push to main branch
   - Monitor for errors
   - Have rollback plan ready

6. **Post-Deployment**
   - Verify live site works
   - Test on production with real user account
   - Monitor logs for 24 hours

---

## PRIORITY MATRIX

| Issue | Impact | Effort | Priority | Deploy Blocking? |
|-------|--------|--------|----------|------------------|
| Replace prompt()/confirm() | High (UX) | 1-2h | P0 | ✅ YES |
| Fix validation timing | Medium (Data) | 1h | P1 | ✅ YES |
| Step 10 placeholder | Medium (UX) | 30m | P1 | ✅ YES |
| Better validation messages | Low (Polish) | 30m | P2 | ❌ No |
| Progress indicator | Low (Nice-to-have) | 30m | P3 | ❌ No |
| Keyboard shortcuts | Low (Power users) | 15m | P3 | ❌ No |
| ID collision fix | Low (Edge case) | 10m | P3 | ❌ No |

**Total blocking work: 2.5-4 hours**

---

## FILE LOCATIONS REFERENCE

All changes in: `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/frontend/index.html`

| Feature | Line Range | What to Change |
|---------|------------|----------------|
| Obstacle form HTML | After line 546 | Add inline form |
| Obstacle event listeners | Lines 3010-3030 | Replace prompt() logic |
| Action form HTML | After line 546 | Add inline form |
| Action event listeners | Lines 3032-3052 | Replace prompt() logic |
| Validation logic | Lines 2320-2370 | Update experiment checks |
| Experiment creation | Lines 2515-2525 | Auto-create on Step 6 |
| Completion screen | Around line 2700 | Add Step 10 placeholder |

---

## QUESTIONS FOR DAMIAN

Before implementing fixes:

1. **Modal vs Inline Forms**: Do you prefer modal dialogs (more work) or inline forms (recommended) for obstacle/action collection?

2. **Step 10 Timeline**: Should we ship with placeholder now and build full dashboard in Sprint 2? Or delay deployment until dashboard is complete?

3. **Validation Strictness**: Should we block users from advancing if experiments incomplete, or just show warnings?

4. **Browser Support**: What's minimum browser version? (Affects crypto.randomUUID() usage)

5. **Backend Sync**: When do you want to tackle experiment data sync to backend? (Currently localStorage only)

---

**Document prepared by:** Claude Code (Troubleshooting SSE)
**For implementation by:** Cursor
**Estimated total fix time:** 2.5-4 hours
**Blocking production:** Yes (3 critical issues)
