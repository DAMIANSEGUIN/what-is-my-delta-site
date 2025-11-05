# ✅ PS101 Mosaic Deployment Kit - Ready for Use

**Date:** 2025-11-04  
**Status:** All scripts installed and ready

## 📦 New Deployment Scripts (Root `scripts/` Directory)

All scripts are now available in the root `scripts/` directory with corrected paths:

1. **`scripts/apply_trial_patch.sh`** - Injects trial-mode bootstrap into both HTML files
   - Creates `.bak` backups automatically
   - Idempotent (skips if already applied)
   - Uses correct paths to `trial_mode_snippet.html`

2. **`scripts/deploy_now_zsh.sh`** - One-step commit + push + deploy
   - Stages required files
   - Commits with standard message
   - Pushes to `origin main`
   - Deploys to Netlify production

3. **`scripts/dns_cache_reset_mac.sh`** - Flushes macOS DNS cache
   - Includes instructions for Chrome cache clearing

4. **`scripts/roll_back_to_prev.sh`** - Safe rollback with confirmation
   - Creates backup tag before rollback
   - Resets to previous commit
   - Force pushes and redeploys

5. **`scripts/verify_mosaic_ui.sh`** - Production verification helper
   - Checks HTTP 200
   - Verifies line count (3875)
   - Confirms auth modal and PS101 state presence
   - Validates BUILD_ID footer

## 📋 Quick Start - 10-Minute Cutover Flow

```bash
# 1. Apply trial patch
./scripts/apply_trial_patch.sh

# 2. Commit + push + deploy
./scripts/deploy_now_zsh.sh

# 3. Verify production
./scripts/verify_mosaic_ui.sh

# 4. If browser still shows legacy UI
./scripts/dns_cache_reset_mac.sh
# Then: Quit Chrome, reopen, Empty Cache and Hard Reload
```

## 📄 Documentation

- **Guardrails:** `docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md`
- **Checklist:** `Mosaic/PS101_Continuity_Kit/mosaic_deploy_cutover_checklist.md`
- **Trial Snippet:** `Mosaic/PS101_Continuity_Kit/trial_mode_snippet.html`

## ✅ What's Fixed

- ✅ Script paths corrected (relative to repo root)
- ✅ Trial patch script uses correct snippet path
- ✅ All scripts made executable
- ✅ Deploy script includes safety checks
- ✅ Rollback script includes confirmation prompt

## 🎯 Expected Outcome

After running the cutover flow:
- Production site serves Mosaic/PS101 UI
- Automatic 5-minute trial mode for unauthenticated users
- No login wall on fresh load
- BUILD_ID/SHA in source matches latest commit
- Netlify locked to `mosaic_ui` directory

---

**Ready for production cutover when you are.**


