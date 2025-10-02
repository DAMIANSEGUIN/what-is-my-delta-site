# Conversation Archive — 2025-10-01

This snapshot captures the key threads from the session between Damian Seguin and CODEX on 2025-10-01. Use it if future context resets or agents need to replay the plan after a crash/drift.

## Prompts & CSV Handling
- `/prompts/active` null issue traced to missing `data/prompts_registry.json` on deploy; fallback added in `api/prompts_loader.py`.
- Registry now derived from CSV/JSON artifacts when absent; canonical source is `data/prompts.csv` with derived `prompts_clean.csv` and `prompts_fixed.csv`.
- Outstanding decision: whether to commit a sanitized `prompts_registry.json` or regenerate at deploy time.

## Protocol & Structure Updates
- `PROJECT_STRUCTURE.md`: now authoritative workspace layout; links to routing and job-feed plans.
- `PROTOCOL_ENFORCEMENT_PLAN.md`: session start checklist, gates A–E, documentation requirements.
- `CURSOR_CLAUDE_SYNC_README.md`, `NETLIFY_AGENT_RUNNER_README.md`: handoffs for internal/external agents.
- `AI_ROUTING_PLAN.md`: defines CSV → AI → metrics fallback for coach responses.
- `JOB_FEED_DISCOVERY_PLAN.md`: runbook for sourcing live OpportunityBridge data.
- `NETLIFY_AGENT_RUNNER_README.md`: instructions for Netlify agents, including routing upgrade and job-feed expansion.

## OpportunityBridge State & Next Steps
- Backend endpoints (`/ob/*`, `/resume/*`) fully implemented; currently powered by static `JOB_LIBRARY`.
- Plan: integrate real job feeds via documented workflow, normalize results, and expose MOSAIC signals.
- UI redesign: simplify to “Focus Stack” layout (chat + metrics, opportunity snapshot, action ledger) while keeping deeper tools accessible on demand.

## OSINT / Job Intelligence Prompts
- Two MOSAIC-aligned prompt templates defined for company/job seekers; focus on discovery, signal extraction, skeptical analysis, and receipts table.
- Special case for Kyle Matuzewski / Bau-Xi Gallery documented; future agents to gather gallery-specific insights.
- Prompts to be embedded in `JOB_FEED_DISCOVERY_PLAN.md` for consistent execution.

## Search & Integration Workflow
- No universal job API; workflow mandates curated source catalog (`docs/job_sources_catalog.md`) tracking auth, ToS, status.
- Connectors to reside in `api/job_sources/` with shared schema and logging.
- Discovery agents/scripts should poll API directories, log candidates, and require human approval before integration.

## UI Prototype Snippet
- Minimal HTML prototype provided (Focus Stack layout) with chat, metrics, opportunity cards, action ledger.
- Goal: maintain simple aesthetic, reveal advanced features only when user signals need.

## Actions Delegated to Netlify Agent Runners (NARs)
1. Implement CSV → AI fallback per `AI_ROUTING_PLAN.md` (feature gated, tests required).
2. Build job-feed connectors following `JOB_FEED_DISCOVERY_PLAN.md`; populate catalog.
3. Assess prompts registry source control; document outcome.
4. Cleanup workspace artifacts (`.netlify/`, `mosaic_ui/mosaic_ui_extracted/`) per policy.
5. Coordinate UI simplification using provided HTML sketch.

## Open Questions / Pending Decisions
- Whether `prompts_registry.json` becomes a tracked artifact.
- Which job feeds to prioritize and what legal permissions are required.
- Final UI direction (Focus Stack vs. Toggle Deck vs. Split Hero) once feedback received.
- Timing for integrating MOSAIC prompt templates into automated reports.

Keep this archive with the repo documentation so future sessions can reload context instantly if systems reset.
