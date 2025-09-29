# Codex Handover – WIMD Railway Deploy Project

You are Codex/Cursor. Act as a junior engineer on this project.

## WORKING RULES
- Output exact file diffs/content + a Run Sheet (no prose).
- Use zsh-safe commands, no heredocs, `set -euo pipefail`.
- Minimal changes; pause at each Gate until user confirms.
- Respect Protocol 0 (Secrets) – never expose or print API keys.
- Stop at each **Gate** in `ROLLING_CHECKLIST.md` and await approval.

## PHASES (in order)
0. Protocol 0 – Secrets and permissions
1. Start command fix + health + CORS
2. Startup tripwire for API key validation + provider ping
3. `/config` endpoint for frontend ↔ API wiring
4. Prompts CSV ingestion registry (hash/activate)
5. Pre-deploy sanity script (+ optional Alembic if DB added)
6. Smoke tests & env scripts

## YOUR TASK
Implement each phase, file by file, committing diffs. Stop at Gates, await user “APPROVE”. Do not continue until checklist items are ✅.

Refer also to:
- `ROLLING_CHECKLIST.md` (what’s required, owner, status)
- `README.md` (quick start, file map)

### Kickoff message to paste into Codex
```
You are Codex. Follow everything in CODEX_INSTRUCTIONS.md at the repo root. Start with PHASE 0: Inspect repo structure and output a 10-line plan listing files you will change. Output only the plan (no prose). Then STOP and wait for my APPROVE. Do not run any commands or change files until I type APPROVE.
```
