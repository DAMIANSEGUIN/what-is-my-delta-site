# Codex Restart Context Checklist

Use this checklist whenever you restart the Codex CLI session. Capture the answers and paste them at the top of the new conversation so Codex can immediately regain context.

## 1. Git State
- Output of `git status --short`
- Output of `git log -3 --oneline`

## 2. Deployment Baseline
- Contents of `deployment/deploy_baseline.env`
- Current production tag (e.g., `prod-YYYY-MM-DD`) and whether production matches it

## 3. Verification Snapshot
- Latest entries from `.verification_audit.log` (tail 20 lines)
- Path to most recent `BASELINE_SNAPSHOT_*.md` file covering today’s work

## 4. Current Objective
- One or two sentences on the active goal (e.g., “reconstruct working chat/auth build after Nov 12 fixes”)
- Known blockers or open questions

## 5. Evidence Links
- Paths or URLs for the latest browser walkthrough/screenshots proving the live site state
- Any documents that should be reviewed first (e.g., DOM timing reports, team notes)

Paste this bundle when you open a new session. It gives Codex everything needed to pick up the project without re‑investigating prior conversation.
