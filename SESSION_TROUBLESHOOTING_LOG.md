# Session Troubleshooting Log - 2025-09-30

## Issue: Domain API routing and chat "failed to fetch" error

### What Was Attempted (DO NOT RETRY THESE):

1. ❌ **Multiple empty git commits to trigger Netlify deployment** - Site wasn't connected to GitHub
2. ❌ **Copying netlify.toml to mosaic_ui directory** - Already done, wasn't the issue
3. ❌ **Adding [build] section to netlify.toml** - Made it worse
4. ❌ **Removing [build] section from netlify.toml** - Didn't fix POST proxy issue
5. ❌ **Installing Homebrew/Node.js/Netlify CLI** - Takes forever, system too old (macOS 12)
6. ❌ **Waiting for Netlify to "pick up" changes** - Site wasn't monitoring GitHub repo

### What Actually Worked:

1. ✅ **Connected Netlify site to GitHub in dashboard** - This was the root cause
   - Site ID: `bb594f69-4d23-4817-b7de-dadb8b4db874` (resonant-crostata-90b706)
   - Had `Repo: N/A` - not monitoring any repository
   - User manually connected in Netlify dashboard: Settings → Build & deploy → Link repository
   - Repository: `DAMIANSEGUIN/wimd-railway-deploy`
   - Base directory: `mosaic_ui`
   - Result: GET requests (health, config) now work via domain

2. ⚠️ **Netlify POST proxy limitation discovered**
   - POST requests to external URLs return `HTTP 307` redirect to `http://` (not https)
   - Browser blocks mixed content
   - This is a known Netlify limitation, not fixable via netlify.toml
   - CORS headers exist on Railway but `access-control-allow-origin` missing

### Current Status:

- ✅ Railway backend: Fully operational at `https://what-is-my-delta-site-production.up.railway.app`
- ✅ Domain GET requests: Working (`/health`, `/config`, `/prompts/active`)
- ❌ Domain POST requests: Return 307 redirect (Netlify limitation)
- ⚠️ Chat functionality: Should work via Railway URL fallback in frontend (line 352 of index.html)

### Real Solution Needed:

**Option 1: Fix CORS on Railway backend (RECOMMENDED)**
- Add explicit `access-control-allow-origin: https://whatismydelta.com` header
- Located in: `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/api/index.py`
- Look for CORSMiddleware configuration around line 77
- Add `allow_origins=["https://whatismydelta.com", "https://www.whatismydelta.com"]`

**Option 2: Create Netlify Function as proxy wrapper**
- Create `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project/netlify/functions/wimd.js`
- Function proxies POST requests to Railway
- Frontend calls `/api/wimd` which triggers function

**Option 3: Accept that frontend calls Railway directly**
- Frontend already has Railway URL hardcoded as fallback (line 352)
- Just needs proper CORS headers from Railway
- This is the fastest fix

### Files Modified This Session:

1. `netlify.toml` (root) - Added [build] section (later removed from mosaic_ui copy)
2. `mosaic_ui/netlify.toml` - Created with redirects, added [build], then removed [build]
3. `CONVERSATION_NOTES.md` - Updated status
4. Multiple documentation files created during troubleshooting

### Key Learnings:

1. **Always verify if site is connected to Git first** - Run: `curl -s "https://api.netlify.com/api/v1/sites/{SITE_ID}" | grep repo_url`
2. **Netlify POST proxying has limitations** - External URLs get 307 redirects, not true proxies
3. **Frontend fallback works** - The hardcoded Railway URL in JavaScript is intentional
4. **Don't waste time on CLI installations** - Old macOS systems (12) take forever with Homebrew
5. **Read documentation before acting** - CLAUDE_CODE_README.md lines 831-843 define role clearly

### Next Action Required:

Fix CORS headers in Railway backend to explicitly allow `https://whatismydelta.com` origin, then chat will work.