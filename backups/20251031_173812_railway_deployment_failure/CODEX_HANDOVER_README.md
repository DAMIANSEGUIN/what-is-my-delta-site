# CODEX HANDOVER - Current Project Status

## IMMEDIATE ISSUE (Sep 29)
- **Domain API routes 404**: `https://whatismydelta.com/*` still serves Netlify's 404 page; needs rewrite/proxy to Railway.
- **Claude API key not surfaced**: App still reports missing Claude credentials due to env loading gap.
- **Prod API base**: Use `https://what-is-my-delta-site-production.up.railway.app` directly until Netlify rewrite lands.

## CURRENT PROJECT STATUS
- **Backend (Railway)**: Service `what-is-my-delta-site` healthy; `/health` returns `{"ok": true}`.
- **Frontend (Netlify)**: `resonant-crostata-90b706` live at `https://www.whatismydelta.com`, but API calls hit 404 without rewrite.
- **Custom domains**: Apex + `www` point to Netlify; DNS is correct but routing needs adjustment.
- **Env vars**: `PUBLIC_SITE_ORIGIN=https://www.whatismydelta.com`, `PUBLIC_API_BASE=https://what-is-my-delta-site-production.up.railway.app`, Claude/OpenAI keys present but app cannot read Claude key yet.

## WHAT NEEDS FIXING
1. **Add Netlify rewrite/proxy** so `/health`, `/config`, `/prompts/*`, `/wimd/*`, `/ob/*`, `/resume/*` route to the Railway API.
2. **Investigate env loading** in `api/settings.py` / `api/startup_checks.py` until `CLAUDE_API_KEY` is visible at runtime.
3. **Re-run smoke tests** (`./scripts/verify_deploy.sh`) against the public domain once routing is fixed.

## FILES TO CHECK (Claude)
- `netlify.toml` or Netlify dashboard rules – add proxy for API paths → Railway origin.
- `api/settings.py`, `api/startup_checks.py` – confirm dotenv/environment logic.
- `scripts/verify_deploy.sh` – use after routing fix to confirm `/health`, `/config`, `/prompts/active`.
- `CONVERSATION_NOTES.md`, `ROLLING_CHECKLIST.md` – latest status + outstanding tasks.

## NEXT STEPS FOR CLAUDE_CODE
1. Implement Netlify rewrite and redeploy the frontend.
2. Verify domain `https://whatismydelta.com/health` returns `{"ok": true}`.
3. Troubleshoot environment loading so `CLAUDE_API_KEY` is accessible in app context.
4. Confirm `/config` reflects the correct `apiBase` and active prompt SHA.
5. Update docs/checklist once both routing and env issues are resolved.

## PROJECT DIRECTORY
/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project

## ARCHITECTURE CONSOLIDATION COMPLETED ✅
- **Unified Project Created**: `/Users/damianseguin/projects/mosaic-platform/`
- **All Components Consolidated**: Backend, frontend, docs, and deployment scripts
- **⚠️ CODEX ACCESS ISSUE**: CODEX cannot access `/Users/damianseguin/projects/` due to sandbox limitations
- **SOLUTION**: CODEX should work from this current accessible workspace (`/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/`)
- **All fixes already exist here**: Complete FastAPI code, netlify.toml, fixed requirements.txt

## CRITICAL
- CODEX should deploy from this accessible workspace - all fixed code already exists here
- Architectural consolidation completed but deployment still needed from accessible location
- Keep using the Railway origin for API testing until Netlify rewrite is in place
- Document every change in `CONVERSATION_NOTES.md` and `ROLLING_CHECKLIST.md`














