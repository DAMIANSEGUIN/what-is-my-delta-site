# Netlify Agent Runner Handoff (2025-10-01)

## 1. Workspace & Repos
- **Primary workspace**: `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project`
- **Git remotes**:
  - `origin` → `https://github.com/DAMIANSEGUIN/wimd-railway-deploy.git`
  - `railway-origin` → `https://github.com/DAMIANSEGUIN/what-is-my-delta-site.git`
- **Frontend deploy target**: Netlify site `resonant-crostata-90b706` (`whatismydelta.com`)
- **Backend deploy target**: Railway service `what-is-my-delta-site-production`

## 2. Directory Map (depth ≤ 2)
```
/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project
├── api/                     # FastAPI backend (see `api/index.py`)
│   └── prompts_loader.py    # CSV + registry ingestion
├── data/                    # Prompt datasets & runtime artifacts
│   ├── prompts.csv
│   ├── prompts_clean.csv
│   ├── prompts_fixed.csv
│   ├── prompts_f19c806ca62c.json
│   ├── prompts_6e488b26db77.json
│   └── prompts_registry.json (generated, not in git)
├── mosaic_ui/               # Static UI bundle
├── scripts/                 # Deployment and verification scripts
│   ├── deploy_frontend_netlify.sh
│   ├── predeploy_sanity.sh
│   ├── verify_deploy.sh
│   └── setup_domain.sh
├── netlify.toml             # Proxy rules (ensure deployed)
├── Procfile / railway.json  # Railway configuration
├── requirements.txt         # Backend deps (needs AI SDK additions)
├── AI_ROUTING_PLAN.md       # CSV → AI → metrics fallback spec
├── PROJECT_STRUCTURE.md     # Canonical layout + drift checks
├── PROTOCOL_ENFORCEMENT_PLAN.md
├── CONVERSATION_NOTES.md    # Running status log
└── CURSOR_CLAUDE_SYNC_README.md
```

## 3. Mandatory Reading Order
1. `PROTOCOL_ENFORCEMENT_PLAN.md`
2. `PROJECT_STRUCTURE.md`
3. `AI_ROUTING_PLAN.md`
4. `JOB_FEED_DISCOVERY_PLAN.md`
5. Latest `CODEX_HANDOFF_*.md`
6. `CONVERSATION_NOTES.md` (top section dated 2025-10-01)

## 4. Current Status Snapshot
- Prompts CSVs present; `/prompts/active` works locally.
- `_coach_reply` still uses CSV-only responses; AI fallback not implemented yet.
- Documentation updated to lock the CSV → AI → fallback contract.
- `data/prompts_registry.json` ignored by git; deployments currently rely on runtime regeneration.

## 5. Required Workstreams
### A. Chat Routing Upgrade (highest priority)
1. Implement selector + threshold logic per `AI_ROUTING_PLAN.md`.
2. Add AI client abstraction (OpenAI/Anthropic) and env toggles.
3. Update `requirements.txt`, `api/settings.py`, and ops docs.
4. Add unit tests + smoke checks (`scripts/verify_deploy.sh` extension).
5. Deploy behind `AI_FALLBACK_ENABLED` flag → verify `/wimd` path decisions.

### B. Prompts Registry Source Control
1. Decide whether to commit a sanitized `data/prompts_registry.json` (recommended).
2. If tracked, remove ignore rule and document regeneration procedure.

### C. Directory Hygiene
1. Confirm whether `.netlify/` and `mosaic_ui/mosaic_ui_extracted/` should remain.
2. Update `PROJECT_STRUCTURE.md` and `.gitignore` accordingly.

## 6. Netlify Runner Checklist
- [ ] Run session-start checklist from `PROTOCOL_ENFORCEMENT_PLAN.md` (pwd, git status, remotes, doc review).
- [ ] Sync with upstream (`git fetch origin`, etc.) before editing.
- [ ] Execute `scripts/predeploy_sanity.sh` prior to any deploy (Gate C).
- [ ] Log every significant action in `CONVERSATION_NOTES.md` and update `ROLLING_CHECKLIST.md` when gates close.
- [ ] Coordinate with human gatekeeper before pushing or deploying.

## 7. Contact & Escalation
- Implementation questions → follow `PROTOCOL_ENFORCEMENT_PLAN.md` (Claude in Cursor role).
- Infrastructure / Railway issues → escalate to Claude Code.
- Product requirements or missing artifacts → human gatekeeper (Damian Seguin).

Keep this document updated if scope or paths change so future runners inherit a consistent map.
### D. OpportunityBridge Data Expansion
1. Follow `JOB_FEED_DISCOVERY_PLAN.md` to populate `docs/job_sources_catalog.md` with approved job/data feeds.
2. Implement connectors under `api/job_sources/` and update `_generate_matches` to blend live data with local metrics.
3. Add smoke tests/scripts for each new feed and record findings in `CONVERSATION_NOTES.md`.
