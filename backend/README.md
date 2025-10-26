# WIMD – Railway Deploy Project

This repo is a **persisted handover** for Codex/Cursor: Protocol 0 (secrets), rolling checklist, minimal FastAPI app, and Railway deployment files.

## Quick Start
1. Set secrets in **Railway → Service or Shared Variables**:
   - `OPENAI_API_KEY`, `CLAUDE_API_KEY`, optional: `PUBLIC_SITE_ORIGIN`, `PUBLIC_API_BASE`, `DATABASE_URL`, `SENTRY_DSN`
2. Deploy via Git push. Railway uses `Procfile` / `railway.json`.
3. Verify:
   ```bash
   ./scripts/verify_deploy.sh https://<your-api-domain>
   ```

## Files
- `Procfile`, `railway.json` – start command & healthcheck
- `api/index.py` – FastAPI app (`/health`, `/config`), strict CORS
- `api/settings.py`, `api/startup_checks.py` – secrets validation & provider ping at startup
- `api/prompts_loader.py` – CSV hashing, registry, activation
- `scripts/predeploy_sanity.sh` – tripwire script
- `scripts/check_prompts.sh` – CSV validator
- `.github/workflows/secret-scan.yml` – CI secret scanning
- `.env.example`, `.gitignore`

See `ROLLING_CHECKLIST.md` for gated steps.
