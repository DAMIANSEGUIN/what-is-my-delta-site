# Netlify Sanity Check — Avoid Frontend/ Regressions

**Check in Netlify UI:**
- Site → Settings → Build & Deploy:
  - Base directory: `mosaic_ui`
  - Publish directory: `mosaic_ui`
  - Production branch: `main`
  - Ignore builds: (empty)
  - Environment: ensure no var like `PUBLISH_DIR=frontend`

**Check in repo:**
- Only one `netlify.toml` (root). None inside `frontend/` or other dirs.
- `netlify.toml` has `base = "mosaic_ui"` and `publish = "mosaic_ui"`.
- CLI deploys always specify `--dir mosaic_ui` for production.