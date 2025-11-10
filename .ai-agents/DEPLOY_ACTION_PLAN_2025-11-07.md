# Deployment Action Plan - DOM Timing Fix
**Created:** 2025-11-07 16:01
**Status:** READY TO EXECUTE
**Target:** Deploy commit `8d8d83f` to production

---

## Code Review: ✅ VERIFIED CORRECT

### Lines 1208-1210 (Footer Year):
```javascript
// Safe footer year update with null-guard
const yearEl = $('#y');
if (yearEl) yearEl.textContent = new Date().getFullYear();
```
✅ Null-guard present
✅ No immediate execution (runs inside init flow)
✅ Pattern matches playbook

### Lines 2059-2115 (Phase 2.5 - Chat Initialization):
```javascript
// Phase 2.5: Initialize API check and chat system
console.log('[INIT] Phase 2.5: Initializing API check and chat...');

// API Status Check
checkAPI();
setInterval(() => {
  const apiStatus = $('#apiStatus');
  if (apiStatus && apiStatus.className.includes('error')) {
    checkAPI();
  }
}, 30000);

// Chat System Setup
const chat = $('#chat');
chatInput = $('#chatInput'); // Set module-level variable
chatLog = $('#chatLog'); // Set module-level variable
sendMsg = $('#sendMsg'); // Set module-level variable
const openChatBtn = $('#openChat');
const closeChatBtn = $('#closeChat');

if (openChatBtn && chat && chatInput) {
  openChatBtn.addEventListener('click', e => {
    e.preventDefault();
    chat.style.display = 'block';
    chatInput.focus();
  });
}

if (closeChatBtn && chat) {
  closeChatBtn.addEventListener('click', () => {
    chat.style.display = 'none';
  });
}

// Close chat on Escape key
document.addEventListener('keydown', e => {
  if (chat && e.key === 'Escape' && chat.style.display === 'block') {
    chat.style.display = 'none';
  }
});

// Setup send message handlers
if (sendMsg) {
  sendMsg.addEventListener('click', send);
}

if (chatInput) {
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });
}

console.log('[INIT] Phase 2.5 complete');
```
✅ All DOM access after DOMContentLoaded
✅ Null-guards on every element
✅ Event listeners set up safely
✅ Module-level variables set correctly
✅ Pattern matches playbook

**Code Quality:** PRODUCTION READY

---

## Deployment Options

### Option 1: Use Wrapper Script (RECOMMENDED)

**Command:**
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
./scripts/deploy.sh netlify
```

**Why Recommended:**
- Automated verification built-in
- Follows protocol (SESSION_START_PROTOCOL.md rule #9)
- Runs pre-deployment checks
- Logs to `.verification_audit.log`

**Prerequisites:**
- ✅ Git working tree clean (only untracked .ai-agents files)
- ✅ Code verified correct
- ✅ Netlify CLI authenticated
- ✅ Site linked (resonant-crostata-90b706)

---

### Option 2: Manual Netlify CLI (IF WRAPPER FAILS)

**Step 1: Check Prerequisites**
```bash
# Verify Netlify CLI installed
netlify --version

# Check site link status
netlify status

# If not linked, link now
netlify link --id resonant-crostata-90b706
```

**Step 2: Deploy**
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
netlify deploy --prod --dir mosaic_ui
```

**Step 3: Verify**
```bash
./scripts/verify_live_deployment.sh
```

---

### Option 3: Netlify Dashboard (IF CLI BLOCKED)

**Steps:**
1. Push commits to GitHub origin:
   ```bash
   git push origin main
   ```

2. Go to Netlify Dashboard: https://app.netlify.com/

3. Find site: `resonant-crostata-90b706` (whatismydelta.com)

4. Deploys tab → "Trigger deploy" → "Deploy site"

5. Wait for build to complete (~2-3 minutes)

6. Verify production:
   ```bash
   ./scripts/verify_live_deployment.sh
   ```

---

## Pre-Deployment Checklist

**Run these checks BEFORE deploying:**

```bash
# 1. Verify HEAD is on correct commit
git log --oneline -1
# Expected: 8d8d83f fix: Move all immediate DOM access inside initApp (Stage 1 fix)

# 2. Verify file line count
wc -l mosaic_ui/index.html
# Expected: 4019

# 3. Verify BUILD_ID in file
tail -1 mosaic_ui/index.html
# Should contain: BUILD_ID:8d8d83f (or current HEAD)

# 4. Run critical features check
./scripts/verify_critical_features.sh
# Expected: All checks pass

# 5. Check PS101 hash
./Mosaic/PS101_Continuity_Kit/check_spec_hash.sh
# Expected: 7795ae25
```

---

## Post-Deployment Verification

