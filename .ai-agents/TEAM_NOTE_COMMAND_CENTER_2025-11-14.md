# Team Note — Command Center Backup & Release Controls  
**Date:** 2025-11-14  
**Author:** Codex (GPT-5 CLI)

## What Changed
- Documented the unified release/backup protocol (`docs/COMMAND_CENTER_BACKUP_PLAN.md`).
- Updated session start rules: every agent must read the latest release log, confirm the active `prod-YYYY-MM-DD` tag, and ensure a same-day site backup exists (see `.ai-agents/SESSION_START_PROTOCOL.md` Step 3).
- Deployment gate now auto-logs manual confirmations and blocks pushes if the working tree is dirty or the baseline mismatches.

## Current Artefacts
- Production tag: `prod-2025-11-12` @ commit `132c85012b230e2924363e4877c4aa2014191834`.
- Release log: `deploy_logs/2025-11-14_prod-2025-11-12.md`.
- Fallback bundle: `backups/prod-2025-11-12.zip`.
- Full site snapshot: `backups/site-backup_20251114_195930Z.zip`.

## Action Items for Agents
1. At session start, read the latest release log and note current prod tag in your kickoff message.
2. If no `/backups/site-backup_<today>.zip` exists, create one (temporary manual step; run `zip -r` until `scripts/archive_current_site.sh` lands) and log the filename.
3. Use `./scripts/run_deploy_gate.sh` before any deploy; archive the gate output and evidence in your handoff.
4. Post new deploys, append to `deploy_logs/` and tag the release before ending your session.

Future automation work (archive script, structured gate logs, Drive mirroring) is tracked in the plan—coordinate with Codex before implementing.***
