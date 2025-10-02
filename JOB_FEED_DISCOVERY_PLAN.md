# Job Feed Discovery & Integration Plan (2025-10-01)

Use this runbook to expand OpportunityBridge from static data to live job intelligence. Share with Mosaic team, Netlify Agent Runners, LLM collaborators, and future ChatGPT agents.

## 1. Current Backend Gaps
- Coach replies lack the CSV → AI → metrics fallback (see `AI_ROUTING_PLAN.md`).
- OpportunityBridge matches use the placeholder `JOB_LIBRARY`; no live data source yet.
- Mosaic UI is not wired to the `/ob/*` endpoints.
- No catalog of sanctioned job feeds or community signals exists.

## 2. Objectives
1. Maintain a vetted list of job-data sources (official APIs, aggregators, community feeds).
2. Provide a repeatable process to evaluate, authorize, and integrate each source.
3. Supply connector templates and test commands so new feeds can be added quickly.
4. Keep legal/usage requirements explicit to avoid ToS violations.

## 3. Source Catalog Workflow
1. Create/maintain `docs/job_sources_catalog.md` with columns: `Name`, `Type`, `Region`, `Auth`, `Rate Limits`, `Data Fields`, `Status`, `Notes`.
2. Weekly or when needed, run discovery:
   - Search API directories (RapidAPI, ProgrammableWeb, Public APIs list) for keywords: “jobs”, “careers”, “opportunity”, “hiring feed”.
   - Check official job SaaS providers (Greenhouse, Lever, Workable, Ashby, JazzHR) for public feed docs.
   - Monitor community APIs (Reddit, Hacker News Algolia, specialized forums) for job-related endpoints.
   - Log leads into the catalog with status `candidate`.
3. For each candidate, evaluate:
   - Terms of service (explicit allowance for programmatic use?).
   - Authentication model (API key, OAuth, IP whitelist, paid plan).
   - Response schema & localization, pagination, filtering.
   - Update catalog status to `approved`, `rejected`, or `needs review` with justification.

## 4. Connector Implementation Steps
1. For an approved source, create a new module in `api/job_sources/` following pattern `greenhouse.py`, `serpapi.py`, etc.
2. Each connector exports `async def fetch_jobs(settings) -> List[Dict[str, Any]]` returning normalized fields: `id`, `title`, `company`, `location`, `url`, `description`, `tags`, `source_metadata`.
3. Update `requirements.txt` if the provider needs SDKs (e.g., `serpapi`, `requests_oauthlib`).
4. Add configuration entries to `api/settings.py` (`GREENHOUSE_BOARD_TOKENS`, `SERPAPI_KEY`, etc.) and document env variables in `OPERATIONS_MANUAL.md`.
5. Extend `_generate_matches` in `api/index.py` to merge static `JOB_LIBRARY` with live feeds (or replace entirely) while caching results in SQLite (`store_job_matches`).
6. Include telemetry (log provider, count, errors) for monitoring.

## 5. Testing & Verification
1. Unit tests using mocked provider responses (`tests/job_sources/test_greenhouse.py`).
2. CLI smoke scripts under `scripts/job_sources/` with sample commands, e.g.:
   ```bash
   scripts/job_sources/fetch_greenhouse.sh your_board_token
   scripts/job_sources/fetch_serpapi.sh "product manager"
   ```
3. Integration test: run `scripts/verify_deploy.sh` (extended) to ensure `/ob/opportunities` surfaces live data when credentials are present.
4. Record results in `CONVERSATION_NOTES.md` and update `ROLLING_CHECKLIST.md` gate once verified.

## 6. Community Signal Harvesting
- Approved APIs: Reddit (`/r/forhire`, `/r/remotejs`), Hacker News (“Who is hiring” threads via Algolia API), other forums with published APIs.
- Treat each community like a provider: document rate limits, required headers (User-Agent), query parameters, and moderation constraints.
- Normalize outputs to distinguish between formal listings and exploratory leads (`listing_type`: `formal`, `discussion`, `contract`, etc.).

## 7. Automation & Discovery Agent (Optional)
- Build a supervised script (`scripts/discover_job_feeds.py`) that queries known API directories and commits findings to `job_sources_catalog.md` with status `candidate`.
- Require human review for promotion to `approved` to stay compliant.
- Integrate with workflow bots (Netlify Agent Runner, ChatGPT agent) by pointing them to the catalog + this plan.

## 8. Handoff Notes for Runners/Agents
- Never add a source without verifying ToS and logging the decision in the catalog.
- Coordinate credential storage with the human gatekeeper; do not commit secrets.
- Update `NETLIFY_AGENT_RUNNER_README.md` when a new source or testing script is added.
- Any production deploy touching job feeds requires human approval (Gate E).

Keep this document current; update timestamps and sections when new sources or requirements are introduced.
