# 📋 Project Plan Adjustments - Review Request

**To:** Cursor + Codex + Team
**From:** Claude Code (Troubleshooting SSE)
**Date:** 2025-10-31 (Updated with Codex corrections)
**Re:** Critical action items from PS101 v2 review + Codex operational notes

### ✅ Latest Update (2025-10-31)
**Codex corrections applied** to main document:
- Fixed non-existent test/script references
- Marked TODOs for net-new work (validate_data_quality.py, rotate_api_key.sh)
- Corrected OPERATIONS_MANUAL to expand existing section (not create duplicate)

**All references now point to real, actionable files.**

---

## 📄 Document to Review

**`docs/PROJECT_PLAN_ADJUSTMENTS.md`**

This consolidated action plan integrates:
- ✅ Claude Code's PS101 v2 technical review findings
- ✅ Codex's operational gap analysis
- ✅ Updated checklists with ownership assignments
- ✅ Decision points requiring team discussion

---

## 🎯 Key Points to Review

### 1. **PS101 v2 Status** (Section 1)
- ✅ Code complete, matches canonical spec
- 🚨 **3 blocking issues** need 2.5-4 hours to fix before deployment
- 📋 Detailed fixes documented in `docs/CURSOR_FIXES_REQUIRED.md`

**Owner:** Cursor
**Deadline:** 2025-11-01

### 2. **Operational Gaps** (Section 2)
Three critical documentation gaps identified:

**Gap #1: Checklist Ownership**
- SHARE_WITH_MOSAIC_TEAM.md has all items unchecked
- No owners, no deadlines, unclear status
- **Owner:** Codex | **Deadline:** 2025-11-01

**Gap #2: API Key Management**
- No rotation process documented
- No security/revocation procedure
- **Owner:** Codex | **Deadline:** 2025-11-02

**Gap #3: Success Metrics Validation**
- Claims <2s response, >90% quality, >99% uptime
- No measurement methodology defined
- **Owner:** Codex | **Deadline:** 2025-11-02

### 3. **Action Plan** (Section 3)
Phased approach with owners and deadlines:

**Phase 1 (This Week):** Unblock deployment + close critical gaps
- Total: ~7-10 hours across team

**Phase 2 (Next Sprint):** Complete features + strengthen operations
- Total: ~30 hours

**Phase 3 (Sprint 3):** Full maturity
- Total: ~40+ hours

### 4. **Decision Points** (Section 6)
**4 decisions needed from Damian:**

1. **Inline forms vs modals** for obstacle/action collection
   - Recommendation: Inline forms (faster)
   - Needed by: 2025-11-01

2. **Step 10 timeline**: Deploy with placeholder vs wait for full dashboard?
   - Recommendation: Placeholder now, full dashboard Sprint 2
   - Needed by: 2025-11-01

3. **Operations doc ownership**: Who maintains going forward?
   - Recommendation: Shared (Codex process, Cursor technical)
   - Needed by: 2025-11-02

4. **Monitoring tool**: Railway only vs Sentry vs custom dashboard?
   - Recommendation: Railway + enhanced /health + Uptime Robot (free)
   - Needed by: 2025-11-05

### 5. **Risk Assessment** (Section 7)
**High-risk items flagged:**
- 🚨 PS101 v2 prompt() dialogs (UX/accessibility issue)
- 🚨 No API key rotation plan (security risk)
- 🚨 Web scraping untested (user-facing features may break)
- 🚨 No monitoring = can't detect outages

### 6. **Updated Checklists with Ownership** (Section 5)
All checklists now have:
- ✅ Current status (Done / In Progress / Not Started)
- 👤 Owner assignments
- 📅 Deadlines
- 🔗 Dependencies

---

## ✅ Immediate Next Actions

### For Damian (5 minutes)
- [ ] Read Executive Summary (Section: EXECUTIVE SUMMARY)
- [ ] Review Decision Points (Section 6)
- [ ] Make 4 key decisions
- [ ] Assign backend team owners

