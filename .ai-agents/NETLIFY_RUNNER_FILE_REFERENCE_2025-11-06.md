# Netlify Runner Agent – Complete File Reference (2025-11-06)

**Purpose:** This document provides exact file paths and locations for all files needed to complete the Netlify deployment and verification.

---

## 📋 Primary Handoff Document

**File:** `.ai-agents/HANDOFF_NETLIFY_RUNNER_2025-11-06.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/HANDOFF_NETLIFY_RUNNER_2025-11-06.md`  
**Contents:** Step-by-step execution instructions, verification checks, expected outcomes

---

## 🚀 Deployment Scripts

### Main Deployment Wrapper
**File:** `scripts/deploy.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/deploy.sh`  
**Usage:** `./scripts/deploy.sh netlify`  
**What it does:** Orchestrates deployment with pre/post verification, injects BUILD_ID

### Netlify-Specific Deployment Script
**File:** `scripts/deploy_frontend_netlify.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/deploy_frontend_netlify.sh`  
**Usage:** `NETLIFY_SITE_ID=resonant-crostata-90b706 ./scripts/deploy_frontend_netlify.sh`  
**What it does:** Direct Netlify deployment from `mosaic_ui/` directory

### Pre-Deployment Verification
**File:** `scripts/pre_push_verification.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/pre_push_verification.sh`  
**Usage:** `./scripts/pre_push_verification.sh`  
**What it does:** Runs pre-deployment checks (sanity checks, critical features, content verification)

### Pre-Deployment Sanity Checks
**File:** `scripts/predeploy_sanity.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/predeploy_sanity.sh`  
**Usage:** Called by `pre_push_verification.sh`  
**What it does:** Checks Python dependencies, API keys, prompts CSV

### Critical Features Verification
**File:** `scripts/verify_critical_features.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/verify_critical_features.sh`  
**Usage:** Called by `pre_push_verification.sh`  
**What it does:** Verifies auth UI, PS101 flow, experiment components are present in code

---

## ✅ Verification Scripts

### Live Deployment Verification
**File:** `scripts/verify_live_deployment.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/verify_live_deployment.sh`  
**Usage:** `./scripts/verify_live_deployment.sh | tee -a .verification_audit.log`  
**What it does:** Checks live production site (reachability, line count, title, UI presence)  
**Expected output:** Line count should match 3989 after successful deployment

### Deployment Verification (Alternative)
**File:** `scripts/verify_deployment.sh`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/scripts/verify_deployment.sh`  
**Usage:** Called by `deploy.sh` after deployment  
**What it does:** Post-deployment verification wrapper

---

## 📝 Source Files (Frontend)

### Primary Frontend HTML
**File:** `mosaic_ui/index.html`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/mosaic_ui/index.html`  
**Status:** Contains consolidated build with `initApp` function + auth button fix (commit `0c44e11`)  
**Expected line count:** 3989 lines (after BUILD_ID injection)

### Mirror Frontend HTML
**File:** `frontend/index.html`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/frontend/index.html`  
**Status:** Should mirror `mosaic_ui/index.html` (keep in sync)  
**Note:** Deployment uses `mosaic_ui/`, but both files should match

### BUILD_ID Injection Script
**File:** `Mosaic/PS101_Continuity_Kit/inject_build_id.js`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/Mosaic/PS101_Continuity_Kit/inject_build_id.js`  
**Usage:** `node Mosaic/PS101_Continuity_Kit/inject_build_id.js`  
**What it does:** Injects BUILD_ID and SPEC_SHA into HTML footer

### Manifest File (for SPEC_SHA)
**File:** `Mosaic/PS101_Continuity_Kit/manifest.can.json`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/Mosaic/PS101_Continuity_Kit/manifest.can.json`  
**Usage:** Used to calculate SPEC_SHA: `shasum -a 256 Mosaic/PS101_Continuity_Kit/manifest.can.json | cut -d' ' -f1 | cut -c1-8`

---

## ⚙️ Configuration Files

### Netlify Configuration
**File:** `netlify.toml`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/netlify.toml`  
**Contents:** Build settings, redirects, security headers, cache control  
**Key settings:**
- `base = "mosaic_ui"`
- `publish = "mosaic_ui"`
- SPA redirects: `/*` → `/index.html`
- Cache headers: `index.html` = `no-store`, `/assets/*` = long cache

