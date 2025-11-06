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

## Questions for Team Input (Responses logged 2025-11-05 by CIT ✅)

### 1. Documentation Discipline Script Scope

**Decision:** ✅ Include four mandatory touchpoints  
- `CLAUDE.md`  
- `.verification_audit.log`  
- Active incident note (`FOR_*_*.md`)  
- Relevant checklist used for the session (e.g., `TROUBLESHOOTING_CHECKLIST.md`, `DEPLOYMENT_CHECKLIST.md`)

Architecture decisions and handoff docs remain optional (notify reviewer when changed, but no hard gate).

**Context:** The script (`scripts/verify_documentation_discipline.sh`) will enforce Operating Rule #8 from the session protocol, which requires agents to update documentation before declaring tasks complete.

---

### 2. Regression Test Suite Scope

**Decision:** ✅ Ship a minimum smoke suite initially  
- Verify `[INIT]` log sequence to confirm trial initializer  
- Check auth modal visibility + form elements  
- Confirm chat button/input exist and handler is attached

**Context:** The script (`scripts/regression_tests.sh`) will serve as the baseline UX regression suite. Initial version can wrap existing smoke tests.

---

### 3. Checkpoint Validator Enforcement Level

**Decision:** ✅ Keep the validator lightweight  
- Quick syntax check  
- Critical signature presence (auth modal, PS101 markers, chat DOM nodes)  
- Hard fail only when signatures missing; leave lint/style enforcement to pre-commit hooks

**Context:** The validator (`.ai-agents/checkpoint_validator.sh`) is a fast lint/feature smoke test that runs after each significant change. It's a subset of pre-push checks designed to fail fast.

---

### 4. Retrospective Scheduling

**Decision:** ✅ 30-minute live session the day after production stability  
- Attendees: Codex (planning), Cursor (implementation), Netlify Ops rep, owners for chat/auth  
- Use call to lock in framework adoption timing; capture actions in short follow-up doc

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

- [x] **Team:** Provide decisions on automation scope (CIT, 2025-11-05)
- [ ] **Codex:** Update automation work plan + notify Cursor (in progress)
- [ ] **Cursor:** Implement automation scripts/templates per decisions
- [ ] **Terminal Codex:** Available for deep searches/log pulls during testing
- [ ] **Claude Code:** Standby for deployment/log validation once scripts ready

---

**Next Steps:** Once team questions are answered, Codex will proceed with template/script build and coordinate testing across agents.
