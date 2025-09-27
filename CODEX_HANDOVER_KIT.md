# Codex Handover Kit (Master Spec)

**Working Rules**
- Output exact file diffs/content + a Run Sheet.
- zsh-safe, no heredocs, fail fast.
- Minimal changes; pause at Gates awaiting approval.

**Phases**
0) Protocol 0 (Secrets) → already included in repo; ensure CI secret scan is active.
1) Start cmd + health + CORS
2) Startup tripwire (provider key validation + ping)
3) `/config` endpoint
4) Prompts registry (hash/activate)
5) Pre-deploy sanity (+ optional Alembic if DB added)
6) Smoke tests & env scripts

**Deliverables**: PRs touching files listed in README. Stop at each Gate.

## Run Sheet (Quick)
- Env: ensure `OPENAI_API_KEY`, `CLAUDE_API_KEY`, `PUBLIC_API_BASE`, `PUBLIC_SITE_ORIGIN`, `APP_SCHEMA_VERSION` are set in Railway.
- Sanity: `./scripts/predeploy_sanity.sh` (checks deps, keys, optional prompts CSV).
- Deploy: Railway uses `gunicorn api.index:app` with `/health` healthcheck.
- Smoke: `./scripts/verify_deploy.sh "$PUBLIC_API_BASE"` checks `/health`, `/config`, `/prompts/active`.
- Prompts: validate `./scripts/check_prompts.sh data/prompts.csv`; ingest via `api/prompts_loader.ingest_prompts` (manual/admin).
