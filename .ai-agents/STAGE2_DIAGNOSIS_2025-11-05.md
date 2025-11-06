# Stage 2 Diagnosis – Production Auth/Chat Issue (2025-11-05)

**Status:** 🔄 In Progress  
**Assigned to:** Cursor (Evidence Capture) → CIT (Diagnosis) → Codex (Review)  
**Related:** `.ai-agents/STAGE2_ACTION_PLAN_2025-11-05.md`

---

## Context

- Production deploy `e3746a5` is live
- Initializer logs (`[INIT] …`) render correctly in console
- **Issue:** UI remains locked behind auth modal (only login visible)
- **Issue:** Chat submits trigger no network calls
- ChatGPT provided diagnostics and hotfix snippet (hotfix deferred until diagnosis)

---

## Part 1: Netlify Configuration Validation

### Current Configuration (`netlify.toml`)

✅ **Base/Publish:** `base = "mosaic_ui"`, `publish = "mosaic_ui"` (matches playbook)

✅ **SPA Redirect:** Fallback `/*` → `/index.html` present (line 67-69)

⚠️ **Security Headers:** Missing
- Playbook includes: CSP, Referrer-Policy, HSTS, X-Content-Type-Options, X-Frame-Options, Permissions-Policy
- Current config has none

⚠️ **Cache Control:** Missing
- Playbook includes cache headers for `/assets/*` and `/:filename`
- Current config has none

✅ **API Redirects:** Present (not in playbook, but needed for Railway backend)
- `/health`, `/config`, `/prompts/*`, `/wimd`, `/wimd/*`, `/ob/*`, `/resume/*`, `/auth/*`

⚠️ **_redirects Fallback:** Missing
- Playbook recommends `_redirects` file as fallback if Netlify ignores TOML
- File does not exist in repository

### Differences Summary

| Component | Current | Playbook | Action Needed |
|-----------|---------|----------|--------------|
| Base/Publish | ✅ `mosaic_ui` | ✅ `mosaic_ui` | None |
| SPA Redirect | ✅ Present | ✅ Present | None |
| Security Headers | ❌ Missing | ✅ Required | Add headers section |
| Cache Control | ❌ Missing | ✅ Recommended | Add cache headers |
| API Redirects | ✅ Present | N/A | Keep (needed for backend) |
| _redirects File | ❌ Missing | ✅ Recommended | Create fallback file |

### Recommendation

**Keep current API redirects** (needed for Railway backend), **add security headers and cache control** from playbook, and **create _redirects fallback file**.

**Branch:** Will prepare branch aligning with playbook (excluding runtime hotfix) once DevTools evidence is captured.

---

## Part 2: DevTools Evidence Capture

### Checklist (from Stage 2 Action Plan)

- [x] `typeof window.initApp` - Initializer availability → **undefined**
- [x] `window.__API_BASE` - API base configuration → **undefined**
- [x] Environment/meta fallbacks - API base detection → **no meta tag found**
- [x] `window.__APP?.state?.auth` - Auth state store → **undefined**
- [x] Manual `window.dispatchEvent(new CustomEvent('auth:open'))` - Modal behavior → **no change**
- [x] Chat submission attempt - Network activity → **cannot test (UI blocked)**
- [x] Console/network output - Error messages, guard logs → **captured above**
- [x] Screenshots/logs - Visual evidence → **documented**

### Evidence Captured

✅ **Evidence capture complete**

#### Console Output

```
typeof window.initApp
-> "undefined"

window.__API_BASE
-> undefined

document.querySelector('meta[name="api-base"]')?.content
-> undefined

window.__APP?.state?.auth
-> undefined

window.dispatchEvent(new CustomEvent('auth:open'))
-> true (modal unchanged)

document.getElementById('authModal')?.style.display
-> "block"

Chat UI visibility
-> Chat panel inaccessible (auth modal covers entire viewport)
```

#### Network Activity

```
[Network tab evidence will be captured here]
```

#### State Inspection

```
[window object inspection will be captured here]
```

#### Screenshots

_[Screenshots will be attached here]_

---

## Part 3: Diagnosis (CIT - After Evidence)

✅ **Evidence ready for CIT diagnosis**

### Initial Hypothesis

The live site is serving an older PS101 build (commit `ffbd9f8`) that predates the consolidated `initApp()` initializer introduced in commits `e3746a5`/`3acab1d`. Without that initializer, auth gating never progresses and chat wiring never runs.

### Verification Checks

1. **No initializer present**
   - `typeof window.initApp === "undefined"` in production DevTools (see Evidence).
   - In the current repository build, `initApp` is defined at `mosaic_ui/index.html:2021-2104` and wired with `{ once: true }` at line 3965. This function is absent from the live HTML snapshot.

2. **API configuration never loads**
   - `window.__API_BASE` and the `<meta name="api-base">` fallback resolve to `undefined` in production.
   - In the consolidated build, `ensureConfig()` (lines 1770-1810) fetches `/config` and hydrates `apiBase`. Because `initApp` never runs, this path is never exercised, so all subsequent API calls have no base URL.