### For Cursor (2.5-4 hours)
- [ ] Read `docs/CURSOR_FIXES_REQUIRED.md` (detailed implementation guide)
- [ ] Implement PS101 v2 fixes (Issues #1, #2, #3)
- [ ] Run testing checklist (14 scenarios)
- [ ] Commit changes (wait for Damian approval before deploy)

### For Codex (3-4 hours)
- [ ] Read full PROJECT_PLAN_ADJUSTMENTS.md
- [ ] Audit SHARE_WITH_MOSAIC_TEAM.md checklist statuses
- [ ] Assign owners and deadlines to unchecked items
- [ ] Document API key management process
- [ ] Define success metrics validation methodology

### For Backend Team (TBD)
- [ ] Awaiting owner assignment
- [ ] Priority: End-to-end testing of job sources
- [ ] Next: Implement rate limiting + monitoring

---

## 📊 Critical Path

**To unblock PS101 v2 deployment:**

```
Day 1 (2025-11-01):
├─ Cursor: Fix 3 blocking issues (2.5-4h)
├─ Cursor: Run testing checklist (1-2h)
├─ Codex: Assign checklist owners (30m)
└─ Damian: Make decisions + approve fixes (30m)

Day 2 (2025-11-02):
├─ Cursor: Deploy to production (30m)
├─ Codex: Document API key management (1h)
├─ Codex: Define metrics validation (1-2h)
└─ Team: Monitor logs for 24 hours
```

**Total blocking work:** 7-10 hours

---

## 📁 Related Documents

**Read these in order:**

1. **`docs/PROJECT_PLAN_ADJUSTMENTS.md`** ← **START HERE** (this is the master plan)
2. **`docs/CURSOR_FIXES_REQUIRED.md`** (Cursor implementation guide)
3. **`docs/TEAM_REVIEW_CHECKLIST.md`** (Comprehensive review checklist)
4. **`SHARE_WITH_MOSAIC_TEAM.md`** (Job sources plan with gaps)
5. **`SESSION_START_README.md`** (Claude Code startup guide)

**Supporting docs:**
- `docs/PS101_CANONICAL_SPEC_V2.md` (Product spec)
- `docs/IMPLEMENTATION_SUMMARY_PS101_V2.md` (Technical summary)
- `TROUBLESHOOTING_CHECKLIST.md` (Safety protocols)

---

## 🎯 Success Criteria

**Phase 1 complete when:**
- [ ] PS101 v2 deployed to production (no blockers)
- [ ] All checklists have owners + deadlines
- [ ] API key management documented
- [ ] Success metrics validation defined

**Target:** 2025-11-02

---

## 💬 Questions or Blockers?

**Technical questions (PS101 v2 fixes):**
→ Reference `docs/CURSOR_FIXES_REQUIRED.md` (has code snippets + testing checklist)

**Process questions (checklists, ownership):**
→ Reference `docs/PROJECT_PLAN_ADJUSTMENTS.md` Section 5 (Updated Checklists)

**Operational questions (keys, metrics, monitoring):**
→ Reference `docs/PROJECT_PLAN_ADJUSTMENTS.md` Section 4 (Operations Manual Additions)

**Blockers or need decisions:**
→ Escalate to Damian immediately

---

## 📝 Summary

**What:** Comprehensive project plan adjustment consolidating technical review + operational gaps

**Why:** PS101 v2 ready but has 3 blocking issues; operational docs missing critical info

**When:** Immediate action needed (Phase 1 targets 2025-11-02)

**Who:**
- Cursor (implementation)
- Codex (documentation/process)
- Damian (decisions/approval)
- Backend Team (testing/deployment)

**Next Step:** Read `docs/PROJECT_PLAN_ADJUSTMENTS.md` and execute immediate actions for your role

---

**Document:** `docs/PROJECT_PLAN_ADJUSTMENTS.md`
**Status:** Ready for team review
**Action Required:** Read + Execute immediate actions
**Timeline:** Phase 1 complete by 2025-11-02
