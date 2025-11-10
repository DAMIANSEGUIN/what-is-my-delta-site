# DOM Timing Issues - Prevention Protocol & Playbook
**Integrated:** 2025-11-07
**Source:** AI Frontend Safety Playbook (JS + Vite Edition)
**Status:** MANDATORY for all frontend code changes

---

## Quick Reference: AI Frontend Rules

**Paste into every AI prompt for frontend code:**

1. Use `<script type="module" defer>`; do not use `async` for DOM-dependent code.
2. **No top-level DOM queries/mutations.** Provide an `init()` called from DOMContentLoaded.
3. Null-guard all DOM targets.
4. `init()` must be idempotent and safe on re-entry.
5. If using `$`, define it explicitly (jQuery vs querySelector wrapper) and use correct API (`.text` vs `.textContent`).
6. Provide a Playwright smoke test that asserts `init` is defined and `#y` contains a year.
7. Avoid global leaks; export from modules explicitly.
8. Keep functions small and purposeful; comment only where intent is non-obvious.

---

## Problem Pattern: Immediate DOM Access

### ❌ WRONG (Causes Crash):
```javascript
<script>
  // This runs IMMEDIATELY before DOM is ready
  $('#y').textContent = new Date().getFullYear(); // CRASHES!

  const chat = $('#chat'); // CRASHES if element doesn't exist yet!
  const chatLog = $('#chatLog');

  $('#openChat').addEventListener('click', () => { ... }); // CRASHES!
</script>
```

**Result:**
- `TypeError: Cannot set properties of null`
- Script execution stops
- Everything below never runs
- `initApp` never defined
- Nothing initializes
- UI appears broken

---

## Solution Pattern: DOMContentLoaded Wrapper

### ✅ CORRECT (Safe):
```javascript
<script>
  // Declare module-level variables (no DOM access)
  let chatLog = null;
  let chatInput = null;
  let sendMsg = null;

  // All DOM access inside init function
  function init() {
    // Belt and suspenders: check if already initialized
    if (booted) return;
    booted = true;

    // Safe DOM access with null-guards
    const yearEl = document.getElementById('y');
    if (yearEl) yearEl.textContent = String(new Date().getFullYear());

    // Initialize chat elements
    chatLog = document.getElementById('chatLog');
    chatInput = document.getElementById('chatInput');
    sendMsg = document.getElementById('sendMsg');

    // Set up event listeners with null-guards
    if (sendMsg) {
      sendMsg.addEventListener('click', handleSend);
    }

    if (chatInput) {
      chatInput.addEventListener('keydown', e => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSend();
        }
      });
    }
  }

  // Wait for DOM to be ready
  document.addEventListener('DOMContentLoaded', init, { once: true });

  // Expose for tests (optional)
  window.init = init;
</script>
```

---

## ESLint Rule: Prevent Top-Level DOM Access

**Add to `.eslintrc.json`:**

```json
{
  "rules": {
    "no-restricted-syntax": [
      "error",
      {
        "selector": ":matches(Program > ExpressionStatement, Program > VariableDeclaration, Program > FunctionDeclaration) CallExpression[callee.object.name='document'][callee.property.name=/^(getElementById|querySelector|querySelectorAll)$/]",
        "message": "DOM queries must not run at top level. Use DOMContentLoaded or defer."
      }
    ]
  }
}
```

**What this blocks:**
- Top-level `document.getElementById()`
- Top-level `document.querySelector()`
- Top-level `document.querySelectorAll()`

**What this allows:**
- DOM queries inside functions
- DOM queries inside event handlers
- DOM queries inside `init()` or `initApp()`

---

## Diagnostic Checklist: "My UI is Broken"

### Symptoms:
- Chat doesn't work
- Login doesn't show
- Buttons don't respond
- Console shows `initApp is not defined` or `TypeError: Cannot set properties of null`

### Quick Diagnosis:

**1. Check Browser Console:**
```javascript
typeof window.initApp
// Expected: "function"
// If "undefined": initialization never ran
```

**2. Look for Immediate DOM Access:**
Search codebase for:
```bash
# Find top-level DOM queries (outside functions)
grep -n "getElementById\|querySelector" index.html | grep -v "function\|=>"
```

**3. Check for Common Patterns:**
- [ ] `$('#element').textContent = ...` at top level
- [ ] `const el = $('#element');` at top level
- [ ] `addEventListener` calls at top level
- [ ] Any DOM manipulation before `DOMContentLoaded`

**4. Verify Script Loading:**
- [ ] Script has `defer` attribute OR is at end of `<body>`
- [ ] Script is inside IIFE (Immediately Invoked Function Expression)
- [ ] DOMContentLoaded listener exists

---

## Prevention Checklist: Before Every Code Change

### Pre-Flight Check:
```
□ No top-level DOM queries/mutations
□ All DOM access inside init() or event handlers
□ Every element access has null-guard (if (el) { ... })
□ init() is idempotent (safe to call multiple times)
□ DOMContentLoaded listener uses { once: true }
□ Script has defer OR is at end of <body>
□ ESLint passes (no restricted syntax violations)
```

### Pre-Deploy Check:
```
□ Run ESLint: npm run lint
□ Test in browser: typeof window.init === "function"
□ Console shows initialization logs
□ No console errors
□ All interactive elements respond
□ Run smoke test: npm test (if Playwright configured)
```

---

## Common Mistakes & Fixes

### Mistake 1: "I need this to run immediately!"
**Wrong:**
```javascript
$('#y').textContent = new Date().getFullYear(); // Runs immediately
```

