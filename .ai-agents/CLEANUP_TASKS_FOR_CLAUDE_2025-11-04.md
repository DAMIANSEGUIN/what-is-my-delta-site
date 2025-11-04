# Cleanup Tasks – PS101 BUILD_ID Integration

**Prepared by:** Codex  
**Date:** 2025-11-04  
**Audience:** Claude_Code (primary), Cursor (verification)

---

## 1. Current Workspace Snapshot
- `git status` shows staged/unstaged work across deployment scripts, UI HTML, protocol docs, and new review notes.
- Pre-push hook blocks because the tree is dirty and the PS101 UI deltas are not yet committed.
- `scripts/pre_push_verification.sh` otherwise passes (auth + PS101 checks) and the BUILD_ID helper scripts succeeded during the pipeline test.

---

## 2. Files to Keep & Commit
Group these into a single commit titled **“INTEGRATE: PS101 BUILD_ID continuity gate”** once you finish the checks.

| File | Purpose | Notes |
| --- | --- | --- |
| `scripts/deploy.sh` | Injects `BUILD_ID`/`SPEC_SHA` before verification | Already tested end-to-end |
| `frontend/index.html`, `mosaic_ui/index.html` | Footer comment now includes `BUILD_ID:<commit>|SHA:<manifest>` | Confirm both footers match `manifest.can.json` (`check_spec_hash.sh`) |
| `.ai-agents/SESSION_START_PROTOCOL.md` | Operating rules updated with documentation discipline and PS101 Step 2b | Cursor will sanity-check lines 105-172 |
| `DEPLOYMENT_CHECKLIST.md` | Adds PS101 helper script step + documentation logging requirements | Cursor to re-review lines 32-87 |
| `.ai-agents/PS101_PROTOCOL_ACKNOWLEDGMENT_*` | Agent compliance receipts | Keep both Cursor + Claude variants |
| `.ai-agents/CURSOR_REVIEW_PS101_BUILD_ID_INTEGRATION_2025-11-04.md` | Review evidence | Already linked from team note |
| `NOTE_FOR_TEAM_REVIEW_PS101_BUILD_ID.md`, `TEAM_REVIEW_NOTE_PS101_BUILD_ID_INTEGRATION_2025-11-04.md`, `SHORT_NOTE_DOCUMENTATION_DISCIPLINE.md` | Reviewer & leadership summaries | Leave paths intact for sharing |
| `.ai-agents/CURSOR_REVIEW_DOCUMENTATION_DISCIPLINE_CHANGES_2025-11-04.md`, `.ai-agents/CURSOR_ACKNOWLEDGMENT_DOCUMENTATION_DISCIPLINE_2025-11-04.md` | Cursor’s acknowledgement of new documentation rules | Needed for audit trail |
| `Mosaic/PS101_Continuity_Kit/**` | Canonical manifest + helper scripts | Ensure directory is added recursively (`git add Mosaic/PS101_Continuity_Kit`) |

Check the Markdown notes for typos, then `git add` each file.

---

## 3. Files to Normalize (No Real Content Change)
The following markdown files only picked up a trailing blank line. Reset them unless you intend to make substantive edits:
- `docs/AUTH_MERGE_EXECUTION_2025-11-03.md`
- `docs/CURSOR_UI_BUG_REPORT_2025-11-03.md`
- `docs/NETLIFY_AGENT_URGENT_DEPLOYMENT_FIX.md`

Command:
```bash
git checkout -- docs/AUTH_MERGE_EXECUTION_2025-11-03.md \
  docs/CURSOR_UI_BUG_REPORT_2025-11-03.md \
  docs/NETLIFY_AGENT_URGENT_DEPLOYMENT_FIX.md
```

---

## 4. Deployment Queue Docs
New files that describe the push backlog (`DEPLOYMENT_READY_FOR_PUSH.md`, `PUSH_REQUIRED_SUMMARY.md`, `READY_TO_PUSH.txt`, `URGENT_TEAM_HANDOFF.md`):
- Skim for accuracy (dates, responsible parties).
- If still relevant, keep and `git add` them; otherwise archive outside repo before continuing.

---

## 5. Commit Flow
1. Run the normalization command (Section 3).
2. Re-run `git status` and ensure only intentional files remain.
3. Stage everything listed in Sections 2 + 4 (and any additional notes you choose to keep):
   ```bash
   git add scripts/deploy.sh frontend/index.html mosaic_ui/index.html \
     .ai-agents/SESSION_START_PROTOCOL.md DEPLOYMENT_CHECKLIST.md \
     .ai-agents/PS101_PROTOCOL_ACKNOWLEDGMENT_* \
     .ai-agents/CURSOR_REVIEW_PS101_BUILD_ID_INTEGRATION_2025-11-04.md \
     .ai-agents/CURSOR_REVIEW_DOCUMENTATION_DISCIPLINE_CHANGES_2025-11-04.md \
     .ai-agents/CURSOR_ACKNOWLEDGMENT_DOCUMENTATION_DISCIPLINE_2025-11-04.md \
     NOTE_FOR_TEAM_REVIEW_PS101_BUILD_ID.md \
     TEAM_REVIEW_NOTE_PS101_BUILD_ID_INTEGRATION_2025-11-04.md \
     SHORT_NOTE_DOCUMENTATION_DISCIPLINE.md \
     DEPLOYMENT_READY_FOR_PUSH.md PUSH_REQUIRED_SUMMARY.md READY_TO_PUSH.txt \
     URGENT_TEAM_HANDOFF.md Mosaic/PS101_Continuity_Kit
   ```
   (Adjust if any docs are archived.)
4. Commit with:
   ```bash
   git commit -m "INTEGRATE: PS101 BUILD_ID continuity gate"
   ```
5. Re-run `./scripts/pre_push_verification.sh`. It should now pass through the git-clean gate.
6. Capture outputs in `.verification_audit.log`, then ping Cursor for a quick final confirmation.

---

## 6. Post-Commit Steps
- Once verification passes, prep for the eventual push (`./scripts/push.sh railway-origin main`) when approved.
- Update `NOTE_FOR_CURSOR_AND_CLAUDE_CODE_2025-10-27.md` with the commit hash and BUILD_ID so the enforcement log stays current.
- Notify Codex when the tree is clean; we’ll schedule the deployment dry-run.

---

**Ping if any of the instructions conflict with a local policy or if unexpected diffs remain after normalization.**
