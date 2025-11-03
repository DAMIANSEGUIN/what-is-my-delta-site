# Protocol Enforcement Plan (2025-10-01)

This plan governs multi-agent collaboration. Follow these gates at every session; deviations require human approval.

## Session Start Checklist (All Agents)

1. `pwd` → confirm `/Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project`.
2. `git status --short` → ensure clean slate or list inherited diffs.
3. `git remote -v` → verify `origin` and `railway-origin` URLs.
4. Read: `CODEX_HANDOFF_*.md` (latest date), `CODEX_INSTRUCTIONS.md:1`, `ROLLING_CHECKLIST.md:1`, `PROJECT_STRUCTURE.md`, `AI_ROUTING_PLAN.md`, `JOB_FEED_DISCOVERY_PLAN.md`.
5. Append a brief session note in `CONVERSATION_NOTES.md` describing intended focus before making changes.

## Role Boundaries

- **CODEX (Planning)**: Produces analyses, specs, run sheets. Stops before touching implementation without explicit approval. Logs plans + open questions.
- **Claude in Cursor (Implementation)**: Executes approved run sheets, runs scripts/tests, manages git operations. Must not skip checklists or push absent approval.
- **Claude Code (Infrastructure)**: Investigates Railway, DNS, and deploy logs. Does not edit repo files.
- **Human (Gatekeeper)**: Approves deployments, environment mutations, cross-workspace moves, and role escalations.

## Handoff Triggers

- Planning complete → CODEX pauses and flags Claude in Cursor with run sheet.
- Local tests or filesystem ops required → Claude in Cursor takes over, reports results before releasing control.
- Deployment/log analysis or environment issues → Claude in Cursor requests Claude Code with exact context + log paths.
- Two consecutive failures or unclear state → Escalate to human with summary + blocking question.

## Gate System

- **Gate A (Workspace Validation)**: No edits until session checklist passes; abort if directory mismatch.
- **Gate B (Plan Approval)**: Implementation waits for human approval on CODEX plan/run sheet.
- **Gate C (Pre-Deploy)**: Run `scripts/predeploy_sanity.sh` and document result before any deploy action.
- **Gate D (Post-Change Logging)**: Record modifications/tests in `CONVERSATION_NOTES.md` and update `ROLLING_CHECKLIST.md` if steps close.
- **Gate E (Deployment Approval)**: Human must expressly approve Railway deploys, Netlify publishes, or remote pushes to `main`.

## Verification Procedures

- Before editing files: confirm target file exists in active workspace (`ls path`); if not, consult `PROJECT_STRUCTURE.md`.
- After code changes: run applicable scripts/tests (`scripts/verify_deploy.sh`, unit tests) and capture output summary.
- After ingesting prompts: ensure `data/prompts_registry.json` present; if absent, rerun ingestion or document fallback reliance.
- During merges/pulls: double-check remote names to avoid pushing to wrong repo; prefer `git remote show <name>` for sanity.

## Escalation Criteria

- Two failed attempts at the same command/test.
- Unknown files appearing outside documented structure.
- Suspected secret exposure (stop work, notify human immediately).
- Infrastructure anomalies (Railway deploy stuck, 5xx spikes, DNS drift).
- Any uncertainty about role boundaries or approvals.

## Enforcement

- Treat this plan as a blocking checklist. Agents who cannot satisfy a gate must stop, document the blocker, and wait for human direction.
- Human may revise these rules; commit updates after acknowledgement to keep this document authoritative.
