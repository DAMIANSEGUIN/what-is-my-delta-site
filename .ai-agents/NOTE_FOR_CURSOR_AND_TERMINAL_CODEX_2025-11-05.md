# NOTE FOR CURSOR & TERMINAL CODEX – FAST MODE + FRAMEWORK UPDATE
**Prepared by:** Codex (Planning)  
**Date:** 2025-11-05

---

## Cursor (Implementation)
1. **Incident Focus:** `FOR_NARS_FRONTEND_JAVASCRIPT_ISSUE_2025-11-04.md` – trial initializer halts after first console log.  
2. **Code Targets:**  
   - Consolidate and harden the trial initializer in `mosaic_ui/index.html` at lines ~2021, 2275, 2300, 3526.  
   - Extract a safe localStorage helper and reconcile DOMContentLoaded handlers into a single `initApp()` entry point.  
3. **Verification:**  
   - Run `./scripts/verify_critical_features.sh` before and after the fix.  
   - Use DevTools to confirm console flows through `[TRIAL] Initialization complete`.  
   - Execute `./scripts/verify_live_deployment.sh https://whatismydelta.com/` when ready.  
4. **Documentation:** Update `CLAUDE.md`, `.verification_audit.log`, and the incident file with results. Reference `REVISED_TROUBLESHOOTING_FRAMEWORK_2025-11-05.md` for Stage 6 expectations.

---

## Terminal Codex
1. **Reference Docs:**  
   - Revised framework: `REVISED_TROUBLESHOOTING_FRAMEWORK_2025-11-05.md`  
   - Situational report: `.ai-agents/SITUATIONAL_REPORT_2025-11-05.md`
2. **Support Tasks:**  
   - Assist Cursor with wide searches (`rg`/tooling) or large diffs during FAST-mode debugging.  
   - Help draft automation scripts listed in the framework roadmap when scheduled.  
3. **Protocol Reminder:** Run `.ai-agents/SESSION_START_PROTOCOL.md` and log compliance before starting any command sequence; defer destructive commands unless explicitly approved.

---

**Contact:** Coordinate through the situational report for status changes and handoffs. Once production is stabilized, revisit the automation roadmap in the revised framework.
