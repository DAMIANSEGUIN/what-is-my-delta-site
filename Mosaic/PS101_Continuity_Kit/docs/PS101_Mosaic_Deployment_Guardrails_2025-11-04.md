# PS101 / Mosaic — Deployment Guardrails (2025-11-04)

## 1) Source of Truth
- `netlify.toml` at repo root: `base = "mosaic_ui"`, `publish = "mosaic_ui"`.
- Do not rely on UI deploys from `frontend/` unless explicitly testing legacy.
- All production deploys use: `netlify deploy --prod --site <SITE_ID> --dir mosaic_ui`.

## 2) Files to keep committed
- `docs/PS101_Mosaic_Deployment_Guardrails_2025-11-04.md` (this doc)
- `scripts/verify_mosaic_ui.sh`
- `mosaic_ui/index.html`, `frontend/index.html` (both include trial snippet)
- `trial_mode_snippet.html`
- `netlify.toml`

## 3) Build & Deploy
- Production branch: `main`.
- Netlify Site ID: `bb594f69-4d23-4817-b7de-dadb8b4db874`.
- Monorepo / base dir: `mosaic_ui` (set in both `netlify.toml` and Netlify UI if needed).
- No environment variable should override publish dir.

## 4) Anti‑drift tripwires
- Verify that no `netlify.toml` exists under `frontend/`.
- Confirm Netlify UI (Build & Deploy) shows base/publish `mosaic_ui`.
- Verify domain mapping: `whatismydelta.com` points to this exact Site ID.
- Service Worker: if `/service-worker.js` exists, version-bump or remove on each UI cutover.

## 5) Verification must pass
- `scripts/verify_mosaic_ui.sh` returns success.
- View‑source contains the latest `<!-- BUILD_ID:...|SHA:... -->` comment.
- Fresh/incognito visit shows **no login modal**; `?forceLogin=1` toggles modal back on.

## 6) Rollback
- Use `scripts/roll_back_to_prev.sh` to tag current head, reset to prior commit, and redeploy.