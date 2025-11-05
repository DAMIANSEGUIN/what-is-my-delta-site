# Team Questions - Automation Rollout Planning
**Date:** 2025-11-05  
**From:** Codex (Planning)  
**Context:** Post-FAST-mode remediation, pre-automation template build

---

## Prerequisites Status ✅

**FAST-mode remediation complete:**
- ✅ DOMContentLoaded handlers consolidated into single `initApp()` function
- ✅ Verification scripts executed and passed
- ✅ Evidence captured in incident log (`FOR_NARS_FRONTEND_JAVASCRIPT_ISSUE_2025-11-04.md`)
- ✅ Documentation updated (`CLAUDE.md`, `.verification_audit.log`)

**Ready for automation template work once team questions are answered.**

---

## Questions for Team Input

### 1. Documentation Discipline Script Scope

**Question:** Are there extra checks or file paths the documentation discipline script must verify beyond the standard trio (CLAUDE.md, .verification_audit.log, incident note)?

**Context:** The script (`scripts/verify_documentation_discipline.sh`) will enforce Operating Rule #8 from the session protocol, which requires agents to update documentation before declaring tasks complete.

**Current scope:**
- `CLAUDE.md` - Main documentation file
- `.verification_audit.log` - Audit trail
- Incident notes (e.g., `FOR_*_*.md`)

**Need team input on:**
- Additional required files?
- Architecture decision logs?
- Deployment checklists?
- Handoff manifests?

---

### 2. Regression Test Suite Scope

**Question:** What level of coverage do we expect for the first regression suite iteration—minimum smoke (trial init, chat button) or anything broader?

**Context:** The script (`scripts/regression_tests.sh`) will serve as the baseline UX regression suite. Initial version can wrap existing smoke tests.

**Options:**
- **Minimum smoke:** Trial init, chat button, auth modal visibility
- **Broader:** Include PS101 flow navigation, form validation, localStorage persistence
- **Comprehensive:** Full feature matrix (future iteration)

**Need team input on:**
- Minimum viable scope for first iteration?
- Which features are critical path?
- Any features to explicitly exclude initially?

---

### 3. Checkpoint Validator Enforcement Level

**Question:** Should the checkpoint validator enforce formatting (e.g., linting) or just critical signatures?

**Context:** The validator (`.ai-agents/checkpoint_validator.sh`) is a fast lint/feature smoke test that runs after each significant change. It's a subset of pre-push checks designed to fail fast.

**Options:**
- **Critical signatures only:** Verify key functions/features exist, no formatting checks
- **Formatting included:** Run linter, enforce code style
- **Hybrid:** Critical signatures + basic syntax validation (no style enforcement)

**Need team input on:**
- Balance between speed and thoroughness?
- Should it block on style issues or just warn?
- Integration with existing pre-commit hooks?

---

### 4. Retrospective Scheduling

**Question:** Any scheduling constraints for the retrospective once production is stable?

**Context:** After the outage is confirmed closed and automation templates are built, we'll hold a short post-fix retrospective to:
- Review how FAST mode went
- Confirm adoption timing for the revised framework
- Assign automation deliverables

**Need team input on:**
- Preferred timing (immediate after fix, next day, end of week)?
- Duration (15 min, 30 min, 1 hour)?
- Required attendees?
- Format preferences (async doc, sync call, hybrid)?

---

## Automation Template Work Plan

Once team questions are answered and outage fix is locked in the repo, Codex will:

1. **Build automation templates/scripts:**
   - `.ai-agents/checkpoint_validator.sh` - Fast lint + critical-feature smoke
   - `scripts/verify_documentation_discipline.sh` - Enforce Operating Rule #8
   - `scripts/regression_tests.sh` - Initial PS101/UI regression wrapper
   - `.ai-agents/templates/STAGE_1_TEMPLATE.md` - Structured Stage 1 capture
   - `.ai-agents/templates/RETROSPECTIVE_TEMPLATE.md` - Post-incident review scaffold

2. **Coordinate testing:**
   - Cursor implements shell scripts/templates
   - Terminal Codex provides deep searches/log pulls
   - Claude Code reviews deployment/log health

3. **Schedule retrospective:**
   - Review FAST mode execution
   - Confirm revised framework adoption timing
   - Assign automation deliverables

---

## Action Items

- [ ] **Team:** Answer questions above (provide input via Slack/Discord/PM thread)
- [ ] **Codex:** Wait for team input before starting template work
- [ ] **Cursor:** Stand by for automation script implementation assignments
- [ ] **Terminal Codex:** Available for deep searches/log pulls during testing
- [ ] **Claude Code:** Standby for deployment/log validation once scripts ready

---

**Next Steps:** Once team questions are answered, Codex will proceed with template/script build and coordinate testing across agents.

