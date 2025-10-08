# Foundation & Mosaic Development Guide

## Architecture
- Microservices architecture: Foundation (Safety & Evidence) + Mosaic (Career Transition Platform)
- Production URL: https://whatismydelta.com (LIVE ✅)
- Backend API: Railway deployment at what-is-my-delta-site-production.up.railway.app
- Frontend: Netlify deployment (resonant-crostata-90b706)
- Repository: github.com/DAMIANSEGUIN/wimd-railway-deploy

## Deployment Status (v2.0 Phase 1-4+ - PRODUCTION)
- ✅ Frontend: Fully deployed and functional
- ✅ Backend API: Railway deployment operational
- ✅ Authentication: Login/register/password reset flows working
- ✅ Chat/Coach: Career coaching chat interface operational
- ✅ File Upload: Resume/document upload functional
- ✅ Interactive UI: ALL navigation working (explore, find, apply, chat, guide, upload)
- ✅ Trial Mode: 5-minute trial for unauthenticated users
- ✅ Proxy Configuration: Netlify → Railway API routes configured
- ✅ Phase 1: Migration framework + CSV→AI fallback + feature flags
- ✅ Phase 2: Experiment engine backend (feature flag disabled)
- ✅ Phase 3: Self-efficacy metrics + coach escalation + Focus Stack UI
- ✅ Phase 4: RAG baseline + job feeds + 13 job sources
- ✅ Phase 4+: Dynamic source discovery + cost controls + competitive intelligence + OSINT + domain-adjacent search

## API Endpoints
- Health: `/health`, `/health/comprehensive`, `/health/recover`, `/health/prompts`, `/health/rag`, `/health/experiments`
- Config: `/config`
- Prompts: `/prompts/*`
- WIMD: `/wimd/*`
- Opportunities (legacy): `/ob/*`
- Jobs (Phase 4+): `/jobs/search`, `/jobs/search/rag`, `/jobs/{job_id}`
- Resume: `/resume/rewrite`, `/resume/customize`, `/resume/feedback`, `/resume/versions`
- Auth: `/auth/register`, `/auth/login`, `/auth/me`, `/auth/reset-password`
- RAG: `/rag/embed`, `/rag/batch-embed`, `/rag/retrieve`, `/rag/query`, `/rag/domain-adjacent`
- Intelligence: `/intelligence/company/{company_name}`, `/intelligence/positioning`, `/intelligence/resume-targeting`, `/intelligence/ai-prompts`
- OSINT: `/osint/analyze-company`, `/osint/health`
- Sources: `/sources/discover`, `/sources/analytics`
- Cost: `/cost/analytics`, `/cost/limits`
- Domain Adjacent: `/domain-adjacent/discover`, `/domain-adjacent/health`

## Current Status (Updated: 2025-10-07 - Phase 4 COMPLETE + All 12 Free Sources LIVE)
- ✅ UI frontend: OPERATIONAL
- ✅ Chat/Coach interface: OPERATIONAL
- ✅ Backend API: OPERATIONAL (FastAPI on Railway)
- ✅ Authentication: OPERATIONAL (with password reset)
- ✅ File handling: OPERATIONAL
- ✅ Self-efficacy metrics: OPERATIONAL (backend + UI toggle)
- ✅ Coach escalation: OPERATIONAL
- ✅ Experiment engine: IMPLEMENTED (feature flag disabled)
- ✅ Button functionality: ALL WORKING (explore, find, apply, chat, guide, upload)
- ✅ Job search: OPERATIONAL (Phase 4 deployed - find jobs button working)
- ✅ Resume optimization: OPERATIONAL (Phase 4 deployed - apply button working)
- ✅ RAG engine: OPERATIONAL (real OpenAI embeddings, no fallback - api/rag_engine.py:172)
- ✅ Job sources: ALL 12 FREE SOURCES IMPLEMENTED (deployed 2025-10-07)
- ✅ Competitive intelligence: OPERATIONAL (company analysis, positioning, resume targeting)
- ✅ Cost controls: OPERATIONAL (usage tracking, daily/monthly limits, emergency stop)

## Job Sources Status (Updated: 2025-10-07)
**All 12 Free Sources Implemented:**
- ✅ **6 Direct API Sources** (production-ready):
  - RemoteOK (JSON API - api/job_sources/remoteok.py)
  - WeWorkRemotely (RSS feed - api/job_sources/weworkremotely.py)
  - HackerNews (Firebase API - api/job_sources/hackernews.py)
  - Greenhouse (Multi-board API - api/job_sources/greenhouse.py)
  - Indeed (RSS feed - api/job_sources/indeed.py)
  - Reddit (JSON API - api/job_sources/reddit.py)
- ✅ **6 Web Scraping Sources** (deployed, needs testing):
  - LinkedIn (BeautifulSoup - api/job_sources/linkedin.py)
  - Glassdoor (BeautifulSoup - api/job_sources/glassdoor.py)
  - Dice (BeautifulSoup - api/job_sources/dice.py)
  - Monster (BeautifulSoup - api/job_sources/monster.py)
  - ZipRecruiter (BeautifulSoup - api/job_sources/ziprecruiter.py)
  - CareerBuilder (BeautifulSoup - api/job_sources/careerbuilder.py)

**Cost Savings:** $3,120-7,200/year by using free sources vs. paid APIs

## Outstanding Issues
- ⚠️ **Testing Required**: All 12 job sources deployed but untested in production
  - Web scraping sources may need CSS selector adjustments
  - Need to verify real job data returns from all sources
