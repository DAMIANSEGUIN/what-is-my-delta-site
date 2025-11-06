# Team Note – Deployment Package Review & Stage 2 Execution
**Date:** 2025-11-05  
**From:** Cursor (Team Coordinator)  
**To:** All Team Members  
**Status:** ✅ Ready for execution

---

## Summary

Deployment playbook reviewed and ready for adoption. Stage 2 execution continues with deployment validation in parallel.

**📋 Deployment Playbook:** `MOSAIC_DEPLOYMENT_FULL_2025-11-05.md` (repo root)

---

## Deployment Package Review

✅ **Playbook Contents:**
- Netlify `netlify.toml` configuration (base=mosaic_ui, SPA redirect)
- `_redirects` fallback file (if Netlify ignores TOML)
- Environment checklist (VITE_API_BASE, etc.) - matches Stage 0 requirements
- Runtime hotfix snippet (wraps fetch, forces modal open) - **deferred until Stage 2 diagnosis**

⚠️ **Runtime Hotfix Status:**
- Useful for debugging but **parked** until Stage 2 diagnosis complete
- Applying now would mask root causes
- Revisit after Codex approves Stage 2 diagnosis

---

## Today's Plan

### 1. Cursor – Netlify Validation + Stage 2 Capture

**Action Items:**
1. **Validate Netlify Configuration:**
   - Check if `netlify.toml` exists and matches playbook (base=mosaic_ui, SPA redirect)
   - Check if `_redirects` file exists (fallback if TOML ignored)
   - Document any differences from playbook in `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`
   - If differences found, prepare a branch aligning with playbook (no runtime hotfix yet)

2. **Continue Stage 2 DevTools Capture:**
   - Follow `.ai-agents/STAGE2_ACTION_PLAN_2025-11-05.md`
   - Attach all findings (screenshots, logs, console output) to `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`

**Deliverables:**
- Netlify config validation status in Stage 2 diagnosis doc
- Complete DevTools capture evidence in Stage 2 diagnosis doc

→ **Next:** CIT takes over with evidence to draft Stage 2 diagnosis

---

### 2. CIT – Stage 2 Diagnosis Author

**Action Items:**
1. Wait for Cursor's capture evidence
2. Draft Stage 2 diagnosis in `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`
3. Include:
   - Hypothesis list based on evidence
   - Falsifiers and verification checks
   - Updated diagnosis
   - Reference deployment playbook as remediation option
   - Highlight any config gaps (Netlify env/CSP) surfaced by capture

**Deliverables:**
- Complete Stage 2 diagnosis document
- Request Codex approval before any code changes

→ **Next:** Codex reviews and decides next steps

---

### 3. Codex – Oversight & Decision

**Action Items:**
1. Review Stage 2 diagnosis document
2. Decide:
   - Apply runtime hotfix snippet (from playbook)?
   - Proceed directly to targeted code fixes?
   - Further analysis needed?
3. Coordinate Stage 3 actions

**Deliverables:**
- Decision recorded in Stage 2 diagnosis doc
- Stage 3 action plan if approved

→ **Next:** Assign Stage 3 work based on decision

---

## Key Files & Locations

**Deployment Playbook:**
- `MOSAIC_DEPLOYMENT_FULL_2025-11-05.md` (repo root)

**Stage 2 Documents:**
- `.ai-agents/STAGE2_ACTION_PLAN_2025-11-05.md` (instructions)
- `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md` (evidence + diagnosis)

**Netlify Configuration:**
- `netlify.toml` (current config)
- `_redirects` (fallback file, if needed)

---

## Status Updates

All status updates follow revised troubleshooting framework format:
- `✅` Completed actions
- `⚠️` Warnings/issues
- `→ Next` Upcoming actions
- `🔴 BLOCKED` Blockers

---

## Timeline

- **Now:** Cursor validates Netlify config + captures DevTools evidence
- **Next:** CIT drafts Stage 2 diagnosis (after evidence lands)
- **Then:** Codex reviews and decides on hotfix vs. targeted fixes
- **Finally:** Stage 3 execution (hotfix or code fixes + redeploy)

---

**Next Action:** Cursor begins Netlify validation and Stage 2 DevTools capture

