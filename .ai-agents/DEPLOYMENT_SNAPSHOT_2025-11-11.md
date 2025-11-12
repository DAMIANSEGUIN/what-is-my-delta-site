# Deployment Snapshot — 2025-11-11 (14:15 ET)

**Role:** Codex Terminal (Claude Code CLI counterpart)  
**Purpose:** Lock in the known-good chat/auth build delivered on the morning of 2025-11-11 so future sessions do not regress to the 5 Nov baseline.

---

## Current Production State

- **2025-11-12 Update — Chat session fix deployed**  
  - Commit `f13cba45a39262fc902b7783fa3a4a3ce8548867` (“fix: route coach chat via callJson”) is live on Netlify deploy `6914a51661dc38f3e806ff02`.  
  - `askCoach()` now uses `callJson()`, so `/wimd` requests carry the `X-Session-ID` header; chat no longer loops on Step 1.  
  - Console capture (`scripts/capture_console.mjs`, 2025-11-12 15:21Z) confirms `[COACH] Using knowledge base match …` followed by API response, and PS101 assets load (`Loaded 607 career coaching prompts + 8 PS101 framework questions`).  
  - Verification: `./scripts/verify_critical_features.sh`, Netlify wrapper checks, and live console capture all pass post-deploy.
- **2025-11-12 Update — PS101 navigation smoother**  
  - Commit `a2fffa3028d779b19ed6814dad02aeb20842ff58` (“ux: allow browsing PS101 prompts before answering”) deployed via Netlify `6914a9eeb1531804b7605f91`.  
  - Non-final PS101 prompts now allow “Next prompt” even when answers are short (user can preview all questions). Last prompts still enforce minimum detail before advancing to the next step.  
  - `validateCurrentStep()` now offers a confirmation dialog when skipping early prompts. Console capture (2025-11-12 15:39Z) confirms prompts load successfully after deploy.

- **Frontend (Netlify)**  
  - Deploy ID `691219f373c0da2b0ac61b6f` (built from commit `c9900f3` and subsequent UI hardening) is live.  
  - Chat strip responds, login CTA renders and opens the auth modal. Verified manually morning of 11 Nov.  
  - Recent stabilizers:
    - `8aeae464df73d33d622897cc2d9c46aac9818e56` — guard coach strip references until Phase 2.5 wiring completes.
    - `96dd6962d12033686df7511ac18f5e48d6dfa7b3` — remove legacy context payload so the coach API accepts requests.
    - `1065a91a079c0bbee388fb3d36e53a074d3c8bb6` — floating auth CTA for logged-out visitors.

- **Backend (Railway)**  
  - Latest commit on `main`: `623cbd51dba79f99fc212e40bd897a2cb799371a` (“support forced HTTPS fallback for Railway deploy”) — adds PAT fallback so pushes succeed without SSH.  
  - Prior commit `f19ba5537bea6a8bb71d157d1c36da5a3f3ffa55` normalizes auth emails + hardens reset endpoint.  
  - Railway rebuild completed today using the HTTPS fallback path; login + password reset tested OK immediately afterward.

---

## Required Follow-Up

1. **Backups**
   - Create a lightweight git tag and directory snapshot before any further edits:  
     ```bash
     cd ~/AI_Workspace/WIMD-Railway-Deploy-Project
     git tag -a snapshot-2025-11-11-chat-auth -m "Stable chat/auth build logged 2025-11-11"
     rsync -a --exclude '.git' ~/AI_Workspace/WIMD-Railway-Deploy-Project ~/Backups/WIMD-Railway-Deploy-Project_2025-11-11/
     ```
   - Push the tag to GitHub once validated: `git push origin snapshot-2025-11-11-chat-auth`.

2. **Session Discipline**
   - Every new CLI/Cursor session must read this note **before** referencing any older 5 Nov documents (e.g., `DEPLOYMENT_ACTION_PLAN_2025-11-07.md`).  
   - If an agent loads cached context that predates 11 Nov, explicitly discard it and reload from this snapshot plus `NOTE_FOR_CLAUDE_CODE_2025-11-09.md`.

3. **Regression Guard**
   - Keep `scripts/push.sh` in sync with the HTTPS fallback logic; do **not** revert to the SSH-only workflow.  
   - Verify `NETLIFY` deploy wrapper continues to leave the working tree clean (BUILD_ID stamping stays in the disposable copy).

---

## Verification Checklist (Completed 2025-11-11 ~13:45 ET)

- [x] `./scripts/verify_critical_features.sh`
- [x] `./scripts/verify_live_deployment.sh`
- [x] Browser smoke test (chat ask → response, auth CTA for logged-out user)
- [x] Railway rebuild log shows success (see `.verification_audit.log`, entries 2025-11-11 18:20–18:23 UTC)

---

**Next Agent Instruction:** Treat this snapshot as the authoritative baseline. Any future modifications must reference the commits above and update this file (or create a new dated snapshot) to prevent rollbacks to the pre-fix state.