- ⚠️ **Email Service**: Password reset sends placeholder message (needs SendGrid/AWS SES integration)
- ⚠️ **Feature Flags**: Phase 4 features NOW ENABLED
  - ✅ `RAG_BASELINE`: **ENABLED** (RAG-powered job search active)
  - ✅ `JOB_SOURCES_STUBBED_ENABLED`: **ENABLED** (all 12 sources active)
  - ✅ `AI_FALLBACK_ENABLED`: **ENABLED** (CSV→AI fallback now working properly - cache cleared, flag enabled)
  - ⚠️ `EXPERIMENTS_ENABLED`: disabled (experiment engine)

## Import Patterns
@issues.json
@decision_matrix.csv
@surface_presence.json
@docs/README.md

## Surface Presence Map
```json
{
  "ui_frontend": true,
  "api_backend": true,
  "llm_generation": true,
  "agent_orchestration": false,
  "orchestration": false,
  "retrieval_or_vector_or_cache": false,
  "jobs_scheduling": false,
  "config": true,
  "prompt_asset": false
}
```

## Nate's Solution Ladder (Decision Matrix)
1. Data ingestion & cleaning → Data Ops
2. Storage & retrieval → Data Ops (+RAG if justified)
3. Scoring/Ranking → Classical ML
4. Generation (resumes/prompts/personas) → LLM with Evidence Bridge
5. Workflow automation → Thin Agents
6. UI → Data Ops (+typed contracts)
7. API → Data Ops (+typed contracts)
8. Observability & Governance → Data Ops (+eval traces)
9. **Safety & Evidence (Foundation)** → **Data Ops + LLM**

## Resolved Issues (v1.0 + v2.0 Phase 1-3)
- ✅ **BLOCKER-UI-ASK**: Chat/coach interface now operational
- ✅ **BLOCKER-API-BACKEND**: Backend deployed on Railway and connected
- ✅ **Button functionality**: All Phase 1-3 interactive elements working
- ✅ **Cache management**: Browser caching disabled for proper updates
- ✅ **Trial mode**: Unauthenticated users get 5-minute trial period
- ✅ **Phase 1**: Migration framework, CSV→AI fallback, feature flags deployed
- ✅ **Phase 2**: Experiment engine backend implemented (gated by flag)
- ✅ **Phase 3**: Self-efficacy metrics + coach escalation + Focus Stack UI deployed
- ✅ **Password reset**: Forgot password flow implemented (email service pending)
- ✅ **CSV lookup fix**: Fixed prompt selector to properly handle response/completion fields (api/prompt_selector.py:118)
- ✅ **Auto-restart monitoring**: Railway health checks with automatic restart on prompt system failure

## Monitoring & Auto-Restart System
- **Railway Health Checks**: Configured via `railway.toml` with `/health` endpoint monitoring
- **Automatic Recovery**: System attempts cache clearing and flag reset on failure
- **Multi-layer Monitoring**:
  - `/health` - Basic health with 503 status on failure (triggers Railway restart)
  - `/health/comprehensive` - Detailed monitoring with failure rate tracking
  - `/health/recover` - Manual recovery endpoint for system fixes
- **Failure Detection**: Tests actual prompt responses, not just API availability
- **Health Logging**: Stores failure history in `prompt_health_log` table
- **Recovery Actions**: Cache clearing, feature flag reset, database connectivity checks
- **Auto-restart Triggers**: 503 HTTP status codes automatically trigger Railway container restart

## Technical Implementation Notes
- Frontend uses vanilla JavaScript (ES6+) with IIFE pattern
- Event listeners use null checks to prevent script crashes
- Semantic search uses OpenAI embeddings with cosine similarity
- Authentication uses SQLite database backend
- Auto-save functionality for user session data
- localStorage for client-side session persistence
- Trial timer persists across page refreshes via localStorage

## Known Limitations (v1.0)
- No staging environment (direct to production deployment)
- API keys stored in Railway environment variables (secure but not rotated)
- CSV prompt library integration incomplete
- No automated testing pipeline
- Browser requirement: Chrome 55+, Firefox 52+, Safari 10.1+, Edge 15+ (2017+)

## Foundation Integration Points
- Safety layer: Data Ops + LLM for evidence validation (pending)
- Evidence Bridge: Connect classical ML scoring with LLM generation (pending)
- Governance: Eval traces for observability (pending)
- Security: API keys managed via Railway environment variables

## Recent Changes (2025-10-07)
**Phase 4 Recovery & Full Implementation:**
1. **Clean Rollback**: Reverted to stable commit f439633 (pre-failed Cursor implementation)
2. **RAG Engine Fixed**: Removed random fallback, now uses real OpenAI embeddings exclusively
3. **All 12 Job Sources Implemented**:
   - 6 direct API sources using HTTP requests + JSON/RSS/XML parsing
   - 6 web scraping sources using BeautifulSoup4 + CSS selectors
   - Added `requests` and `beautifulsoup4` to requirements.txt
4. **Feature Flags Updated**: Enabled RAG_BASELINE + JOB_SOURCES_STUBBED_ENABLED
5. **Deployed to Production**: Pushed to Railway, health check confirms deployment successful

## Next Steps for v2.0 Phase 4+
- ✅ **Phase 4 Implementation** (Claude Code): COMPLETE (2025-10-07)
- ✅ **Phase 4 Deployment** (Claude Code): COMPLETE (2025-10-07)
- 📋 **Immediate Next Steps**:
  - **CRITICAL**: Stress test all 12 job sources with persona testing framework
  - Verify real job data returns from each source
  - Monitor error rates and adjust CSS selectors if needed
  - Email service integration for password reset (SendGrid/AWS SES)
  - Monitor cost controls and usage analytics
- 📋 **Future Considerations**:
  - Automated testing implementation with persona cloning
  - Staging environment setup
  - API key rotation strategy
  - A/B testing for RAG vs. traditional search
  - CSS selector monitoring for web scraping sources