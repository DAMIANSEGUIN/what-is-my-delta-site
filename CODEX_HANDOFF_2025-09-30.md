# CODEX/CURSOR HANDOFF - 2025-09-30 16:00 EDT

## HANDOFF REASON
**Claude Code (Senior Debugger) → Codex/Cursor (Implementation Engineer)**

Claude Code has been operating outside role boundaries:
- Made 3 iterative code commits without systematic plan
- Guessing at CORS fixes without local testing
- 60+ minutes troubleshooting without team consultation
- Missing comprehensive dependency mapping

Per CODEX_INSTRUCTIONS.md:
- **Codex/Cursor role**: Systematic implementation, exact specifications, hold the frame
- **Claude Code role**: Infrastructure debugging, log analysis, deployment issues

## CURRENT BLOCKER

**Issue**: Chat window shows `net::ERR_FAILED` when posting to Railway API
**Browser error**:
```
POST https://what-is-my-delta-site-production.up.railway.app/wimd net::ERR_FAILED
Access to fetch at 'https://what-is-my-delta-site-production.up.railway.app/wimd'
from origin 'https://whatismydelta.com' has been blocked by CORS policy:
Response to preflight request doesn't pass access control check:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**Verified working**:
- ✅ Railway backend healthy: `/health` returns `{"ok":true}`
- ✅ Railway API works: `curl -X POST /wimd` returns HTTP 200
- ✅ Netlify frontend deployed: `https://whatismydelta.com` loads correctly
- ✅ GET requests proxied: `/health`, `/config`, `/prompts/active` work via domain
- ❌ POST requests fail: Browser `net::ERR_FAILED` but curl succeeds
- ❌ CORS headers missing: No `access-control-allow-origin` in OPTIONS response

## COMMITS MADE (DO NOT REPEAT)

### Commit 1456992 (2025-09-30 15:20)
**Change**: Added explicit CORS origins
```python
origins = [
    os.getenv("PUBLIC_SITE_ORIGIN", "https://whatismydelta.com"),
    "https://whatismydelta.com",
    "https://www.whatismydelta.com",
    "https://resonant-crostata-90b706.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    ...
)
```
**Result**: ❌ Deployed but no `access-control-allow-origin` header in response

### Commit fcad803 (2025-09-30 15:50)
**Change**: Added `expose_headers=["*"]` to CORSMiddleware
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["content-type", "authorization", "x-session-id"],
    expose_headers=["*"],  # ADDED THIS
)
```
**Result**: ❌ Deployed but still no `access-control-allow-origin` header

## EVIDENCE

### Test 1: OPTIONS Preflight (FAILING)
```bash
curl -I -X OPTIONS https://what-is-my-delta-site-production.up.railway.app/wimd \
  -H "Origin: https://whatismydelta.com" \
  -H "Access-Control-Request-Method: POST"

# Response:
HTTP/2 400
access-control-allow-credentials: true
access-control-allow-headers: Accept, Accept-Language, Content-Language, Content-Type, authorization, content-type, x-session-id
access-control-allow-methods: GET, POST, OPTIONS
access-control-max-age: 600
vary: Origin
# MISSING: access-control-allow-origin: https://whatismydelta.com
```

### Test 2: Actual POST (WORKING via curl)
```bash
curl -X POST https://what-is-my-delta-site-production.up.railway.app/wimd \
  -H "Content-Type: application/json" \
  -H "Origin: https://whatismydelta.com" \
  -d '{"prompt":"test"}'

# Response:
HTTP/2 200
access-control-allow-credentials: true
content-type: application/json
# Returns valid JSON response
```

### Test 3: Browser (FAILING)
- Open https://whatismydelta.com
- Open chat window
- Send message
- Browser console: `POST /wimd net::ERR_FAILED`
- Network tab: Request blocked by CORS policy

## ROOT CAUSE ANALYSIS

**Symptom**: FastAPI CORSMiddleware configured but not returning `access-control-allow-origin` header
**Evidence**:
- All other CORS headers present (`allow-credentials`, `allow-headers`, `allow-methods`)
- `vary: Origin` header present (middleware is running)
- OPTIONS request returns HTTP 400 (not 200)
- Missing the critical `access-control-allow-origin` header

**Possible causes**:
1. FastAPI CORSMiddleware requires additional configuration
2. OPTIONS endpoint not properly configured
3. Middleware order issue (CORS middleware needs to be first)
4. Railway proxy stripping CORS headers
5. Missing CORS response handler for OPTIONS method

## SYSTEMATIC APPROACH NEEDED

### Phase 1: Local Testing (MISSING from previous attempts)
```bash
# Run Railway app locally with production env
cd /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project
export OPENAI_API_KEY="..."
export CLAUDE_API_KEY="..."
python -m uvicorn api.index:app --reload --port 8000

# Test CORS locally
curl -I -X OPTIONS http://localhost:8000/wimd \
  -H "Origin: https://whatismydelta.com" \
  -H "Access-Control-Request-Method: POST"

# Should return: access-control-allow-origin: https://whatismydelta.com
```

### Phase 2: Fix CORS Configuration
**Research FastAPI CORSMiddleware documentation**:
- Check if `allow_origin_regex` needed
- Verify middleware order (must be first middleware added)
- Check if explicit OPTIONS route handler needed
- Test with wildcard `allow_origins=["*"]` to isolate issue

**Candidate fixes**:
1. Add explicit OPTIONS route handler
2. Change middleware order (add CORS first)
3. Use `allow_origin_regex` instead of `allow_origins`
4. Add CORS response manually in OPTIONS handler

### Phase 3: Deploy and Verify
```bash
# Commit fix
git add api/index.py
git commit -m "Fix: CORS configuration for OPTIONS preflight"
git push