### Automated Checks:
```bash
# Run live deployment verification
./scripts/verify_live_deployment.sh

# Expected output:
# ✅ Site reachable
# ✅ Line count matches
# ✅ Title correct
# ✅ Authentication UI present
# ✅ PS101 flow present
# ✅ BUILD_ID matches current commit
```

### Browser Verification:

**1. Open DevTools Console:**
```javascript
// Check initApp defined
typeof window.initApp
// Expected: "function"

// Check Phase 2.5 logs appear
// Look for in console:
// [INIT] Phase 2.5: Initializing API check and chat...
// [INIT] Phase 2.5 complete
```

**2. Test Chat Functionality:**
- Click chat button (should open)
- Type message and press Enter
- Check Network tab for `/wimd` request
- Verify response received

**3. Test Login/Auth:**
- Look for login/sign up button or modal trigger
- Verify auth modal can open

**4. Check Console for Errors:**
- Should see NO TypeError messages
- Should see NO "Cannot set properties of null" errors
- Should see clean initialization logs

---

## Expected Changes After Deployment

### Production Will Change From:
```
BUILD_ID: 6d8f2ed
Commit: 6d8f2ed (docs update)
Status: Partial fix, chat broken
```

### Production Will Change To:
```
BUILD_ID: 8d8d83f (or regenerated)
Commit: 8d8d83f (complete DOM timing fix)
Status: Full fix, chat functional
```

### User-Visible Changes:
- ✅ Chat window opens AND functional (not just opens)
- ✅ Chat sends messages to API
- ✅ Login/auth modal shows when needed
- ✅ No console errors
- ✅ All interactive elements work

---

## Rollback Plan (IF DEPLOYMENT FAILS)

### If Production Breaks:

**Option 1: Rollback via Netlify Dashboard**
1. Go to Netlify Deploys tab
2. Find last working deploy (before this one)
3. Click "Publish deploy" to restore it

**Option 2: Rollback via Git**
```bash
# Revert to previous commit
git revert HEAD
git push origin main

# OR reset to previous commit (nuclear option)
git reset --hard 6d8f2ed
git push origin main --force
```

**Option 3: Use Backup Branch**
```bash
# Switch to backup
git checkout backup-before-dom-fix

# Force push to main (CAREFUL!)
git push origin backup-before-dom-fix:main --force
```

---

## Known Previous Deployment Issues

**From `.verification_audit.log`:**

1. **EPERM Error** (Nov 6, 16:57):
   - Netlify CLI couldn't write to `~/Library/Preferences/netlify/config.json`
   - Solution: Use dashboard deploy or fix CLI permissions

2. **Site Not Linked**:
   - CLI needs: `netlify link --id resonant-crostata-90b706`

3. **NETLIFY_SITE_ID Env Var Blocking**:
   - If set, unset it: `unset NETLIFY_SITE_ID`
   - Use linked site context instead

---

## Decision Matrix: Which Deploy Method?

**Use Wrapper Script IF:**
- ✅ Netlify CLI is working
- ✅ Want automated verification
- ✅ Want audit trail

**Use Manual CLI IF:**
- ✅ Wrapper script fails
- ✅ Need fine control
- ✅ Debugging deploy issues

**Use Dashboard IF:**
- ❌ CLI is completely broken (EPERM, auth issues)
- ✅ Want visual confirmation
- ✅ Need to see build logs in real-time

---

## Execute Deployment

**User can now run:**

### Quick Deploy (Recommended):
```bash
./scripts/deploy.sh netlify
```

### Or Manual:
```bash
netlify deploy --prod --dir mosaic_ui
```

### Or Push + Auto-Deploy:
```bash
git push origin main
# Then trigger deploy in Netlify Dashboard if not auto-deployed
```

---

## Post-Deployment Actions

**After successful deploy:**

1. Update `.verification_audit.log`:
   ```bash
   echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] DOM_TIMING_FIX_DEPLOYED | Commit=8d8d83f | Deploy=SUCCESS | User_Issue=RESOLVED" >> .verification_audit.log
   ```

2. Update Stage 3 verification document:
   ```bash
   # Document resolution in .ai-agents/STAGE3_VERIFICATION_2025-11-05.md
   ```

3. Verify user issue resolved:
   - Ask user to test chat functionality
   - Ask user to confirm login shows
   - Ask user to check console for errors

4. Create handoff if session ending:
   ```bash
   ./scripts/create_handoff_manifest.sh > .ai-agents/handoff_$(date +%Y%m%d_%H%M%S).json
   ```

---

**Status:** READY TO DEPLOY
**Risk Level:** LOW (code verified, backup exists)
**Expected Outcome:** Fixes user-reported issue (chat + login)
