# Git Authentication Fix & Deployment Instructions

## Current Status
- ✅ Minimal version ready (fixes internal server errors)
- ✅ All files committed locally  
- ❌ Git push failing due to authentication
- ❌ Vercel still running old version with bugs

## Quick Fix Options

### Option A: GitHub Web Interface (RECOMMENDED - 2 minutes)
1. Go to https://github.com/DAMIANSEGUIN/what-is-my-delta-site
2. Click "Upload files" 
3. Drag these files from `/Users/damianseguin/Downloads/mosaic_vercel_api/`:
   - `api/index.py` (the minimal working version)
   - `vercel.json` (updated configuration)
4. Commit message: "Fix: Deploy minimal version to resolve 500 errors"
5. Vercel will auto-deploy in 1-2 minutes

### Option B: Fix Git Authentication
1. **Create new GitHub token:**
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` permissions
   - Copy the token

2. **Update git remote:**
   ```bash
   cd /Users/damianseguin/Downloads/mosaic_vercel_api
   git remote set-url origin https://YOUR_TOKEN@github.com/DAMIANSEGUIN/what-is-my-delta-site.git
   git push origin main
   ```

### Option C: Force Deploy via Vercel Dashboard
1. Go to vercel.com → your project
2. Settings → Git → Disconnect and reconnect repository
3. Trigger manual deployment
4. Or use "Redeploy" button with latest commit

## What the Minimal Version Fixes
- ✅ Removes PyPDF2, openai imports causing crashes
- ✅ Working /health endpoint
- ✅ Working /test interface with proper HTML
- ✅ Placeholder WIMD/job search (for testing deployment)
- ✅ Ready to restore full functionality once stable

## Files Ready for Deployment
```
api/index.py          # Fixed minimal version (no heavy dependencies)  
api/index_full.py     # Complete version (restore later)
vercel.json          # Updated configuration  
requirements.txt     # Core dependencies only
```

## Expected Results After Deployment
- https://mosaic-platform.vercel.app/health → `{"ok": true}`
- https://mosaic-platform.vercel.app/test → Working HTML interface
- https://mosaic-platform.vercel.app/ → API info (minimal mode)

## Next Steps After Deployment Works
1. Gradually restore full WIMD functionality
2. Add back OpenAI integration
3. Enable file upload features
4. Full OpportunityBridge integration

**Recommendation: Use Option A (GitHub web upload) - fastest and most reliable.**