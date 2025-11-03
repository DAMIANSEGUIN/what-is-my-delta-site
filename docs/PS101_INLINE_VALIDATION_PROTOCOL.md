# Inline Validation Protocol

**Established:** 2025-10-31 (PS101-FIX-001)
**Purpose:** Standard pattern for form validation throughout the application
**Status:** ✅ Active Protocol

---

## Overview

This protocol defines the standard approach for form validation established during PS101 v2 Issue #1 fix. All new forms and validation should follow this pattern.

---

## Core Principle

**Never use `alert()` or `confirm()` for validation feedback.** Always use inline error messages.

---

## Pattern Requirements

### 1. Error Display
- **Location:** Error messages appear inline below the input field
- **Styling:** Use `.form-error` class (12px, color: #d63638, margin-top: 4px)
- **Structure:** `<span id="field-name-error" class="form-error hidden">Error message</span>`
- **Hidden state:** Use `.hidden` class to show/hide (display: none)

### 2. Validation Timing
- **On submit:** Check all required fields when Save button clicked
- **On input:** Clear error messages when user starts typing (real-time feedback)
- **Focus:** Auto-focus first invalid field when validation fails

### 3. Error Messages
- **Content:** Clear, specific instructions (e.g., "Please describe the obstacle.")
- **Tone:** Helpful, not accusatory
- **Accessibility:** Error messages are part of DOM (screen readers can announce)

### 4. Visual Feedback
- **Invalid state:** Show error message below field
- **Valid state:** Hide error message (no green checkmarks needed per Peripheral Calm aesthetic)
- **No alerts:** Never block UI with modal dialogs

---

## Implementation Example

```html
<!-- HTML Structure -->
<div class="form-group">
  <label for="field-name">Field Label *</label>
  <input
    type="text"
    id="field-name"
    aria-required="true"
    aria-describedby="field-name-error"
  />
  <span id="field-name-error" class="form-error hidden"></span>
</div>
```

```css
/* CSS */
.form-error{font-size:12px;color:#d63638;margin-top:4px;display:block}
.form-error.hidden{display:none}
```

```javascript
// JavaScript Validation
const fieldInput = document.getElementById('field-name');
const fieldError = document.getElementById('field-name-error');

// On save/submit
if (!fieldInput.value.trim()) {
  fieldError.textContent = 'Please provide a value for this field.';
  fieldError.classList.remove('hidden');
  fieldInput.focus();
  return; // Stop submission
} else {
  fieldError.classList.add('hidden');
}

// Real-time error clearing
fieldInput.addEventListener('input', () => {
  if (fieldInput.value.trim()) {
    fieldError.classList.add('hidden');
  }
});
```

---

## Where This Pattern Is Used

### Currently Implemented
- ✅ PS101 Step 7: Obstacle form (lines 3089-3231 in frontend/index.html)
- ✅ PS101 Step 8: Action form (lines 3233-3318 in frontend/index.html)

### Should Be Applied To
- ❌ PS101 Step validation (lines 2875-2902 still use `alert()`)
- ❌ File upload errors (lines 1525-1530 use `alert()`)
- ❌ Save/load errors (lines 1511, 2967 use `alert()`)
- ❌ Feedback submission (lines 1611-1614 use `alert()`)

**Note:** These remaining `alert()` calls should be replaced in future tasks following this protocol.

---

## Rationale

### Why Not `alert()`?
- ❌ Blocks entire UI (bad UX)
- ❌ Not accessible (screen readers struggle)
- ❌ Poor mobile experience
- ❌ Can't be styled (doesn't match Peripheral Calm aesthetic)
- ❌ Users can't see context while error shown

### Why Inline Messages?
- ✅ Non-blocking (user can still see form)
- ✅ Accessible (part of DOM, screen readers announce)
- ✅ Mobile-friendly (doesn't take over screen)
- ✅ Styled to match design system
- ✅ Contextual (appears right where the problem is)
- ✅ Real-time feedback (can clear as user types)

---

## Related Decisions

- **Decision #003:** Inline Forms for Experiment Data Collection (established this pattern)
- **Decision #007:** Peripheral Calm Design Aesthetic (error styling follows this)

---

## Future Enhancements (Not Required Now)

- Success indicators (green checkmarks) - deferred per Peripheral Calm (minimal UI)
- Field-level validation on blur - can add if user feedback requests
- Toast notifications - only for non-form actions (save success, etc.)

---

**Last Updated:** 2025-10-31
**Established By:** PS101-FIX-001 implementation
**Protocol Owner:** Codex (documentation) / Cursor (implementation)





