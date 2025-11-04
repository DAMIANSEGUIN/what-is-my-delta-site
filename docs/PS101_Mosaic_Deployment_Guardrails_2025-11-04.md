## Context

- **Date:** 2025-11-04  
- **Session:** PS101 Mosaic Deployment guardrail review  
- **Participants:** Damian, Codex, Claude_Code  
- **Objective:** Resolve production mismatch where Netlify served the legacy `frontend/` UI instead of the PS101 Mosaic UI.

## Root Cause Summary

- Root `netlify.toml` on GitHub still pointed to `base = "frontend"` / `publish = "."`.
- Mosaic UI fixes lived only in local commits (`c336607`, `3614131`, `b61f115`) that never reached GitHub because pushes failed.
- Netlify always reads configuration from GitHub, so auto-deploys continued to build the legacy assets despite local updates.

### UI Disparity Snapshot

- **Legacy build (`frontend/index.html@dce6d5c3`)**
  - ~1,450 lines; relies on static textareas and alert prompts.
  - No authentication modal, no PS101 state engine, limited API usage.
- **Mosaic build (`frontend/index.html@b61f115`)**
  - ~3,875 lines; includes auth/login/register/reset flows, PS101 stepper UI, experiment builders, persistence logic.
  - Adds `authModal`, `PS101State`, obstacle/action dashboards, and accessibility upgrades.
- If production lacks these mosaic elements, Netlify is deploying the legacy file.

## Implementation Guardrails — “Mosaic Deploy Safeguard”

> **Name:** Mosaic Deploy Safeguard (MDS)  
> **Invocation:** Mention “Apply Mosaic Deploy Safeguard” at session start to enforce these steps.

1. **Source Control Check**
   - `git status` must be clean before deployment.
   - Confirm target commits exist locally:  
     `git log --stat netlify.toml Procfile scripts/deploy_frontend_netlify.sh`
2. **Remote Sync Verification**
   - Ensure `origin` URL is reachable. If SSH fails, switch to HTTPS:  
     `git remote set-url origin https://github.com/DAMIANSEGUIN/wimd-railway-deploy.git`
   - Push with credentials: `git push origin main`
3. **Netlify Config Validation**
   - Repo root `netlify.toml` **must** contain:
     ```
     [build]
       base = "mosaic_ui"
       publish = "mosaic_ui"
     ```
   - Any change to deploy scripts must echo the chosen directory.
4. **Deployment Confirmation**
   - Netlify Deploys tab → “Clear cache and deploy site”.
   - Verify logs show `Publish directory: mosaic_ui`.
5. **Live Site Verification**
   - `curl https://whatismydelta.com/ | wc -l` → ~3875 lines.
   - `curl https://whatismydelta.com/ | rg "authModal"` to confirm auth modal presence.
   - Footer `<!-- BUILD_ID:... -->` must match `git rev-parse HEAD`.

These guardrails are now required checkpoints before declaring production ready.

## SSH Authentication Issue

- **Symptom:** `ssh: Could not resolve hostname github.com: -65563`
- **Impact:** Prevented pushes, leaving Netlify stuck on old configuration.
- **Resolution Options:**
  1. **Immediate:** Switch `origin` to HTTPS (`git remote set-url ...`) and push with PAT.
  2. **Long-Term:** Fix SSH setup (validate `~/.ssh/config`, add key to GitHub, ensure agent loaded).

Record which path was used; future sessions should either restore working SSH or default to HTTPS until resolved.

## Action Checklist

- [ ] Confirm Mosaic commits pushed to GitHub (`git log origin/main | head`).
- [ ] Trigger Netlify redeploy with cache clear.
- [ ] Validate production UI with guardrail checks.
- [ ] Document results in `.verification_audit.log`.
- [ ] Assign owner to restore SSH auth (optional but recommended).

## Notes for Next Sessions

- Reference this document when invoking “Mosaic Deploy Safeguard”.
- Keep Claude_Code focused on pushing config changes rather than only updating `BUILD_ID`.
- Update `.ai-agents/SESSION_START_PROTOCOL.md` to add a reminder about the guardrail invocation if needed.
