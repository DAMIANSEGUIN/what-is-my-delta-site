# NETLIFY AI AGENT - Troubleshooting Instructions

## Current Issue
Auth proxy routes in netlify.toml are not working. Netlify returns "Page not found" HTML for `/auth/*` endpoints instead of proxying to Railway backend.

## What's Working
✅ Railway backend fully operational at https://what-is-my-delta-site-production.up.railway.app
✅ `/health` proxy works correctly through Netlify
✅ `/config` proxy works correctly through Netlify
✅ `/prompts/*` proxy works correctly through Netlify

## What's NOT Working
❌ `/auth/register` returns Netlify 404 HTML
❌ `/auth/login` returns Netlify 404 HTML
❌ `/auth/me` returns Netlify 404 HTML

## Repository Details
- **Site**: https://whatismydelta.com
- **Netlify Site ID**: resonant-crostata-90b706
- **Git Repo**: https://github.com/DAMIANSEGUIN/wimd-railway-deploy.git
- **Branch**: main
- **Build Directory**: mosaic_ui
- **Publish Directory**: mosaic_ui

## Recent Changes
1. Pushed netlify.toml with auth routes (commit 343f4c8) ~10 minutes ago
2. Auth routes configured with `force = true` to override SPA fallback
3. Routes are positioned BEFORE the catch-all `/*` SPA route

## Your Tasks

### 1. Check Current Deployment Status
```
Go to Netlify dashboard → Site deploys
- What is the status of the latest deploy?
- When was the last successful deploy?
- Is there a deploy in progress?
- Are there any failed deploys?
```

### 2. Verify netlify.toml is Deployed
```
Check if netlify.toml is present in the deployed site:
- Look at deploy details → "Deploy log"
- Search for "netlify.toml" in the build log
- Verify redirect rules were processed
```

### 3. Check Build Configuration
```
Site settings → Build & deploy → Build settings:
- Base directory: mosaic_ui
- Publish directory: mosaic_ui
- Build command: (should be empty or custom)
```

### 4. Verify Redirect Rules
```
Site settings → Build & deploy → Post processing → Redirect rules:
- Are the /auth/* rules visible?
- Are they in the correct order (before /* catch-all)?
- Do they have status 200 and force: true?
```

### 5. Test Expected Behavior
The netlify.toml should contain these redirects (in order):

```toml
[[redirects]]
  from = "/auth/register"
  to = "https://what-is-my-delta-site-production.up.railway.app/auth/register"
  status = 200
  force = true

[[redirects]]
  from = "/auth/login"
  to = "https://what-is-my-delta-site-production.up.railway.app/auth/login"
  status = 200
  force = true

[[redirects]]
  from = "/auth/me"
  to = "https://what-is-my-delta-site-production.up.railway.app/auth/me"
  status = 200
  force = true

# Should be LAST
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### 6. Common Issues to Check

**Issue: Netlify didn't deploy latest commit**
- Solution: Manually trigger redeploy from dashboard
- Go to Deploys → Trigger deploy → Deploy site

**Issue: Build directory is wrong**
- Solution: Verify `base = "mosaic_ui"` and `publish = "mosaic_ui"` in netlify.toml
- Check Site settings → Build settings match this

**Issue: netlify.toml not being read**
- Solution: Verify netlify.toml is at repository root, NOT inside mosaic_ui/
- File should be at: `/netlify.toml` (root level)

**Issue: Redirect order is wrong**
- Solution: Auth routes MUST come before `/*` catch-all
- Netlify processes redirects in order - first match wins

**Issue: Cache is serving old config**
- Solution: Clear cache and redeploy
- Go to Site settings → Build & deploy → Post processing → Clear cache and retry deploy

### 7. Force Fresh Deployment

If nothing else works:
1. Go to Deploys tab
2. Click "Trigger deploy"
3. Select "Clear cache and deploy site"
4. Wait for deployment to complete
5. Test: `curl https://whatismydelta.com/auth/login -X POST -H "Content-Type: application/json" -d '{"email":"test","password":"test"}'`
6. Expected: JSON error response (NOT HTML)

### 8. Verification Commands

After deployment, run these tests:

```bash
# Should return JSON error (NOT HTML)
curl https://whatismydelta.com/auth/login \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"test","password":"test"}'

# Should return JSON with user data
curl https://whatismydelta.com/auth/register \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@test.com","password":"password123"}'

# Should return JSON error about missing header
curl https://whatismydelta.com/auth/me \
  -H "X-User-ID: test"
```

### 9. Report Back

Please provide:
1. Latest deploy status (success/failed/building)
2. Whether netlify.toml was processed (check deploy log)
3. Current redirect rules visible in dashboard
4. Results of the verification curl commands
5. Any error messages from build/deploy logs

## Expected Outcome

After successful deployment:
- `/auth/register` → proxies to Railway, returns JSON
- `/auth/login` → proxies to Railway, returns JSON
- `/auth/me` → proxies to Railway, returns JSON
- All responses should be JSON, NOT HTML

## Context

This is the Mosaic Platform authentication system. Railway backend is fully functional and tested. The only issue is Netlify not proxying the auth routes correctly. The netlify.toml configuration is correct and committed - we just need Netlify to deploy it.

---

**URGENT**: The Railway backend is working perfectly. This is purely a Netlify proxy configuration deployment issue. Focus on getting Netlify to read and apply the netlify.toml redirect rules.
