# AI Agent Initialization Prompt

**Copy/paste this at the start of EVERY new AI agent session**

---

You are working on the Mosaic Platform project. This project has strict protocols to prevent breaking critical features.

**MANDATORY FIRST ACTION - Before doing ANYTHING else:**

1. Run session start verification:
   ```bash
   ./scripts/verify_critical_features.sh
   ```

2. If verification passes, declare:
   ```
   ✅ Session start verification passed
   ✅ Critical features confirmed present:
      - Authentication UI: [count] references
      - PS101 v2 flow: [count] references
      - API configuration: [status]

   I acknowledge these features MUST BE PRESERVED.
   ```

3. If verification FAILS:
   ```
   ❌ CRITICAL: Verification failed
   🚨 I will NOT proceed until this is resolved

   Human action required: [details from verification output]
   ```

**Protocol files to read:**
- `.ai-agents/SESSION_START_PROTOCOL.md` - Full session start procedure
- `.ai-agents/HANDOFF_PROTOCOL.md` - Agent handoff procedures
- `TROUBLESHOOTING_CHECKLIST.md` - Pre-flight checks for code changes
- `docs/DEPLOYMENT_VERIFICATION_CHECKLIST.md` - Post-deploy verification

**Critical features that CANNOT be removed:**
1. Authentication UI (authModal, loginForm, registerForm)
2. PS101 v2 flow (PS101State references)
3. API_BASE = '' configuration (relative paths)
4. Chat interface
5. File upload functionality

**Operating rules:**
- ✅ Run `./scripts/verify_critical_features.sh` before EVERY deploy
- ✅ Never remove critical features without explicit human approval
- ✅ Never use `git commit --no-verify` without approval
- ✅ Never replace files (like copying frontend → mosaic_ui) without checking for feature loss
- ✅ Follow pre-commit hook warnings (they block destructive changes)
- ✅ Run deployment verification checklist after every deploy

**Pre-commit hook installed:**
- Blocks commits that remove authentication
- Blocks commits that remove PS101 flow
- Blocks database anti-patterns
- You will see errors if you try to commit breaking changes

**If you need to hand off to another agent:**
1. Run: `./scripts/create_handoff_manifest.sh > .ai-agents/handoff_$(date +%Y%m%d_%H%M%S).json`
2. Tell human: "Handoff manifest created - next agent should read it"

**Session log:**
- Your actions are logged in `.ai-agents/session_log.txt`
- Handoffs are logged in `.ai-agents/handoff_log.txt`

---

**Acknowledge protocol by running verification and declaring readiness (see steps 1-2 above).**
