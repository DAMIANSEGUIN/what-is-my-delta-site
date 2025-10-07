# CODEX → Claude Code Handoff (2025-10-06)

## TL;DR
- Treat the "Phase 4" job/RAG/competitive-intelligence features as prototypes. The code is present, but everything is still mocked or disabled and the docs claiming they're live are inaccurate.
- Reset expectations with stakeholders, then focus on (a) restoring production smoke tests on the custom domain, (b) wiring the new API endpoints through Netlify, and (c) deciding which Phase 4 items to finish versus cutting for now.
- No sensitive keys are loaded anywhere. `.env` is a template with placeholders, `secure_key_loader.py` has never been run, and Railway will not see the required secrets until you add them yourself.

---

## Reality Check vs. Prior Notes
- `CLAUDE.md` and multiple handoff files say every Phase 4 feature shipped; that conflicts with the actual repository state.
  - `feature_flags.json`: only `SELF_EFFICACY_METRICS` and `COACH_ESCALATION` are enabled. `RAG_BASELINE` and `JOB_SOURCES_STUBBED_ENABLED` stay `false`, so the new pipelines never run in production.
  - `.env`: still contains `OPENAI_API_KEY=your_openai_api_key_here` and `CLAUDE_API_KEY=your_claude_api_key_here`. Nothing will authenticate until real keys are supplied.
  - All job source modules (`api/job_sources/*.py`) return hard-coded mock data; the `requests` imports are commented out. The "15 job sources" story is aspirational only.
  - `api/competitive_intelligence.py`, `api/cost_controls.py`, `api/rag_engine.py`, etc. all synthesize canned output. Several guard rails rely on SQLite tables that may not even exist remotely because migrations were never executed.
- Before you trust any of the new endpoints, pull the logs in Railway → "Deployments" and confirm we have ever run a migration after `2025-09-29`. I see no migration history locally, so assume the database is still at the pre-Phase-4 schema.

---

## Immediate Priorities for Claude Code
1. **Re-establish production observability**
   - Run `./scripts/verify_deploy.sh https://whatismydelta.com` once routing is fixed. At the moment the script fails because the domain proxies skip new endpoints (see below).
   - Manually hit `https://what-is-my-delta-site-production.up.railway.app/health` to double-check origin health; make sure the Railway deployment date matches our latest code push.
   - Capture current Railway + Netlify deploy IDs in `CONVERSATION_NOTES.md` once verified.

2. **Fix Netlify routing for the expanded API surface**
   - `netlify.toml` only proxies `/health`, `/config`, `/prompts/*`, `/wimd*`, `/ob/*`, `/resume/*`, `/auth/*`.
   - Add rewrites for the new endpoints: `/jobs/*`, `/rag/*`, `/sources/*`, `/cost/*`, `/intelligence/*`, `/osint/*`, `/analytics/*`, `/domain-adjacent/*`, `/corpus/*`.
   - Redeploy the frontend with `scripts/deploy_frontend_netlify.sh` and re-run the smoke tests against `whatismydelta.com`.

3. **Decide the Phase 4 scope**
   - If we want production-quality job search, you must build real integrations (RemoteOK, WeWorkRemotely, etc.) instead of the current stub loops. Otherwise keep the feature behind a flag and make the UI hide it.
   - The RAG engine currently calls OpenAI directly and falls back to random vectors if the request fails. Without rate limiting, caching, and evals this should not be exposed to end users.
   - The "cost controls" write into SQLite via `api/cost_controls.py`; confirm the tables exist and consider disabling this surface until we add tests.

4. **Credential management**
   - Decide where to store the real API keys. Recommended: add them as Railway variables and update `PUBLIC_API_BASE` there (it is empty locally).
   - If you keep the `.env` workflow, replace placeholders and run `python secure_key_loader.py` locally to verify the loader actually persists to `.env.jobsearch` (currently untested).
   - Update `env_template.txt` to match whatever final variable list you settle on.

5. **Documentation cleanup**
   - Update `CONVERSATION_NOTES.md` and `ROLLING_CHECKLIST.md` with the accurate status (job search/RAG pending, rewrites pending, migrations unverified).
   - Either delete or clearly flag the contradictory handoff docs (`CLAUDE.md`, `CLAUDE_CODE_HANDOFF_2025-10-06.md`, etc.) so future agents do not assume work is complete.

---

## Useful Files & References
- `netlify.toml` — missing rewrites for new endpoints.
- `feature_flags.json` — confirms which features are actually on.
- `api/job_sources/*.py` — all mocked data; no real HTTP calls.
- `api/rag_engine.py` — disabled unless `RAG_BASELINE` flips; installs `openai` at runtime and generates random embeddings on failure.
- `secure_key_loader.py` — interactive helper; never executed.
- `scripts/verify_deploy.sh` — production smoke tests; currently failing on custom domain.

---

## Suggested Next Moves (if continuing Phase 4)
1. Wire Netlify rewrites ➜ redeploy ➜ run smoke tests.
2. Run pending migrations against Railway (confirm state before/after).
3. Replace mocked job-source implementations with real calls (start with RemoteOK + WeWorkRemotely since they are easiest).
4. Introduce integration tests for `/jobs/search` and `/jobs/search/rag` using VCR or recorded fixtures.
5. Only after tests pass, flip `RAG_BASELINE` (and optionally `JOB_SOURCES_STUBBED_ENABLED`) via `feature_flags` table/migration.
6. Document the rollout plan in `CONVERSATION_NOTES.md` and notify the team.

Let me know if you need anything else before you dive back in.
