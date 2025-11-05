# For Codex Review - PS101 Mosaic Deployment Kit

**Date:** 2025-11-04  
**Status:** Ready for Codex review before commit

## 📦 What's Ready for Review

### New Deployment Scripts (Root `scripts/` Directory)

1. **`scripts/apply_trial_patch.sh`**
   - Injects `trial_mode_snippet.html` into both `frontend/index.html` and `mosaic_ui/index.html`
   - Creates `.bak` backups before modification
   - Idempotent (checks for `ps101_trial_started_at` before applying)
   - Uses correct paths relative to repo root

2. **`scripts/deploy_now_zsh.sh`**
   - One-step commit + push + deploy workflow
   - Stages: guardrails doc, verify script, both HTML files, `netlify.toml`
   - Commits with standard message
   - Pushes to `origin main`
   - Deploys to Netlify production with `--dir mosaic_ui`

3. **`scripts/dns_cache_reset_mac.sh`**
   - Flushes macOS DNS cache
   - Includes user instructions for Chrome cache clearing

4. **`scripts/roll_back_to_prev.sh`**
   - Safe rollback with confirmation prompt
   - Creates backup tag before rollback
   - Resets to previous commit
   - Force pushes and redeploys

5. **`scripts/verify_mosaic_ui.sh`** (already existed, verified present)

### New Documentation

- `Mosaic/PS101_Continuity_Kit/mosaic_deploy_cutover_checklist.md` - Step-by-step cutover guide
- `Mosaic/PS101_Continuity_Kit/trial_mode_snippet.html` - Trial mode bootstrap script
- `docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md` - Deployment guardrails
- `NOTE_DEPLOYMENT_KIT_READY_2025-11-04.md` - Summary for team

### Files Ready to Commit

All scripts are executable and have correct paths. Current git status shows:
- New scripts in `scripts/`
- New documentation in `Mosaic/PS101_Continuity_Kit/`
- Summary notes

## 🔍 Review Checklist for Codex

- [ ] Verify script paths are correct (all use repo root as base)
- [ ] Confirm `apply_trial_patch.sh` correctly references `trial_mode_snippet.html`
- [ ] Verify `deploy_now_zsh.sh` includes all necessary files
- [ ] Check that `roll_back_to_prev.sh` has adequate safety measures
- [ ] Validate that scripts follow project conventions
- [ ] Confirm all scripts are executable (`chmod +x` applied)
- [ ] Review documentation for completeness and accuracy

## 📝 Notes

- Scripts were copied from `Mosaic/PS101_Continuity_Kit/scripts/` to root `scripts/` with path corrections
- The `apply_trial_patch.sh` script had a path issue that was fixed (now uses full path to snippet)
- All scripts tested for syntax correctness (zsh/bash compatible)

---

**Awaiting Codex review before committing and deploying.**


