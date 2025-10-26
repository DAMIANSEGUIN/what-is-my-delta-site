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