**Right:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const yearEl = $('#y');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
}, { once: true });
```

### Mistake 2: "But I added a null check!"
**Still Wrong:**
```javascript
// Still at top level - runs before DOM ready!
const el = $('#y'); // el will ALWAYS be null here
if (el) el.textContent = 'text'; // Never executes
```

**Right:**
```javascript
document.addEventListener('DOMContentLoaded', () => {
  const el = $('#y'); // NOW element exists
  if (el) el.textContent = 'text'; // Executes successfully
}, { once: true });
```

### Mistake 3: "I put it in a function!"
**Still Wrong if function runs immediately:**
```javascript
function setYear() {
  $('#y').textContent = new Date().getFullYear();
}
setYear(); // STILL runs before DOM ready!
```

**Right:**
```javascript
function setYear() {
  const yearEl = $('#y');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
}
document.addEventListener('DOMContentLoaded', setYear, { once: true });
```

### Mistake 4: "DOMContentLoaded is outside IIFE"
**Wrong:**
```javascript
(function() {
  function initApp() { ... }
})(); // IIFE closes here

// Listener is OUTSIDE - initApp is not accessible!
document.addEventListener('DOMContentLoaded', initApp);
```

**Right:**
```javascript
(function() {
  function initApp() { ... }

  // Listener is INSIDE IIFE
  document.addEventListener('DOMContentLoaded', initApp, { once: true });
})();
```

---

## Reference Implementation

### Minimal Safe Boot (from Playbook):

**File: `src/init.js`**
```javascript
let booted = false;

export function init() {
  if (booted) return;
  booted = true;

  const y = document.getElementById('y');
  if (y) y.textContent = String(new Date().getFullYear());
}

// Prefer both guards: defer + DOMContentLoaded (belt and suspenders)
document.addEventListener('DOMContentLoaded', init, { once: true });

// Expose for smoke tests (and manual triggering). Remove if undesired.
window.init = init;
```

**File: `public/index.html`**
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>DOM Timing Safe Boot</title>
    <script type="module" src="/src/init.js" defer></script>
  </head>
  <body>
    <main>
      <h1>Safe Boot Example</h1>
    </main>
    <footer>© <span id="y"></span></footer>
  </body>
</html>
```

---

## Smoke Test Template

**File: `tests/boot.spec.js`** (Playwright)

```javascript
import { test, expect } from '@playwright/test';

test('init is defined and footer year is set', async ({ page }) => {
  await page.goto('http://localhost:3000');

  // Check init function exists
  const initExists = await page.evaluate(() => typeof window.init === 'function');
  expect(initExists).toBe(true);

  // Check footer year is set
  const yearText = await page.textContent('#y');
  expect(yearText).toMatch(/^\d{4}$/);
  expect(parseInt(yearText)).toBeGreaterThanOrEqual(2025);
});
```

---

## Integration into WIMD Project

### Applied to: `mosaic_ui/index.html` & `frontend/index.html`

**Pattern Used:**
1. IIFE wrapper for scope isolation
2. `initApp()` function with phased initialization
3. All DOM access moved into `initApp()` phases
4. DOMContentLoaded listener inside IIFE
5. Null-guards on every element access
6. Module-level variable declarations (no immediate DOM access)

**Phases:**
- Phase 1: API config, session management
- Phase 2: Auth UI setup
- **Phase 2.5: API check + chat system** ← Added for DOM timing fix
- Phase 3: Navigation handlers
- Phase 4: Interactive buttons (explore, find, apply, etc.)
- Phase 5: Trial mode initialization

**Key Addition (Phase 2.5):**
```javascript
// Phase 2.5: Initialize API check and chat system
console.log('[INIT] Phase 2.5: Initializing API check and chat...');

// API Status Check (moved from top-level)
checkAPI();
setInterval(() => {
  const apiStatus = $('#apiStatus');
  if (apiStatus && apiStatus.className.includes('error')) {
    checkAPI();
  }
}, 30000);

// Chat System Setup (moved from top-level)
const chat = $('#chat');
chatInput = $('#chatInput');
chatLog = $('#chatLog');
sendMsg = $('#sendMsg');

if (openChatBtn && chat && chatInput) {
  openChatBtn.addEventListener('click', e => {
    e.preventDefault();
    chat.style.display = 'block';
    chatInput.focus();
  });
}

// ... more chat setup with null-guards ...

console.log('[INIT] Phase 2.5 complete');
```

---

## When to Apply This Protocol

### MANDATORY for:
- Any code that accesses `document.getElementById()`
- Any code that accesses `document.querySelector()` or `querySelectorAll()`
- Any code that sets element properties (`.textContent`, `.value`, `.style`, etc.)
- Any code that adds event listeners to DOM elements
- Any code that manipulates DOM classes, attributes, or content

### NOT REQUIRED for:
- Code inside functions that are only called AFTER DOMContentLoaded
- Code in event handlers (already guaranteed DOM exists)
- Code that only declares variables/functions (no execution)
- Code that only does math/logic (no DOM interaction)

---

## Related Protocols

- **Session Start Protocol:** `.ai-agents/SESSION_START_PROTOCOL.md`
- **Troubleshooting Checklist:** `TROUBLESHOOTING_CHECKLIST.md`
- **Self-Diagnostic Framework:** `SELF_DIAGNOSTIC_FRAMEWORK.md`
- **Deployment Verification:** `scripts/verify_live_deployment.sh`

---

## Update History

- **2025-11-07:** Initial integration from AI Frontend Safety Playbook
- **2025-11-07:** Applied to WIMD project (commits bac92d5, 8d8d83f)
- **2025-11-07:** Added Phase 2.5 pattern for chat initialization

---

**Status:** ACTIVE - Apply to all frontend code changes
**Owner:** Build Team (Claude Code, Cursor, CIT, Codex)
**Review:** Before every deployment
