# PS101 / Mosaic — Production Deploy & Verification Kit
Date: 2025-11-04

This kit contains **everything** your team needs to (a) finalize the Mosaic/PS101 UI cutover to `https://whatismydelta.com`, (b) fix the login-modal race with robust trial-mode init, (c) verify DNS/cache, and (d) validate production with deterministic checks. All scripts are **zsh-safe**, no heredocs, no inline comments, and assume macOS (Monterey) with Netlify CLI installed.

## Contents
- `docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md` — Guardrails document.
- `docs/netlify_sanity_check.md` — Where Netlify can still override `mosaic_ui/`.
- `scripts/deploy_now_zsh.sh` — Add/commit/push + Netlify prod deploy for `mosaic_ui/`.
- `scripts/verify_mosaic_ui.sh` — Deterministic verification of build output and modal behavior.
- `scripts/apply_trial_patch.sh` — Injects trial-mode snippet into both HTML files (backs up `.bak`).
- `scripts/dns_cache_reset_mac.sh` — Flush DNS and restart mDNSResponder.
- `scripts/verify_headers.sh` — Quick curl checks for status, cache, and build ID comment.
- `scripts/roll_back_to_prev.sh` — Safe rollback to previous commit + redeploy (tags current head).
- `trial_mode_snippet.html` — Drop-in snippet to paste before `</body>` of the two HTML files.
- `mosaic_deploy_cutover_checklist.md` — One-page cutover checklist.

### How to use (10‑minute flow)
1. Run `scripts/apply_trial_patch.sh` to inject the snippet into both `frontend/index.html` and `mosaic_ui/index.html`.
2. Run `scripts/deploy_now_zsh.sh` to push and deploy to Netlify (prod site).
3. Run `scripts/verify_mosaic_ui.sh` for deterministic validation.
4. If your local browser still shows the login modal, run `scripts/dns_cache_reset_mac.sh` and repeat the verification.
5. Share `docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md` with the team and keep it committed.