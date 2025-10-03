# Mosaic 2.0 Acceleration Plan (≤30 hrs, 2025-10-02)

This document captures CODEX’s implementation sequence, guardrails, and troubleshooting requirements for the Mosaic 2.0 sprint. Cursor (implementation) and Claude Code (deployment) must follow this plan and update artifacts as progress is made.

## 0. Scope & Entry Flow
- Preserve the coach-first funnel: discovery prompts → obstacle mapping → experiment setup → evidence capture → CV/identity integration.
- All new features ship behind flags so we can revert to the current MVP instantly.
- Update `CONVERSATION_NOTES.md` after every session to reflect feature toggles and validation state.

## 1. Phase Breakdown (hands-on hours)

### Phase 0 – Architecture & Run Sheet (CODEX, 2 hrs)
1. Freeze scope for this build (CSV→AI fallback, experiment engine, self-efficacy metrics, RAG baseline, coach escalation, job-feed groundwork, minimal UI).
2. Record dependencies and QA gates in `CONVERSATION_NOTES.md` and `ROLLING_CHECKLIST.md`.
3. Publish feature flag inventory (`feature_flags.json` or equivalent) with defaults (`false`).

### Phase 1 – Foundation & Guardrails (Cursor, 6 hrs)
1. Add migration framework (Alembic or scripted) plus backup/restore routine; dry run locally.
2. Implement CSV→AI fallback: introduce `api/prompt_selector.py`, `api/ai_clients.py`, env defaults, `AI_FALLBACK_ENABLED` flag; update tests and `scripts/verify_deploy.sh`.
3. Document fallback testing in `CONVERSATION_NOTES.md`.

### Phase 2 – Experiment Engine MVP (Cursor, 8 hrs)
1. Schema: add `experiments`, `learning_data`, `capability_evidence`, `self_efficacy_metrics` (with foreign keys, composite indexes).
2. APIs: `/experiments/create|update|complete`, `/learning/add`, `/evidence/capture`, `/metrics/self-efficacy`.
3. Storage helpers with transactional integrity; flag `EXPERIMENTS_ENABLED`.
4. Minimal UI elements toggled off by default; log manual tests.

### Phase 3 – Self-Efficacy Metrics & Escalation (Cursor, 6 hrs)
1. Compute experiment completion, learning velocity, confidence score; dual-log legacy metrics for comparison.
2. Schedule cleanup of stale experiments; write analytics entries per session.
3. Integrate coach escalation signal: surface prompt to contact Damian when repeated stalls/confidence drops.
4. Update UI (Focus Stack layout) to display new metrics; hide legacy meters under toggle until cutover.

### Phase 4 – RAG Baseline & Opportunity Signals (Cursor, 6 hrs)
1. Build embedding pipeline (OpenAI ADA) with batch caching, retries, rate limiting.
2. Retrieval wrapper with confidence threshold before AI fallback engages; maintain CSV fallback if retrieval fails.
3. Hook coach to include experiments/learning evidence in context.
4. Seed `docs/job_sources_catalog.md`; create `api/job_sources/` interface and prototype connector.
5. Populate opportunity cards with live data (even if limited sample).

### Phase 5 – Hardening & Deploy Prep (Cursor + Claude Code, 2 hrs)
1. Run `scripts/full_check.sh` (or equivalent) covering migrations, lint/tests, smoke tests.
2. Update `ROLLING_CHECKLIST.md` and `CONVERSATION_NOTES.md`; snapshot in `CONVERSATION_ARCHIVE`.
3. Prepare deploy brief for Claude Code; perform staging rollout + monitoring.
4. Human gatekeeper validates beta scenarios; schedule beta start.

## 2. Guardrails & Observability
- Feature flags tracked centrally; on-call can flip to revert features.
- Backend instrumentation: success/latency/error counters for new endpoints, RAG calls, and fallback path.
- Frontend shepherd: alert if coach discovery flow not completed.
- Folder drift: daily script comparing workspace layout against `PROJECT_STRUCTURE.md`.
- No deploy without migration rehearsal + backup success.
- Document every failure in `TROUBLESHOOTING_LOG` within 12 hrs.

## 3. Automation & Tooling
- `scripts/full_check.sh`: run `git status`, migrations, linters/tests, `scripts/verify_deploy.sh`; fail on any error.
- DB health script: verifies row counts, TTL cleanup, and foreign key integrity.
- Coach/RAG smoke script: checks CSV response, AI fallback, self-efficacy metrics.

## 4. Roles & Escalations
- Cursor: implementation + local tests; no production deploys.
- CODEX: planning oversight, approvals, run sheet updates.
- Claude Code: Railway/Netlify deploys, logs, rollback.
- Netlify Agent Runners: assist when approved; must read this plan first.
- Human gatekeeper (Damian): final approvals, secret management, testing feedback.

Escalation ladder: attempt fix → consult documentation → notify on-call → escalate to human if unresolved within timeboxes.

## 5. Deployment Checklist (Claude Code)
1. Confirm migrations + backups executed.
2. Deploy to staging, monitor logs for 30 mins.
3. Flip feature flags gradually (CSV AI fallback → experiments → metrics → RAG).
4. Validate coach funnel, experiments, opportunity cards, escalation prompts.
5. Update `CONVERSATION_NOTES.md` and notify human when production stable.

Keep this doc updated if scope changes. All agents must reference it before touching the Mosaic 2.0 build.
