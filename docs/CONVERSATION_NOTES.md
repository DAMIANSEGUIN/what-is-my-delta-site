# Conversation Notes - WIMD Railway Deployment

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

## Verifications (2025-09-29)
- `curl https://whatismydelta.com/health` → Netlify HTML 404 (no rewrite)
- `curl https://whatismydelta.com/config` → Netlify HTML 404
- `curl https://whatismydelta.com/prompts/active` → Netlify HTML 404
- `curl https://www.whatismydelta.com/health` → Netlify HTML 404
- `curl https://what-is-my-delta-site-production.up.railway.app/health` → `{"ok": true}`

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
-2025-09-29 - Railway origin healthy (`{"ok": true}`); Netlify domain still returns 404 for API routes pending rewrite.
- `curl https://whatismydelta.com/health` → Netlify HTML 404
- `curl https://what-is-my-delta-site-production.up.railway.app/health` → `{"ok": true}`