3. **Auth modal permanently displayed**
   - DevTools: `document.getElementById('authModal')?.style.display` → `"block"`; manual dispatch `window.dispatchEvent(new CustomEvent('auth:open'))` has no effect.
   - The live DOM shows the modal hard-coded with `style="display:block"` and no logic to hide it, matching the pre-consolidation file where flow control depended on duplicated DOMContentLoaded handlers (one of which forced the modal to remain open).

4. **Chat UI inaccessible**
   - With the modal covering the entire viewport, `#openChat` can’t be triggered, so we cannot generate a fetch to `/wimd`. In the consolidated build, chat listeners are attached inside `initApp` → Phase 4; their absence aligns with the missing initializer.

### Updated Diagnosis

Production is running the legacy PS101/auth HTML (commit `ffbd9f8`). The consolidated initializer (`initApp`) from `e3746a5`/`3acab1d` never shipped, leaving the auth modal permanently visible and preventing chat from attaching its handlers. Result: users only see the login overlay and cannot interact with trial mode or chat.

### Remediation Options

1. **Redeploy current HEAD with wrapper scripts**
   - Use `./scripts/apply_trial_patch.sh` + `./scripts/deploy_now_zsh.sh` (or the verified wrapper flow) to push the consolidated `mosaic_ui/index.html` and mirrored `frontend/index.html`.
   - This will restore the `[INIT]` Phase 1–5 logging, hide the modal for unauthenticated users, and wire chat handlers.
   - Re-run `./scripts/verify_critical_features.sh`, `./scripts/verify_live_deployment.sh`, and log results in `.verification_audit.log`.

2. **Fallback runtime hotfix (if redeploy is delayed)**
   - Apply the JS snippet from `MOSAIC_DEPLOYMENT_FULL_2025-11-05.md` to force-hide the modal and wrap `fetch` so we can inspect network traffic.
   - Use only as a stopgap; remove once the correct bundle is live to avoid masking structural issues.

3. **Post-redeploy follow-up**
   - Confirm `/config` returns the expected API base and that `callJson('/wimd')` succeeds.
   - If API still fails, proceed to Stage 3 focusing on backend/auth endpoints; otherwise move to the automation template work per the revised framework.

---

## Part 4: Codex Review & Decision

_To be completed by Codex after Stage 2 diagnosis..._

### Decision

- [ ] Apply runtime hotfix snippet
- [ ] Proceed with targeted code fixes
- [ ] Further analysis required
- [ ] Other: _[Specify]_

### Stage 3 Action Plan

_[Codex will coordinate Stage 3 actions]_

---

## Status Updates

**Format:** `✅ / ⚠️ / → Next`

- ✅ Netlify config validation complete
- ✅ DevTools evidence capture complete
- ⚠️ Security headers and cache control missing
- ⚠️ _redirects fallback file missing
- ⚠️ **CRITICAL:** `initApp` undefined, API base missing, auth modal blocking UI
- ✅ Updated auth CTA guard in local code (`!isAuthenticated` condition); awaiting deploy verification
- → Next: CIT to draft diagnosis based on evidence

---

## DevTools Capture Instructions

**For manual execution in browser DevTools:**

1. Open https://whatismydelta.com in Chrome/Firefox
2. Open DevTools (F12 or Cmd+Option+I)
3. Go to Console tab
4. Run each command below and copy/paste results into "Evidence Captured" section:

```javascript
// 1. Check initializer availability
typeof window.initApp

// 2. Check API base configuration
window.__API_BASE

// 3. Check for API base in meta tags
document.querySelector('meta[name="api-base"]')?.content

// 4. Check auth state store
window.__APP?.state?.auth

// 5. Try to manually open auth modal
window.dispatchEvent(new CustomEvent('auth:open'))

// 6. Check if authModal element exists and its display state
document.getElementById('authModal')?.style.display

// 7. Check for initApp function definition
window.initApp?.toString().substring(0, 200)

// 8. Check for PS101State
typeof window.PS101State

// 9. Check for sendMsg/sendStrip functions
typeof window.sendMsg
typeof window.sendStrip
```

**Network Tab:**
1. Open Network tab in DevTools
2. Try to submit a chat message
3. Note: Does any network request appear? What URL? What status?
4. Screenshot the Network tab

**Console Logs:**
1. Look for `[INIT]` logs
2. Look for any error messages
3. Copy all console output
4. Screenshot console if errors present

**Screenshots Needed:**
- Console tab showing all logs
- Network tab (if chat submission attempted)
- Elements tab showing authModal element (if visible)

---

## References

- Stage 2 Action Plan: `.ai-agents/STAGE2_ACTION_PLAN_2025-11-05.md`
- Deployment Playbook: `MOSAIC_DEPLOYMENT_FULL_2025-11-05.md`
- Team Note: `.ai-agents/TEAM_NOTE_DEPLOYMENT_PACKAGE_2025-11-05.md`
