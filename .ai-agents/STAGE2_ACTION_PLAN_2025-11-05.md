## Stage 2 Action Plan – Production Auth/Chat Diagnosis (2025‑11‑05)

### Context
- Production deploy `e3746a5` is live; initializer logs (`[INIT] …`) render, but UI remains locked behind the auth modal and chat submits trigger no network calls.
- ChatGPT supplied a set of live-site diagnostics and a potential hotfix; we’re adopting the diagnostic portions for Stage 2 while deferring code changes until we have evidence.

### Assignments
- **Cursor – Live DevTools Capture**
  - In prod DevTools console capture the following and attach screenshots/logs to `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md`:
    - `typeof window.initApp` to confirm initializer availability.
    - `window.__API_BASE` and any relevant env/meta fallbacks.
    - `window.__APP?.state?.auth` (or equivalent store) to record auth gating state.
    - Manual dispatch `window.dispatchEvent(new CustomEvent('auth:open'))` and note modal behaviour.
    - Attempt a chat submission; document whether `fetch` fires, including console/network output and any guard log messages.
- **CIT – Stage 2 Diagnosis Author**
  - Use Cursor’s evidence to build the Stage 2 document (hypothesis list, falsifiers, updated diagnosis) and request Codex approval before coding.
- **Codex – Oversight**
  - Review Stage 2 submission, decide next steps (hotfix, env correction, further analysis), and coordinate Stage 3.

### Hotfix Guidance (Deferred)
- ChatGPT’s inline snippet that forces modal visibility and wraps `fetch` is parked until Stage 2 confirms root cause. Revisit after oversight sign-off.

### Deliverables
- Updated incident log: `.ai-agents/STAGE2_DIAGNOSIS_2025-11-05.md` (Cursor → CIT).
- Oversight decision recorded once Stage 2 approved.

### Notes
- Automation rollout questions are resolved per `.ai-agents/TEAM_QUESTIONS_AUTOMATION_ROLLOUT_2025-11-05.md`; implementation should wait for Stage 2/3 outcome.
- Keep status updates in the `✅ / ⚠️ / → Next` format aligned to the revised troubleshooting framework.
