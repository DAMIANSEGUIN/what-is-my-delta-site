# Team Update Template

**Purpose:** Standard format for sharing updates with team (Cursor, Codex, Damian)
**Usage:** Copy and fill out sections when sharing significant changes
**Created:** 2025-10-31

---

## Quick Update (Slack/Chat)

```
**[Feature/Fix Name] - [Status]**

**What's done:**
- [Bullet point summary]
- [Key changes]

**What's new:**
- [New files or documents]

**Next steps:**
- [What needs to happen next]

**Full details:** docs/[DETAILED_DOC].md
```

---

## Full Update (Email/Documentation)

### Subject Line Format
`[Project] [Component] - [Action] Complete/In Progress/Blocked`

**Examples:**
- `PS101 v2 - Browser Prompts Fix Complete`
- `Checkpoint System - Ready for Review`
- `Deployment - Issue #1 Live in Production`

---

### Email/Doc Body Template

```markdown
# [Feature/Fix Name] - Update

**Date:** YYYY-MM-DD
**Updated By:** [Your name/role]
**Status:** ✅ Complete / 🚧 In Progress / ⏳ Blocked / 🚨 Urgent

---

## Summary

[1-2 sentence summary of what changed and why]

---

## What Changed

### Code Changes
- **File:** `path/to/file.ext`
  - **Lines:** XXX-YYY
  - **Change:** [What was changed]
  - **Why:** [Reason for change]

### New Files Created
- `docs/FILE_NAME.md` - [Purpose]
- `scripts/FILE_NAME.sh` - [Purpose]

### Updated Documents
- `docs/FILE_NAME.md` - [What was updated]
- `docs/FILE_NAME.md` - [What was updated]

### Deleted/Deprecated
- `docs/OLD_FILE.md` - [Why deprecated]

---

## Impact Assessment

**Who this affects:**
- [ ] End users - [How]
- [ ] Cursor (code agent) - [How]
- [ ] Codex (docs agent) - [How]
- [ ] Claude Code (SSE) - [How]
- [ ] Damian (owner) - [How]

**Breaking changes:**
- [ ] Yes - [List breaking changes]
- [x] No

**Deployment required:**
- [ ] Yes - [When]
- [ ] No

---

## Testing Status

**Automated tests:**
- [ ] Unit tests: PASS/FAIL (X passed, Y failed)
- [ ] Integration tests: PASS/FAIL
- [ ] Regression tests: PASS/FAIL

**Manual testing:**
- [ ] Smoke test: PASS/FAIL
- [ ] User journey: PASS/FAIL
- [ ] Accessibility: PASS/FAIL
- [ ] Mobile: PASS/FAIL

**Test coverage:** X% (if applicable)

---

## Action Items

**Immediate (Today):**
- [ ] [Action item] - Owner: [Name] - Due: [Date]
- [ ] [Action item] - Owner: [Name] - Due: [Date]

**Short Term (This Week):**
- [ ] [Action item] - Owner: [Name] - Due: [Date]

**Follow-Up (Next Sprint):**
- [ ] [Action item] - Owner: [Name] - Due: [Date]

---

## Documentation

**New documentation:**
- `docs/FILE_NAME.md` - [What to read and why]

**Updated documentation:**
- `docs/FILE_NAME.md` - [What changed]

**Required reading:**
- [ ] `docs/FILE_NAME.md` - [Who should read this]

---

## Known Issues

**Resolved:**
- ✅ [Issue description] - [How resolved]

**Outstanding:**
- ⏳ [Issue description] - [Plan to resolve]

**Risks:**
- ⚠️ [Risk description] - [Mitigation plan]

---

## Questions/Discussion

**Open questions:**
1. [Question] - Needs input from [Who]
2. [Question] - Needs decision by [When]

**Discussion points:**
- [Topic for team discussion]

---

## Next Steps

**Immediate next action:**
[Clear description of the very next thing that needs to happen]

**Blocked on:**
- [ ] [What's blocking progress] - Waiting for [Who/What]

**Timeline:**
- [Date]: [Milestone]
- [Date]: [Milestone]

---

## Additional Context

**Related work:**
- [Link to related task/doc]
- [Link to related issue/PR]

**Background:**
[Any additional context that helps understand this update]

---

**END OF UPDATE**

**Questions?** Contact [Your name/role]
```

---

## Update Frequency Guidelines

**Daily standups (Quick format):**
- What you completed yesterday
- What you're working on today
- Any blockers

**Weekly updates (Full format):**
- Major milestones achieved
- Documentation changes
- Action items for next week

**Deployment updates (Full format):**
- Always send after production deployment
- Include verification results
- Document any issues encountered

**Incident updates (Full format):**
- Send immediately when critical issue found
- Update every 30 min during active incident
- Send final update when resolved

---

## Distribution Guidelines

**Who gets updates:**

**All team members (Cursor, Codex, Claude Code, Damian):**
- Major feature completions
- Deployment notifications
- Breaking changes
- Critical incidents

**Damian only:**
- Budget/cost changes
- Security incidents
- Strategic decisions needed
- Timeline impacts

**Agent-specific:**
- Cursor: Code changes, architecture decisions
- Codex: Documentation changes, process updates
- Claude Code: Infrastructure changes, operational updates

---

## Update Storage

**All team updates should be:**
- Saved to `docs/TEAM_UPDATE_[TOPIC]_[DATE].md`
- Referenced in PROJECT_PLAN_ADJUSTMENTS.md
- Linked from relevant task briefs
- Archived after 90 days (move to `docs/archive/`)

**Archive policy:**
- Keep last 90 days in `docs/`
- Move older to `docs/archive/YYYY-MM/`
- Never delete (maintain history)

---

## Examples

See these for reference:
- `docs/TEAM_UPDATE_PS101_FIX_001.md` - Feature completion update
- `docs/SHARE_CHECKPOINT_SYSTEM_FOR_CODEX_REVIEW.md` - Review request update
- `docs/PROJECT_PLAN_ADJUSTMENTS.md` - Consolidated update

---

**END OF TEAM UPDATE TEMPLATE**

**Maintained by:** Claude Code (SSE)
**Next review:** 2025-11-30
