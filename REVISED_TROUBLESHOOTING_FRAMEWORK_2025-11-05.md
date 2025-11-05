# REVISED TROUBLESHOOTING FRAMEWORK (2025-11-05)
**Author:** Codex (Planning)  
**Purpose:** Integrate the structured troubleshooting proposal with existing enforcement systems while we work the current production outage.

---

## 0. SESSION INITIALIZATION (MANDATORY GATE)

Before any troubleshooting stage:

1. Execute `.ai-agents/SESSION_START_PROTOCOL.md` completely.  
2. Log compliance in `.ai-agents/session_log.txt`.  
3. Run `./scripts/verify_critical_features.sh` and confirm PS101 continuity via `./Mosaic/PS101_Continuity_Kit/check_spec_hash.sh`.  
4. If any check fails, stop and resolve prior to Stage 1.

Only proceed when Stage 0 is complete. This preserves the enforced startup protocol and replaces the implicit assumption in the original proposal.

---

## 1. CURRENT STATE → DESIRED OUTCOME

- Capture measurable symptoms, affected URLs, console/network evidence.  
- Define the Desired Outcome and how it will be verified (acceptance criteria + scripts).  
- Confirm timeline/urgency and responsible agents.  
- Record in `.ai-agents/templates/STAGE_1_TEMPLATE.md` (once created) or the active incident note.

Oversight: Codex signs off that the scope and Desired Outcome match user goals before Stage 2.

---

## 2. CHAIN-OF-VERIFICATION DIAGNOSIS

- Draft initial root-cause hypothesis.  
- Enumerate at least three ways the hypothesis could be wrong, citing evidence required to refute/confirm.  
- Update the diagnosis after collecting that evidence.  
- Log artifacts (DevTools captures, logs, script output) in the incident note.

Oversight: Codex reviews and approves the revised diagnosis prior to Stage 3.

---

## 3. STRUCTURED ANALYSIS

Follow the zero-shot analysis scaffold:

1. **Scope:** Layer(s) and components involved.  
2. **Variables:** What works, what fails, and unknowns.  
3. **Relationships:** Interactions and dependencies.  
4. **Edge Cases:** Browser, network, state variants.  
5. **Synthesis:** Evidence-backed root cause with falsifiable test.

Document counter-evidence that would invalidate the synthesis. Codex validates the reasoning chain before Stage 4.

---

## 4. SOLUTION SYNTHESIS (MULTI-PERSONA DEBATE)

- Draft solution options; run the Deployment Engineer vs QA vs End User perspectives.  
- Capture trade-offs, rollback plans, and monitoring commitments.  
- Select preferred option with rationale and required approvals.

Codex grants the Stage 4 “Proceed” checkpoint once risks and trade-offs are addressed.

---

## 5. IMPLEMENTATION WITH INTEGRATED CHECKPOINTS

Implementation must respect existing safeguards:

1. **Checkpoint A – Rapid Validator (new):**  
   - Run `.ai-agents/checkpoint_validator.sh` (to be built) after each significant change for syntax and critical-signal smoke tests.  
   - If it fails, fix forward; do not proceed.

2. **Checkpoint B – Pre-Commit Hooks (existing):**  
   - Triggered automatically on commit. Never bypass with `--no-verify`. Address hook feedback immediately.

3. **Checkpoint C – Pre-Push Verification (existing):**  
   ```bash
   ./scripts/pre_push_verification.sh
   ```  
   - Confirms line-count baseline, feature signatures, PS101 alignment reference, and clean git status.

4. **PS101 Continuity Enforcement:**  
   - Run `./Mosaic/PS101_Continuity_Kit/check_spec_hash.sh`.  
   - Confirm footer `BUILD_ID` matches `manifest.can.json` via `scripts/inject_build_id.js` before any deployment.

5. **Rollback Discipline:**  
   - Use non-destructive recovery (`git stash push`, `git checkout -- .`, dedicated helper scripts).  
   - Any destructive commands (e.g., `git reset --hard`) require explicit human approval and are **not** part of the default framework.

Codex acknowledges checkpoint results; failures trigger a fix-forward loop within Stage 5.

---

## 6. VERIFICATION & DOCUMENTATION

Automated verification sequence:

```bash
./scripts/verify_critical_features.sh
./scripts/verify_live_deployment.sh https://whatismydelta.com/
./scripts/regression_tests.sh    # placeholder until implemented
```

Manual confirmation:

- Authentication modal reachable without blocking usage.  
- Trial mode initializes and completes console log sequence.  
- Chat/primary CTAs functional in supported browsers.  
- Any incident-specific acceptance criteria met.

Documentation and audit requirements:

- Update `CLAUDE.md`, `.verification_audit.log`, and relevant incident notes.  
- Record evidence (screenshots, logs, script outputs).  
- If deployment occurred, complete `DEPLOYMENT_VERIFICATION_CHECKLIST.md`.

Stage 6 closes only when all verification steps pass and documentation is logged.

---

## APPROVAL & COMMUNICATION MODEL

- **Oversight Checkpoints:** Codex approvals required after Stage 1, Stage 2, Stage 4, and when any checkpoint fails. These remain mandatory.  
- **Batched User Approvals:** Session-level “plan bundles” may still be used to minimize human tokens, but they cannot replace Codex oversight gates.  
- **Escalation Rules:** Any catastrophic-risk action (data loss, auth removal, schema change) or framework deviation requires immediate human approval, outside the batched flow.

Status updates should use the compact format (`✅`, `⚠️`, `→ Next`) to preserve clarity and token efficiency.

---

## AUTOMATION ROADMAP

| Artifact | Owner | Purpose | Notes |
| --- | --- | --- | --- |
| `.ai-agents/checkpoint_validator.sh` | Cursor | Fast lint/feature smoke test | Subset of pre-push checks; fails fast. |
| `scripts/verify_documentation_discipline.sh` | Cursor | Enforce Operating Rule #8 | Ensures required files updated. |
| `scripts/regression_tests.sh` | Cursor + NARs | Baseline UX regression suite | Initial version can wrap existing smoke tests. |
| `.ai-agents/templates/STAGE_1_TEMPLATE.md` | Codex | Structured Stage 1 capture | Supports consistent Current/Desired logging. |
| `.ai-agents/templates/RETROSPECTIVE_TEMPLATE.md` | Codex | Post-incident review | Optional; aligns with analysis recommendations. |

Assignments can shift, but owners must be recorded in the situational report.

---

## ADOPTION PLAN

1. **Current Incident:** Remain in FAST mode until the DOMContentLoaded trial initializer is repaired and verification passes.  
2. **Documentation:** Share this revision with Cursor and Terminal Codex; archive in Git once reviewed.  
3. **Pilot:** On the next incident, trial the revised framework with the automation scaffolding in place.  
4. **Review:** Capture lessons in `.ai-agents/retrospectives/` and iterate.

Once FAST-mode remediation is complete, the team can formally adopt this framework for future troubleshooting sessions.

