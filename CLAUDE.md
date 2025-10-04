# Foundation & Mosaic Development Guide

## Architecture
- Microservices architecture: Foundation (Safety & Evidence) + Mosaic (Career Transition Platform)
- Production URL: https://whatismydelta.com (LIVE ✅)
- Backend API: Railway deployment at what-is-my-delta-site-production.up.railway.app
- Frontend: Netlify deployment (resonant-crostata-90b706)
- Repository: github.com/DAMIANSEGUIN/wimd-railway-deploy

## Deployment Status (v2.0 Phase 1-3 - PRODUCTION)
- ✅ Frontend: Fully deployed and functional
- ✅ Backend API: Railway deployment operational
- ✅ Authentication: Login/register/password reset flows working
- ✅ Chat/Coach: Career coaching chat interface operational
- ✅ File Upload: Resume/document upload functional
- ✅ Interactive UI: All Phase 1-3 buttons working (explore, chat, guide, upload)
- ✅ Trial Mode: 5-minute trial for unauthenticated users
- ✅ Proxy Configuration: Netlify → Railway API routes configured
- ✅ Phase 1: Migration framework + CSV→AI fallback + feature flags
- ✅ Phase 2: Experiment engine backend (feature flag disabled)
- ✅ Phase 3: Self-efficacy metrics + coach escalation + Focus Stack UI
- ⏳ Phase 4: RAG baseline + job feeds (in development)

## API Endpoints
- Health: `/health`
- Config: `/config`
- Prompts: `/prompts/*`
- WIMD: `/wimd/*`
- Opportunities: `/ob/*`
- Resume: `/resume/*`
- Auth: `/auth/register`, `/auth/login`, `/auth/me`

## Current Status (Updated: 2025-10-04)
- ✅ UI frontend: OPERATIONAL
- ✅ Chat/Coach interface: OPERATIONAL
- ✅ Backend API: OPERATIONAL (FastAPI on Railway)
- ✅ Authentication: OPERATIONAL (with password reset)
- ✅ File handling: OPERATIONAL
- ✅ Self-efficacy metrics: OPERATIONAL (backend + UI toggle)
- ✅ Coach escalation: OPERATIONAL
- ✅ Experiment engine: IMPLEMENTED (feature flag disabled)
- ✅ Button functionality: Phase 1-3 complete (explore, chat, guide, upload)
- ⏳ Job search: Waiting on Phase 4 (find jobs button not functional yet)
- ⏳ Resume optimization: Waiting on Phase 4 (apply button not functional yet)

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

## Next Steps for v2.0 Phase 4
- ⏳ **Phase 4 Implementation** (Cursor): RAG baseline + job feeds
  - Build embedding pipeline (OpenAI ADA)
  - Retrieval wrapper with confidence thresholds
  - Job sources catalog and connectors
  - Opportunity cards with live data
  - Enable "Find Jobs" functionality
  - Add resume tools section for "Apply" functionality
- 🚀 **Phase 4 Deployment** (Claude Code): After Cursor completes Phase 4
  - Deploy RAG baseline backend
  - Deploy job feeds integration
  - Enable feature flags gradually
  - Test opportunity search
  - Validate resume optimization
- 📋 **Future Considerations**:
  - Email service integration for password reset
  - Automated testing implementation
  - Staging environment setup
  - API key rotation strategy