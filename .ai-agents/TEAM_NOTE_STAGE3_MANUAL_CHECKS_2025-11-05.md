# Stage 3 Manual Checks – Action Needed (2025-11-05)

**Context**
- Consolidated build (commit `7612285`) is live; automated verification passed.
- Manual check shows `initApp` loads, but the login CTA remains hidden when a stale `delta_session_id` exists in localStorage.
- Users with previous sessions can no longer open the auth modal; chat stays unreachable behind the overlay.

**Required Action**
1. Update both `mosaic_ui/index.html` and `frontend/index.html` so the CTA is shown whenever `!isAuthenticated` (remove the `&& !sessionId` guard).
2. Redeploy via the standard wrapper (BUILD_ID injected) and rerun automated scripts.
3. After redeploy, perform manual checks:
   - `typeof window.initApp` → `"function"`
   - Auth modal hides automatically for new visitors and CTA remains available
   - Chat submission triggers `/wimd` network request in DevTools
4. Log results in `.ai-agents/STAGE3_VERIFICATION_2025-11-05.md` and `.verification_audit.log`.

**Owners**
- Cursor: implement guard tweak + redeploy
- CIT: verify + update Stage 3 doc and incident notes post-deploy
- Codex: review redeploy summary, approve incident closure

Please acknowledge once the guard change is staged so we can proceed to redeploy.
