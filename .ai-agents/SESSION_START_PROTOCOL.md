# AI Agent Session Start Protocol

**MANDATORY: Every AI agent MUST run this at session start**

> Codex Reset Protocol → When invoked, re-run Steps 1–5 below.  
> Restate Present State → Desired Outcome, and re-log the session.

## Step 1: Identify Yourself (FIRST MESSAGE)

```
I am [AGENT_NAME] starting session at [TIMESTAMP]

Running session start protocol...
```

## Step 2: Run Critical Feature Verification

**BEFORE reading any other files or taking any actions:**

```bash
./scripts/verify_critical_features.sh
```

**Expected output:**
```
✅ Authentication UI present
✅ PS101 flow present
✅ API_BASE configured correctly
✅ All critical features verified
```

**If verification FAILS:**
- ❌ STOP immediately
- Do NOT proceed with any tasks
- Report to human: "Critical feature missing - verification failed"
- Wait for human to resolve before proceeding

## Step 2b: Confirm PS101 Continuity Kit Alignment

**Mandatory for Cursor and Claude_Code before continuing:**

1. Review the quick-start in `Mosaic/PS101_Continuity_Kit/README_NOTE_FOR_BUILD_TEAM.md` so the current manifest expectations are top of mind.
2. Run the hash check to confirm the working tree matches the canonical spec bundle:
   ```bash
   ./Mosaic/PS101_Continuity_Kit/check_spec_hash.sh
   ```
3. If the script reports drift, stop immediately, document the variance, and escalate for resolution before making further changes.
4. When preparing a deploy or reviewing a handoff, ensure the footer `BUILD_ID` rendered in the UI matches the value defined by `inject_build_id.js` and recorded in `manifest.can.json`.

## Step 3: Check for Handoff

**Look for handoff manifest:**

```bash
ls -t .ai-agents/handoff_*.json | head -1
```

**If handoff file exists:**
- Read the handoff manifest
- Verify outgoing agent completed checklist
- Acknowledge all critical features listed
- Log handoff receipt in `.ai-agents/handoff_log.txt`

**If NO handoff file (fresh session):**
- Create session start marker:
  ```bash
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Session start: [AGENT_NAME]" >> .ai-agents/session_log.txt
  ```

## Step 4: Review Recent Activity

**Check last 5 commits:**
```bash
git log -5 --oneline
```

**Check for urgent files:**
```bash
ls -1 URGENT_* FOR_*_AGENT*.md 2>/dev/null
```

**If urgent files exist:**
- Read them BEFORE proceeding with other tasks
- These files contain critical information from previous sessions

**Scan shared Stage/Team notes:**
```bash
ls -1t .ai-agents/STAGE*.md .ai-agents/TEAM_NOTE_*.md 2>/dev/null | head
```
- Re-read any document updated since your last session (compare timestamps or `git diff --stat HEAD@{1}`).
- Update the relevant Stage file with an acknowledgment line (e.g., `Cursor Acknowledged: ✅`) before moving on.

## Step 5: Declare Readiness

**Only after completing steps 1-4, declare:**

```
✅ Session start protocol complete
✅ Critical features verified
✅ [Handoff received / Fresh session]
✅ Recent activity reviewed

Ready to proceed with tasks.

Current critical features confirmed:
- Authentication: [PRESENT/MISSING]
- PS101 v2: [PRESENT/MISSING]
- API Integration: [CONFIGURED/NEEDS-ATTENTION]
```

## Step 6: Operating Rules

**Throughout this session, I will:**

1. ✅ Run `./scripts/verify_critical_features.sh` BEFORE any deployment
2. ✅ Never remove authentication without explicit approval
3. ✅ Never replace files without checking for feature loss
4. ✅ Follow pre-commit hooks (never use --no-verify without approval)
5. ✅ Run DEPLOYMENT_VERIFICATION_CHECKLIST.md after deploys
6. ✅ Create handoff manifest before ending session if requested
7. ✅ Confirm the PS101 manifest/footer alignment before approving a review or initiating a deploy; log any intentional variances in `.verification_audit.log`.
8. ✅ Update all impacted documentation (notes, checklists, manifests) before declaring a task complete; summarize changes in the relevant handoff or audit log.
9. ✅ **NEVER use raw `git push` or `netlify deploy` commands - use wrapper scripts:**
   - Use `./scripts/push.sh railway-origin main` instead of `git push railway-origin main`
   - Use `./scripts/deploy.sh netlify` instead of `netlify deploy --prod`
   - Use `./scripts/deploy.sh railway` to deploy backend
   - Use `./scripts/deploy.sh all` to deploy both frontend and backend

**If I fail to follow these rules:**
- Pre-commit hook will BLOCK the commit
- Human will be notified of violation
- Session may be terminated and handed off to another agent

## Emergency Override

**Only use with explicit human approval:**

If human says "EMERGENCY OVERRIDE: [reason]", I may bypass verification ONCE, but must:
1. Document override reason in commit message
2. Add tag: [EMERGENCY-OVERRIDE]
3. Run full verification immediately after override action
4. Create recovery plan if verification fails

## Session End Protocol

**Before ending session (if requested):**

```bash
./scripts/create_handoff_manifest.sh > .ai-agents/handoff_$(date +%Y%m%d_%H%M%S).json
```

**Declare session end:**
```
Session ending. Handoff manifest created.
Next agent should read: .ai-agents/handoff_[TIMESTAMP].json
```

---

## Quick Reference Card

**Session Start Checklist:**
```
□ Identify self
□ Run ./scripts/verify_critical_features.sh
□ Run PS101 continuity hash check
□ Check for handoff manifest
□ Review recent commits
□ Read urgent files
□ Declare readiness
□ Begin work
```

**Before Every Deploy:**
```
□ Run ./scripts/verify_critical_features.sh
□ Confirm manifest.can.json + footer BUILD_ID alignment
□ Verify no critical features removed
□ Follow deployment checklist
□ Monitor post-deploy for 5 minutes
□ Update documentation + audit log entries
```

**Before Session End:**
```
□ Run ./scripts/create_handoff_manifest.sh
□ Commit or document WIP
□ Create handoff file
□ Log session end
```
