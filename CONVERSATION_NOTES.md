# Conversation Notes - WIMD Railway Deployment

## 2025-10-01 Updates
- CODEX added fallback logic in `api/prompts_loader.py` so `/prompts/active` resolves even if `data/prompts_registry.json` is missing from deploy builds.
- Documented canonical layout in `PROJECT_STRUCTURE.md` and codified multi-agent workflow in `PROTOCOL_ENFORCEMENT_PLAN.md`.
- Outstanding: surface original resource audit into accessible workspace; decide whether to track `data/prompts_registry.json` in git or rely on fallback regeneration.

## 2025-10-01 Session Start (Claude in Cursor)
- **Focus**: Validate current deployment status, test prompts loading, and address any immediate issues
- **Status**: Session start checklist completed (Gate A passed)
- **Registry**: `data/prompts_registry.json` exists locally (390 bytes, Sep 26)
- **Next**: Test `/prompts/active` endpoint and verify deployment health

- ✅ **Domain DNS updated** - Apex + www now point to Netlify
- ⚠️ **Custom domain health** - `/health` still returns Netlify 404 page; needs rewrite to backend
- ⚠️ **WWW health regression** - `/health` returns 404 (serving frontend only)
- ✅ **SSL certificate** - Railway automatically issued SSL
- ✅ **Prompts loaded** - CSV ingested and working
- ✅ **API endpoints** - All working (/health, /config, /prompts/active)
- ✅ **DNS proof saved** - User provided Netlify screenshot showing CNAME record
- ✅ **Netlify deploy linked** - Local repo linked to resonant-crostata-90b706
- ✅ **Frontend deployed** - `scripts/deploy_frontend_netlify.sh` pushed Mosaic UI prod build
- ✅ **UI config fallback updated** - `mosaic_ui/index.html` now targets Railway host directly
- ✅ **Railway origin health** - `/health` returns `{"ok": true}` (verified 2025-09-29)

## Current Status
- **API URL:** https://what-is-my-delta-site-production.up.railway.app (direct origin; healthy)
- **Frontend URL:** https://resonant-crostata-90b706.netlify.app (Netlify production)
- **Railway URL:** https://what-is-my-delta-site-production.up.railway.app
- **Domain Provider:** Netlify (DNS updated; API routes not proxied yet)
- **SSL:** Working (Railway automatic)
- **Prompts:** Loaded and active

## Verifications (2025-09-30 - FIXED)
- ✅ `curl https://whatismydelta.com/health` → `{"ok":true,"timestamp":"..."}`
- ✅ `curl https://whatismydelta.com/config` → Working
- ✅ `curl https://whatismydelta.com/prompts/active` → Working
- ✅ Domain routing: WORKING - Netlify proxying to Railway backend
- ✅ Solution: Connected Netlify site to GitHub repository

## User Instructions
- **Track everything** user tells me
- **Update checklist** when steps complete
- **Annotate conversation** with completed items
- **Don't forget** what user has already done

## Next Steps
- ⚠️ Add Netlify rewrite/proxy so domain API routes hit Railway backend
- ⚠️ Re-run smoke tests (`scripts/verify_deploy.sh`) once domain routes resolve

## Frontend Deployment (2025-09-25)
- ✅ **Netlify CLI reinstalled** under Node 20
- ✅ **Bootstrap package added** to resolve missing dependencies
- ✅ **Frontend deployed** via `scripts/deploy_frontend_netlify.sh`
- ✅ **Mosaic UI live** at https://resonant-crostata-90b706.netlify.app
- ⚠️ **Smoke tests pending** - Domain routes still 404 until rewrite in place

## Last Updated
-2025-09-30 - CORS issue escalated to Claude Code
- ✅ **Local CORS working**: HTTP 200 with `access-control-allow-origin` header
- ❌ **Railway CORS failing**: HTTP 400, missing `access-control-allow-origin` header
- ✅ **Explicit OPTIONS handlers added**: All POST endpoints have OPTIONS handlers
- ✅ **Code deployed**: Latest commit `c8a956f` with Railway edge compatibility fix
- ⚠️ **Railway edge interference**: Edge servers intercepting OPTIONS requests before reaching FastAPI
- 🔄 **Escalated to Claude Code**: Railway infrastructure investigation needed

## Current Blocker
- **Issue**: Railway edge servers (`railway-edge`) intercepting OPTIONS preflight requests
- **Evidence**: Local works, Railway returns HTTP 400 regardless of explicit OPTIONS handlers
- **Next**: Claude Code to investigate Railway edge server configuration and alternatives