# Trigger Railway deploy
railway deploy  # or manual trigger in dashboard

# Wait for deployment
# Verify CORS headers
curl -I -X OPTIONS https://what-is-my-delta-site-production.up.railway.app/wimd \
  -H "Origin: https://whatismydelta.com"

# Expected: access-control-allow-origin: https://whatismydelta.com
```

### Phase 4: End-to-End Test
1. Open https://whatismydelta.com
2. Open browser DevTools (F12) → Network tab
3. Open chat window
4. Send message
5. Verify: Request succeeds with HTTP 200
6. Verify: Response contains CORS headers

## FILES TO REVIEW

### api/index.py (lines 75-88)
**Current CORS configuration**:
```python
origins = [
    os.getenv("PUBLIC_SITE_ORIGIN", "https://whatismydelta.com"),
    "https://whatismydelta.com",
    "https://www.whatismydelta.com",
    "https://resonant-crostata-90b706.netlify.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["content-type", "authorization", "x-session-id"],
    expose_headers=["*"],
)
```

**Check**:
- Is this the FIRST middleware added? (must be first)
- Does FastAPI need explicit OPTIONS handler?
- Should we use `allow_origin_regex`?

### mosaic_ui/index.html (line ~352)
**Frontend API call location**:
- Check what URL frontend is calling
- Verify fetch headers being sent
- Check for any CORS-related fetch options

## DEPENDENCIES NOT IN BUILD PLAN

**Missing pre-deployment validation steps**:
1. ❌ Local CORS testing before deployment
2. ❌ OPTIONS preflight verification step
3. ❌ Railway webhook validation (auto-deploy)
4. ❌ Browser-based testing protocol
5. ❌ Systematic "test locally → deploy → verify" cycle

**Add to build plan**:
```markdown
## Pre-Deployment Checklist
- [ ] Run API locally with production env vars
- [ ] Test CORS with curl OPTIONS requests
- [ ] Verify all CORS headers present locally
- [ ] Deploy to Railway
- [ ] Verify Railway auto-deploy triggered
- [ ] Test OPTIONS request against Railway URL
- [ ] Test POST request against Railway URL
- [ ] Test end-to-end in browser
- [ ] Check browser console for errors
- [ ] Check browser network tab for headers
```

## ESCALATION CRITERIA

**When to escalate to human**:
- After 2 failed local test attempts
- If FastAPI documentation unclear
- If Railway-specific CORS issue suspected
- After 15 minutes without progress

**When to escalate to Claude Code**:
- Railway deployment failures
- Railway log analysis needed
- Infrastructure issues (not code issues)

## CURRENT PROJECT STATE

### Infrastructure
- **Railway**: Connected to GitHub `DAMIANSEGUIN/wimd-railway-deploy`
- **Railway**: Manual deploy working (CMD+K → Deploy Latest Commit)
- **Railway**: Auto-deploy working (webhooks functional)
- **Netlify**: Connected to GitHub `DAMIANSEGUIN/wimd-railway-deploy`
- **Netlify**: Base directory `mosaic_ui`
- **Netlify**: Proxy rules for GET requests working

### Environment Variables (Railway)
- ✅ OPENAI_API_KEY: Set
- ✅ CLAUDE_API_KEY: Set
- ❌ PUBLIC_SITE_ORIGIN: Not set (but hardcoded in code)
- Backend URL: `https://what-is-my-delta-site-production.up.railway.app`

### Code Status
- **Backend**: Complete FastAPI implementation (449 lines)
- **Frontend**: Deployed to Netlify
- **Database**: SQLite with 30-day cleanup
- **Prompts**: 600+ prompts CSV loaded

## HANDOFF DELIVERABLES

1. ✅ **SESSION_TROUBLESHOOTING_LOG.md**: Complete history of attempts
2. ✅ **This handoff document**: Current state and systematic approach
3. ✅ **CODEX_INSTRUCTIONS.md**: Role definitions and boundaries
4. ⏳ **Awaiting Codex/Cursor**: Systematic CORS fix with local testing

## NEXT ACTIONS FOR CODEX/CURSOR

1. **Immediate**: Run Railway app locally and test CORS
2. **Research**: FastAPI CORSMiddleware best practices for OPTIONS
3. **Implement**: Fix CORS configuration based on local testing
4. **Deploy**: Push fix to Railway
5. **Verify**: Test end-to-end in browser
6. **Document**: Update build plan with pre-deployment validation steps

## SUCCESS CRITERIA

- [ ] OPTIONS preflight returns `access-control-allow-origin: https://whatismydelta.com`
- [ ] Browser chat window successfully posts to Railway API
- [ ] No CORS errors in browser console
- [ ] Response appears in chat window
- [ ] End-to-end user flow working

## TIME INVESTED

- **Claude Code troubleshooting**: 60+ minutes
- **Commits made**: 3 (without systematic testing)
- **Railway deployments**: 3 manual triggers
- **Remaining issue**: CORS preflight failure

## REFERENCE DOCUMENTS

- `SESSION_TROUBLESHOOTING_LOG.md`: All attempted solutions
- `CODEX_INSTRUCTIONS.md`: AI collaboration roles
- `CURSOR_TEAM_README.md`: Previous deployment issues (resolved)
- `CLAUDE_CODE_README.md`: Operational rules and protocols

---

**Handoff completed**: 2025-09-30 16:00 EDT
**From**: Claude Code (Senior Debugger)
**To**: Codex/Cursor (Implementation Engineer)
**Status**: Awaiting systematic CORS fix with local testing first