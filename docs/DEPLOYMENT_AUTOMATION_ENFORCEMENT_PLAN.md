# Deployment Automation Enforcement Plan

## Context
- Repeated failures to follow deployment protocols have led to regressions and outages.
- Manual compliance has proven unreliable; we need automated, enforced guardrails.
- This plan integrates feedback from Cursor’s review and Codex recommendations.

## Objectives
- Block any production push or deploy that has not passed verification.
- Ensure every agent uses consistent tooling (`scripts/` wrappers) rather than raw commands.
- Provide auditable bypass options for true emergencies.
- Align local safeguards with eventual CI/branch protection controls.

## Enforcement Layers
1. **Git Pre-Push Hook (railway-origin)**
   - Location: `.githooks/pre-push` (tracked)
   - Runs `scripts/pre_push_verification.sh`; blocks push on non-zero exit.
   - Detects target remote; only enforces for `railway-origin` (production backend).
   - Records bypasses when `SKIP_VERIFICATION=true` is set (append to `.verification_audit.log`).
   - Bootstrap: run `./scripts/setup_hooks.sh` (or `git config core.hooksPath .githooks`) after cloning.

2. **Verification Scripts**
   - `scripts/pre_push_verification.sh`: wraps health + content checks, returns exit codes (no token files).
   - `scripts/verify_live_deployment.sh`: callable by both pre-push and post-deploy tasks; includes retry/backoff guidance.
   - Shared configuration for staging vs production URLs via env vars.

3. **Wrapper Commands**
   - `scripts/deploy.sh <railway|netlify|all>`: orchestrates pre-check, deploy, wait, post-verify, and reports status.
   - `scripts/push.sh <remote> [branch]`: invokes `pre_push_verification.sh` before delegating to `git push`.
   - Both scripts log bypass usage and surface next steps clearly on failure.

4. **Documentation & Training**
   - Update `SESSION_START_README.md`, `DEPLOYMENT_CHECKLIST.md`, and `CLAUDE.md` with “no raw git/netlify deploy” rule.
   - Provide troubleshooting guidance for verification failures and bypass protocol.

5. **CI/Branch Protection Follow-Up**
   - Protect `main` (or production) branch; require GitHub Action status checks before merge.
   - Later phase: GitHub Actions workflow that mirrors the local verification, deploys, verifies, and (if needed) rolls back via Netlify/Railway APIs.

## Roles & Handoffs
- **Implementation Lead**: Claude_Code (terminal-focused deployment agent).
- **Pre-Deployment Reviewer**: Cursor (confirm script logic + docs before enabling).
- **Post-Implementation Auditor**: Codex (validate enforcement in practice, ensure no bypass gaps).

## Execution Order
1. Implement and test the pre-push hook + verification script adjustments.
2. Add wrapper scripts and ensure they are executable; document usage.
3. Refresh deployment-related documentation and training notes.
4. Configure branch protections / required status checks (coordinate with repository admins).
5. Draft GitHub Actions workflow (can be activated once secrets + rollback path are confirmed).

## Testing Checklist
- Attempt `git push railway-origin main` without running verification → expect block.
- Run `scripts/pre_push_verification.sh`, reattempt push within allowed window → expect success.
- Run `scripts/deploy.sh railway` and `scripts/deploy.sh netlify` in dry-run mode to validate flow.
- Trigger bypass (`SKIP_VERIFICATION=true git push …`) → confirm log entry and warning output.
- Cursor to review diff + docs; Claude_Code to confirm hook installation across environments.

## Open Questions
- Final convention for staging vs production URLs and check manifests.
- Desired retention/rotation policy for `.verification_audit.log`.
- Timeline for enforcing GitHub branch protection and CI gating.

## Next Steps
1. Claude_Code: implement layers 1–3 and push branch for review.
2. Cursor: review the branch, confirm readiness, and sign off.
3. Team: align on CI/branch protection timeline, then follow up with automation phase.
