# Command Center Backup & Release Control Plan  
**Date:** 2025-11-14  
**Owner:** Codex (release manager)

This plan formalizes how we capture, verify, and distribute production builds so the Mosaic team can recover instantly from regressions.

---

## 1. Golden Build Strategy
- Every certified production build receives a git tag `prod-YYYY-MM-DD` (current: `prod-2025-11-12`).
- Maintain a long-lived `prod-current` branch that tracks the latest tagged release for quick diffing.
- Live BUILD_ID footer must match the tagged commit (`mosaic_ui/index.html` comment `<!-- BUILD_ID:... -->`).

## 2. Release Artefacts
- For each deploy, create a Markdown log in `deploy_logs/` capturing:
  - Deploy timestamp (UTC), initiator, commit SHA, tag, BUILD_ID.
  - Gate output reference, verification results, links to evidence (screenshots, unique Netlify URL).
  - Rollback target (previous prod tag).
- Archive the exact deploy bundle as `/backups/prod-YYYY-MM-DD.zip`.
- Keep a rolling index (future work) summarizing release logs for fast lookup.

## 3. Session Protocol Updates
Agents must:
1. Read the latest entry in `deploy_logs/` at session start and a note the active prod tag in their kickoff message.
2. Confirm a current site backup exists before modifying code. If absent, run `scripts/archive_current_site.sh` (to be implemented) to produce `/backups/site-backup_<timestamp>.zip`, then log the filename.
3. Record backup + release status in `.verification_audit.log` via the deployment gate.

## 4. Deploy Gate & Verification
- `./scripts/run_deploy_gate.sh` executes automated checks (pre-push verification) and prompts for manual confirmations. Pass/fail entries append to `.verification_audit.log`.
- `./scripts/deploy_now_zsh.sh`:
  - Enforces the gate before pushing.
  - Calls the Netlify wrapper with BUILD_ID stamping.
  - Runs `./scripts/verify_live_deployment.sh` post-deploy and fails on mismatch.
- Manual confirmations require visual evidence (browser walkthrough for auth/chat/PS101).

## 5. Daily Backups
- Schedule (manual until automated): once per day, create a full-site snapshot `backups/site-backup_<timestamp>.zip` containing:
  - `mosaic_ui/`, `frontend/`, API/backend sources.
  - Deployment scripts/configs, docs, package manifests.
  - Any critical environment templates.
- Mirror the backup bundle to external storage (e.g., Google Drive) once drive-sync automation is ready.

## 6. Follow-up Tasks
- [ ] Implement `scripts/archive_current_site.sh` to automate the daily backup step.
- [ ] Extend `.verification_audit.log` logging with structured JSON lines for easier parsing.
- [ ] Add a Drive mirroring workflow (cron or CI) to copy `/backups/*.zip` to offsite storage.
- [ ] Build a `deploy_logs/index.json` summarizing each release entry for quick querying.

---

**Current Baseline (2025-11-14):**
- Active production tag: `prod-2025-11-12` @ commit `132c85012b230e2924363e4877c4aa2014191834`.
- Release log: `deploy_logs/2025-11-14_prod-2025-11-12.md`.
- Artefacts: `backups/prod-2025-11-12.zip`, `backups/site-backup_20251114_195930Z.zip`.

Agents must follow this plan until superseded by the designated release manager. Deviations require written approval and an updated release log entry.
