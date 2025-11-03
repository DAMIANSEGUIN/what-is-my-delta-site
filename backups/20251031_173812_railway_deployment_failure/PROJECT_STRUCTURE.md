# Project Structure (2025-10-01)

This document is the single source of truth for where assets live, how they map to remotes, and who can operate on them. Update it whenever directories move or deployment targets change.

## Workspaces & Remotes

| Path | Role | Git Remote | Notes |
| --- | --- | --- | --- |
| `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project` | Active workspace, deployment source | `origin` → `wimd-railway-deploy` | Accessible to all agents; use this tree for production edits. See `AI_ROUTING_PLAN.md` for chat flow contract. |
| `/Users/damianseguin/projects/mosaic-platform` | Consolidated archive | n/a | Claimed canonical in prior audit but **not** sandbox-accessible; mirror any updates back into Downloads workspace before work continues. |
| Railway service repo | `railway-origin` → `what-is-my-delta-site` | Mirror of backend used by Railway deploy | Keep branches aligned with active workspace; do not push unrelated assets here. |

## Deployment Targets

- **Railway Backend**: https://what-is-my-delta-site-production.up.railway.app (branch `main`, repo `railway-origin`).
- **Netlify Frontend**: Site `resonant-crostata-90b706`, proxying to Railway; repo `origin` (Netlify deploy integration).

## Canonical Directory Layout (Depth ≤ 2)

```
├── api/                 # FastAPI backend, entry point `api/index.py`
│   ├── prompts_loader.py
│   ├── settings.py
│   └── ... (service modules)
├── data/
│   ├── prompts_clean.csv
│   ├── prompts_fixed.csv
│   ├── prompts_f19c806ca62c.json
│   ├── prompts_6e488b26db77.json
│   └── prompts_registry.json (generated; see Notes)
├── scripts/
│   ├── deploy_frontend_netlify.sh
│   ├── one_shot_new_deploy.sh
│   ├── predeploy_sanity.sh
│   ├── setup_domain.sh
│   └── verify_deploy.sh
├── mosaic_ui/
│   └── index.html (static UI bundle; ensure sync with active backend)
├── docs (root markdown files)
│   ├── CODEX_*.md (handoffs, protocols)
│   ├── ROLLING_CHECKLIST.md (gated tasks)
│   ├── SESSION_TROUBLESHOOTING_LOG.md
│   ├── OPERATIONS_MANUAL.md
│   ├── AI_ROUTING_PLAN.md (CSV → AI → fallback spec)
│   ├── JOB_FEED_DISCOVERY_PLAN.md (OpportunityBridge sourcing workflow)
│   └── NETLIFY_AGENT_RUNNER_README.md (handoff instructions)
├── Procfile / railway.json (Railway configuration)
├── netlify.toml (Netlify proxy rules)
└── requirements.txt (Backend dependencies)
```

## Data & Registry Notes

- `data/prompts_registry.json` **must exist** in deployments. It is currently generated locally and ignored by git; if absent, the backend now derives the active SHA from CSV/JSON artifacts but still logs a warning in `CONVERSATION_NOTES.md`. Prefer checking this file into source control after sanitising (no secrets inside) or storing a seeded copy for deployments.
- CSV sources: `prompts.csv` is canonical ingestion input. `prompts_clean.csv`/`prompts_fixed.csv` are derived cleanup views; regenerate them from the canonical file when prompts change.
- SQLite file `data/mosaic.db` is runtime state; never commit it upstream.

## Ownership & Access

- **CODEX**: Read/plan only. Must not modify files without explicit plan approval. Works entirely within the Downloads workspace.
- **Claude in Cursor**: Implementation agent with full file write + git access. Responsible for running scripts/tests locally.
- **Claude Code**: Infrastructure/logs only; engages when deployments or Railway debugging is needed.
- **Human**: Gatekeeper. Approves deployments, provides secrets, mirrors resource audit artifacts into this workspace.

## Drift Detection Checklist

1. Run `pwd`, confirm `.../Downloads/WIMD-Railway-Deploy-Project`.
2. Run `git status --short`; any untracked direct subdirectories indicate drift.
3. Validate `tree -L 2` (or compare against layout above) before starting work.
4. Ensure both `origin` and `railway-origin` remotes are present and pointing to expected URLs (`git remote -v`).
5. Confirm `data/prompts_registry.json` exists locally before deploy; regenerate with `python -c 'from api.prompts_loader import ingest_prompts; ingest_prompts("data/prompts_clean.csv")'` if missing.

Update this document whenever directories move, new deploy targets appear, or agent access changes. Treat it as the pre-flight reference for every session.
