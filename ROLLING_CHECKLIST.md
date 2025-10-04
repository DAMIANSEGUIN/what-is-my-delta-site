# Rolling Checklist (Gated)

| Step | What | Owner | Where | Status |
|---|---|---|---|---|
| 0.1 | Add `.gitignore` / `.env.example` | AI | repo | ✅ |
| 0.2 | Add GitHub Secret Scan action | AI | `.github/workflows/secret-scan.yml` | ✅ |
| 0.3 | Move secrets to Railway Variables | YOU | Railway UI | ✅ |
| 0.4 | Scan repo for secrets | AI | CI PR check | ☐ |
| 0.5 | Startup tripwire wired | AI | `api/settings.py`, `api/startup_checks.py` | ✅ |
| 0.6 | Strict CORS + `/config` | AI | `api/index.py` | ✅ |
| 0.7 | Frontend uses `/config.apiBase` | AI | frontend | ✅ |
| 0.8 | No client-side provider calls | AI | frontend/backend audit | ✅ |
| 4.1 | Custom domain setup | YOU | Netlify DNS → Railway | ✅ |
| 4.2 | Domain verification | AI | Railway dashboard | ✅ |
| 4.3 | SSL certificate | AI | Railway automatic | ✅ |
| 1.1 | Start cmd/health fixed | AI | `Procfile`, `railway.json` | ✅ (Railway `/health` = `{"ok": true}` on 2025-09-29) |
| 1.2 | Set required envs | YOU | Railway Variables | ✅ |
| 1.3 | Deploy + smoke test | AI | logs + `verify_deploy.sh` | ⚠️ (blocked by Netlify 404; rerun after rewrite) |
| 2.1 | Prompts registry implemented | AI | `api/prompts_loader.py` | ✅ |
| 2.2 | Ingest latest CSV | YOU | admin/upload | ✅ |
| 2.3 | Verify active SHA | AI | registry/endpoint | ✅ |
| 3.1 | Pre-deploy sanity | AI | `scripts/predeploy_sanity.sh` | ✅ |
| 3.2 | (Opt) DB + Alembic head | AI/YOU | DB/Alembic | ☐ |
| 3.3 | Final deploy + smoke | AI | `verify_deploy.sh` | ⚠️ (awaiting domain rewrite + smoke rerun) |
| 5.1 | SQLite session store + auto-cleanup | AI | `api/storage.py` | ✅ |
| 5.2 | POST /wimd implemented | AI | `api/index.py` | ✅ |
| 5.3 | POST /wimd/upload implemented | AI | `api/index.py` | ✅ |
| 5.4 | OB endpoints (`/ob/*`) wired | AI | `api/index.py` | ✅ |
| 5.5 | Resume endpoints (`/resume/*`) wired | AI | `api/index.py` | ✅ |
| 5.6 | Mosaic UI wired to API flows | AI | `mosaic_ui/index.html` | ✅ |
| 6.1 | Run `predeploy_sanity.sh` (Phase 3) | AI | `scripts/predeploy_sanity.sh` | ✅ |
| 7.1 | User authentication system | Claude in Cursor | `mosaic_ui/index.html` | ✅ (2025-10-02) |
| 7.2 | User onboarding and guide | Claude in Cursor | `mosaic_ui/index.html` | ✅ (2025-10-02) |
| 7.3 | File organization cleanup | Claude in Cursor | `mosaic_ui/` | ✅ (2025-10-02) |
| 7.4 | User experience enhancement | Claude in Cursor | `mosaic_ui/index.html` | ✅ (2025-10-02) |
| 8.1 | Backend user authentication APIs | CODEX | `api/index.py`, `api/storage.py` | ☐ |
| 8.2 | Database user table | CODEX | Database schema | ☐ |
| 8.3 | Railway deployment updates | Claude Code | Railway config | ☐ |
| 8.4 | Production testing | Claude Code | All endpoints | ☐ |
| 9.1 | Phase 1: Migration framework | Cursor | `api/migrations.py` | ✅ (2025-10-03) |
| 9.2 | Phase 1: CSV→AI fallback system | Cursor | `api/prompt_selector.py`, `api/ai_clients.py` | ✅ (2025-10-03) |
| 9.3 | Phase 1: Feature flags system | Cursor | `feature_flags.json` | ✅ (2025-10-03) |
| 9.4 | Phase 1: Prompt selector integration | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 9.5 | Phase 1: Health endpoints | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 10.1 | Phase 2: Experiment schema migration | Cursor | `api/migrations.py` | ✅ (2025-10-03) |
| 10.2 | Phase 2: Experiment engine APIs | Cursor | `api/experiment_engine.py` | ✅ (2025-10-03) |
| 10.3 | Phase 2: Experiment endpoints | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 10.4 | Phase 2: Learning data capture | Cursor | `api/experiment_engine.py` | ✅ (2025-10-03) |
| 10.5 | Phase 2: Self-efficacy metrics | Cursor | `api/experiment_engine.py` | ✅ (2025-10-03) |
| 10.6 | Phase 2: Health endpoints | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 11.1 | Phase 3: Self-efficacy metrics engine | Cursor | `api/self_efficacy_engine.py` | ✅ (2025-10-03) |
| 11.2 | Phase 3: Coach escalation system | Cursor | `api/self_efficacy_engine.py` | ✅ (2025-10-03) |
| 11.3 | Phase 3: Frontend UI implementation | Cursor | `mosaic_ui/index.html` | ✅ (2025-10-03) |
| 11.4 | Phase 3: Toggle system for metrics | Cursor | `mosaic_ui/index.html` | ✅ (2025-10-03) |
| 11.5 | Phase 3: Feature flags enabled | Cursor | `feature_flags.json` | ✅ (2025-10-03) |
| 11.6 | Phase 3: System testing complete | Cursor | All components | ✅ (2025-10-03) |
| 12.1 | Phase 4: RAG engine implementation | Cursor | `api/rag_engine.py` | ✅ (2025-10-03) |
| 12.2 | Phase 4: Job sources interface | Cursor | `api/job_sources/` | ✅ (2025-10-03) |
| 12.3 | Phase 4: Database migrations | Cursor | `api/migrations/004_add_rag_tables.sql` | ✅ (2025-10-03) |
| 12.4 | Phase 4: API endpoints integration | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 12.5 | Phase 4: Job sources catalog | Cursor | `docs/job_sources_catalog.md` | ✅ (2025-10-03) |
| 13.1 | RAG Dynamic Sources: Source discovery engine | Cursor | `api/rag_source_discovery.py` | ✅ (2025-10-03) |
| 13.2 | RAG Dynamic Sources: Dynamic integration | Cursor | `api/rag_source_discovery.py` | ✅ (2025-10-03) |
| 13.3 | RAG Dynamic Sources: Database migration | Cursor | `api/migrations/005_add_dynamic_sources.sql` | ✅ (2025-10-03) |
| 13.4 | RAG Dynamic Sources: API endpoints | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 14.1 | Cost Controls: Usage tracking system | Cursor | `api/cost_controls.py` | ✅ (2025-10-03) |
| 14.2 | Cost Controls: Cost limits implementation | Cursor | `api/cost_controls.py` | ✅ (2025-10-03) |
| 14.3 | Cost Controls: Resource limits | Cursor | `api/cost_controls.py` | ✅ (2025-10-03) |
| 14.4 | Cost Controls: Database migration | Cursor | `api/migrations/006_add_usage_tracking.sql` | ✅ (2025-10-03) |
| 14.5 | Cost Controls: API integration | Cursor | `api/index.py`, `api/rag_engine.py` | ✅ (2025-10-03) |
| 14.6 | Cost Controls: Documentation update | Cursor | `docs/job_sources_catalog.md` | ✅ (2025-10-03) |
| 17.1 | Competitive Intelligence: Company analysis engine | Cursor | `api/competitive_intelligence.py` | ✅ (2025-10-03) |
| 17.2 | Competitive Intelligence: API endpoints | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 17.3 | Competitive Intelligence: Documentation | Cursor | `docs/competitive_intelligence_guide.md` | ✅ (2025-10-03) |
| 17.4 | Competitive Intelligence: Testing | Cursor | `api/competitive_intelligence.py` | ✅ (2025-10-03) |
| 17.5 | Competitive Intelligence: Integration | Cursor | `api/index.py` | ✅ (2025-10-03) |
| 18.1 | Phase 4+ Deployment: Backend to Railway | Claude Code | Railway | ✅ (2025-10-04) |
| 18.2 | Phase 4+ Deployment: Frontend wiring | Claude Code | `mosaic_ui/index.html` | ✅ (2025-10-04) |
| 18.3 | Phase 4+ Deployment: Find Jobs button fix | Claude Code | `mosaic_ui/index.html` | ✅ (2025-10-04) |
| 18.4 | Phase 4+ Deployment: Apply button fix | Claude Code | `mosaic_ui/index.html` | ✅ (2025-10-04) |
| 18.5 | Phase 4+ Deployment: Production testing | Claude Code | Production | ✅ (2025-10-04) |
| 18.6 | Phase 4+ Deployment: All nav verified working | Claude Code | Production | ✅ (2025-10-04) |