### Netlify Redirects Fallback
**File:** `_redirects`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/_redirects`  
**Contents:** `/*   /index.html   200`  
**Purpose:** Fallback if `netlify.toml` redirects are ignored

### Netlify Site ID Storage
**File:** `.netlify_site_id`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.netlify_site_id`  
**Contents:** Site ID (may be empty, use `NETLIFY_SITE_ID=resonant-crostata-90b706` env var)

---

## 📚 Documentation Files

### Stage 3 Verification (Current Status)
**File:** `.ai-agents/STAGE3_VERIFICATION_2025-11-05.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/STAGE3_VERIFICATION_2025-11-05.md`  
**Contents:** Deployment status, verification checklist, manual verification steps, issues found  
**Status:** Updated with failed deployment attempt (2025-11-06T16:57:58Z)

### Stage 2 Diagnosis
**File:** `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`  
**Contents:** Problem diagnosis, evidence, hypotheses

### Production UI Recovery Playbook
**File:** `Mosaic_Production_UI_Recovery_Playbook_2025-11-06.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/Mosaic_Production_UI_Recovery_Playbook_2025-11-06.md`  
**Contents:** Comprehensive recovery procedures, runtime fixes, troubleshooting

### Deployment Wrapper Recovery Guide
**File:** `Mosaic_Deployment_Wrapper_Recovery_Guide_2025-11-06.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/Mosaic_Deployment_Wrapper_Recovery_Guide_2025-11-06.md`  
**Contents:** Git clean state recovery, Path A/B/C options, troubleshooting

### Team Note (Auth Button Fix)
**File:** `.ai-agents/TEAM_NOTE_STAGE3_MANUAL_CHECKS_2025-11-05.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/TEAM_NOTE_STAGE3_MANUAL_CHECKS_2025-11-05.md`  
**Contents:** Action item for auth button guard fix (completed in code, deployment pending)

---

## 📊 Log Files

### Verification Audit Log
**File:** `.verification_audit.log`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.verification_audit.log`  
**Usage:** Append verification results: `./scripts/verify_live_deployment.sh | tee -a .verification_audit.log`  
**Format:** `[TIMESTAMP] Agent | Command | RESULT=success/failed | Notes=...`  
**Latest entry:** `2025-11-06T16:57:58Z` - Failed deployment attempt (EPERM)

---

## 🔑 Environment Variables Needed

**NETLIFY_SITE_ID:** `resonant-crostata-90b706`  
**Usage:** `NETLIFY_SITE_ID=resonant-crostata-90b706 ./scripts/deploy_frontend_netlify.sh`

**BUILD_ID:** Auto-calculated by `deploy.sh` or manually: `export BUILD_ID=$(git rev-parse HEAD)`

**SPEC_SHA:** Auto-calculated by `deploy.sh` or manually: `export SPEC_SHA=$(shasum -a 256 Mosaic/PS101_Continuity_Kit/manifest.can.json | cut -d' ' -f1 | cut -c1-8)`

---

## 📍 Repository Root

**Absolute Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project`  
**Relative Path:** `.` (when in repo root)

**To navigate to repo:**
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
```

---

## 🎯 Quick Command Reference

### Full Deployment Flow (Recommended)
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
git pull origin main
./scripts/pre_push_verification.sh
export BUILD_ID=$(git rev-parse HEAD)
export SPEC_SHA=$(shasum -a 256 Mosaic/PS101_Continuity_Kit/manifest.can.json | cut -d' ' -f1 | cut -c1-8)
node Mosaic/PS101_Continuity_Kit/inject_build_id.js
NETLIFY_SITE_ID=resonant-crostata-90b706 ./scripts/deploy.sh netlify
```

### Direct Netlify Deploy (Alternative)
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
NETLIFY_SITE_ID=resonant-crostata-90b706 netlify deploy --prod --dir mosaic_ui
```

### Verification After Deploy
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
sleep 60  # Wait for CDN propagation
./scripts/verify_live_deployment.sh | tee -a .verification_audit.log
```

---

## ✅ Post-Deployment Checklist

1. **Deployment succeeds** → Note deploy ID from Netlify output
2. **Wait 60-90 seconds** → CDN propagation
3. **Run automated verification** → `./scripts/verify_live_deployment.sh`
4. **Manual browser checks** → See `.ai-agents/STAGE3_VERIFICATION_2025-11-05.md` section "Manual Browser Verification"
5. **Log results** → Append to `.verification_audit.log`
6. **Update Stage 3 doc** → Update `.ai-agents/STAGE3_VERIFICATION_2025-11-05.md` with results
7. **DO NOT mark as "fixed"** → Until manual verification confirms all checks pass

---

## 🚨 Important Notes

- **Verification Rule:** Never mark something as "working" or "fixed" until manual browser verification confirms it works in production
- **Current Production State:** Serving 3,992-line bundle (old version - login modal missing, chat dead)
- **Expected After Deploy:** 3,989-line bundle (consolidated build with `initApp` + auth button fix)
- **Blocker Resolved:** Terminal Codex had EPERM error - Netlify Runner Agent should have proper permissions

---

**End of File Reference – 2025-11-06**

