# What is my Delta — Full Export Bundle (v2)
_Date: 2025-08-22_

This package contains a **self-contained, static** implementation of the Delta coaching flow with:
- PS101 prompts (sequential, one-at-a-time).
- Coaching nudges and iteration support (Support button).
- Local progress persistence (browser LocalStorage).
- Optional **shared database** (Supabase) for community contributions and prompt suggestions.
- A clear map of **all platforms in play** (hosting, AI troubleshooting, widgets).
- **Known Issues & Fixes** from our real troubleshooting history.
- A **ready-to-paste troubleshooting packet** template for Claude/Gemini.

---

## 0) AI-Human Hybrid Development Context

**This project was developed using multiple AI tools working with human oversight. Understanding this context is crucial for troubleshooting and maintenance.**

### AI Tools Used:
- **Code Generation**: ChatGPT, Claude, GitHub Copilot
- **Integration**: Various AI sessions for widget embedding, database setup
- **Deployment**: AI-generated Vercel configurations and CSP policies

### Common AI-Generated Problems:
- Multiple conflicting integrations (3+ chat widgets)
- Over-permissive security policies
- Inconsistent error handling patterns
- Missing production environment considerations

---

## 1) Platforms in Play (Single-Page Overview)

### Hosting / Deployment
- **Vercel** (primary): Git-connected deploys, serverless functions in `/api`.
- **Netlify** (optional fallback): Static hosting, easy drag-and-drop.
- **Cloudflare Pages** (optional fallback): Static hosting with global CDN.

### AI / Troubleshooting Support
- **ChatGPT (OpenAI)**: system-level diagnosis, scripts, deployment orchestration.
- **Claude (Anthropic)**: long-context analysis (large logs, long configs), careful minimal-change fixes.
- **Gemini (Google)**: doc-aligned checks for CSP/CORS/web standards and policy nuances.
- **GitHub Copilot**: inline coding assistance inside VS Code (best for programmers).
- **Sourcegraph Cody**: whole-repo context assistant (open-source, free tier).

### Engagement Widgets (optional embeds in `index.html`)
- **Voiceflow**: AI chat widget.
- **Tidio**: live chat + AI (free tier).
- **Landbot**: visual flow builder.
- **Botpress Cloud**: AI-native no-code bots.

### Database / State
- **LocalStorage**: browser-side progress persistence (default).
- **Supabase**: community DB (free tier Postgres + RLS). Optional; app runs without it.

---

## 1) Quick Start (No Database)
1. Open `index.html` (double-click) or deploy the folder to Netlify/Vercel/Cloudflare.
2. You will see **Start / Next / Support** flow with your local progress saved automatically.
3. Optional: paste a Voiceflow/Tidio/Landbot/Botpress **widget snippet** before `</body>` in `index.html`.

> This runs fully offline (no backend) using `data/prompts.ps101.json`.

---

## 2) Enable Community Database (Supabase) — Optional
1. Create a Supabase project → copy **Project URL** and **anon key**.
2. In Supabase SQL editor, run the schema in `scripts/schema.sql`.
3. Copy `public/env.example.js` to `public/env.js` and set your `SUPABASE_URL` and `SUPABASE_ANON_KEY`.
4. Deploy to **Vercel** (or open locally). If env is present, the app will:
   - Accept **community submissions** (answers).
   - Accept **prompt suggestions**.
   - Read aggregate insights from `/api/aggregate` (serverless placeholder provided; customize).

> If `public/env.js` is missing or empty, DB features are disabled but the app still runs using LocalStorage.

---

## 3) Vercel Deployment Notes
- This bundle includes `vercel.json`.
- **Known Production blocker:** Deployment Protection can return **401/404** on `/` and `/api/*` even when Preview works.
  - **Fix A (simplest):** Vercel → Project → Settings → Deployment Protection → **disable for Production**.
  - **Fix B (keep protection):** Generate a bypass token and append it to the URL: `?vercel_token=YOUR_TOKEN`.
- **CSP (Content-Security-Policy):** set **Report-Only** in `index.html` to start; tighten after widget testing.

---

## 4) Files
- `index.html` — SPA shell with coaching UI and widget slot.
- `assets/styles.css` — minimal, dark UI.
- `assets/coaching.js` — heuristics for hints/nudges.
- `assets/app.js` — main controller (flow, local state, community ops).
- `assets/db.js` — optional Supabase client wrapper.
- `data/prompts.ps101.json` — seed prompts (replace with your full set).
- `api/aggregate.js` — example serverless endpoint for aggregates.
- `scripts/schema.sql` — Supabase schema + RLS policies.
- `public/env.example.js` — copy to `public/env.js` with real values.
- `vercel.json` — routes and headers.
- `docs/troubleshooting-packet.txt` — ready-to-paste packet for Claude/Gemini.

---

## 5) Known Issues & Fixes (AI-Generated Code & Interoperability)

### 5.1 AI-Generated Code Problems

#### 5.1.1 Multiple Chat Widget Conflicts
- **Symptom:** Only one chat widget works, others fail silently or cause console errors.
- **Cause:** AI tools generated multiple widget integrations without conflict resolution.
- **Fix:** Choose ONE widget. Remove others from `index.html`. Update CSP accordingly.
- **Prevention:** Always test widget integrations in isolation first.

#### 5.1.2 Inconsistent Error Handling Patterns
- **Symptom:** Some functions throw unhandled promises, others use callbacks inconsistently.
- **Cause:** Different AI sessions generated different error handling approaches.
- **Fix:** Standardize on async/await with try/catch. See `assets/db.js` for pattern.
- **Detection:** `grep -r "catch\|Promise\|async" assets/` to audit patterns.

#### 5.1.3 Hardcoded Assumptions Breaking in Production
- **Symptom:** Features work in development but fail in production environments.
- **Cause:** AI-generated code assumes specific browser/environment capabilities.
- **Fix:** Add feature detection: `if (typeof localStorage !== 'undefined')` before usage.
- **Common culprits:** LocalStorage, FileReader API, fetch polyfills.

#### 5.1.4 Over-Permissive CSP from AI Generation
- **Symptom:** CSP allows `unsafe-eval` and `unsafe-inline` everywhere.
- **Cause:** AI tools generate permissive CSP to avoid initial blocking issues.
- **Fix:** Start with `Content-Security-Policy-Report-Only`, tighten incrementally.
- **Process:** Monitor `/csp-report` endpoint, remove permissions one by one.

### 5.2 Interoperability Issues

#### 5.2.1 Widget CSP Mismatches
- **Symptom:** Widget loads but can't connect/authenticate with parent service.
- **Cause:** AI-generated CSP doesn't match actual widget domain requirements.
- **Fix:** Check widget vendor docs for exact CSP requirements. Test with `curl -I`.
- **Example:** Crisp needs `*.crisp.chat` for WebSocket connections, not just script loading.

#### 5.2.2 LocalStorage vs Database Sync Conflicts
- **Symptom:** User sees old data after database is configured, or data appears to "disappear."
- **Cause:** No migration strategy between localStorage and Supabase modes.
- **Fix:** Implement data migration in `assets/app.js` `loadSaved()` function.
- **Strategy:** On first DB connection, push localStorage queue, then clear local data.

#### 5.2.3 File Upload Security Gaps
- **Symptom:** Malicious files uploaded or legitimate files rejected.
- **Cause:** AI generated basic `accept=".txt,.pdf"` without server-side validation.
- **Fix:** Add client-side MIME checking and file size limits before processing.
- **Prevention:** Never trust client-side file validation alone in production.

#### 5.2.4 Mobile Viewport Calculation Errors  
- **Symptom:** UI elements overflow or become unusable on mobile devices.
- **Cause:** AI-generated CSS assumes desktop viewport dimensions.
- **Fix:** Test with `chrome://inspect` device emulation. Add `@media` breakpoints.
- **Pattern:** Use `clamp()` for responsive sizing instead of fixed pixel values.

### 5.3 Cross-AI Compatibility Issues

#### 5.3.1 Conflicting Code Styles from Different AI Sessions
- **Symptom:** ESLint errors, inconsistent naming conventions, mixed patterns.
- **Cause:** Different AI tools or sessions generated code with different style preferences.
- **Fix:** Run `prettier --write .` and establish ESLint config before AI iterations.
- **Prevention:** Include existing code context when asking AI for modifications.

#### 5.3.2 Incomplete Refactoring by AI Tools
- **Symptom:** Function renamed in some files but not others, causing reference errors.
- **Cause:** AI tools don't always have full project context during refactoring.
- **Fix:** Use IDE "Find and Replace All" for systematic renames. Verify with `grep -r`.
- **Pattern:** Always request "show me all references" before accepting AI refactoring.

### 5.4 Original Issues (Updated)

#### 5.4.1 Vercel Deployment Protection → 401/404 on Production
- **Symptom:** Prod `/` or `/api/chat` returns 401/404; Preview works.
- **Root Cause:** AI deployment guides don't mention Vercel's default security settings.
- **Fix:** Vercel Dashboard → Settings → Deployment Protection → Disable for Production.
- **Alternative:** Use bypass token: `?vercel_token=YOUR_TOKEN`.

#### 5.4.2 Environment Variables Not Loading
- **Symptom:** `window.__ENV` is undefined, database features don't work.
- **Cause:** AI-generated code assumes `public/env.js` exists without fallback.
- **Fix:** Copy `public/env.example.js` to `public/env.js` with real Supabase credentials.
- **Fallback:** App runs in localStorage-only mode if env missing.

---

## 6) AI-Aware Troubleshooting Workflow 

### 6.1 For AI-Generated Code Issues
1. **Identify the AI pattern**: Look for telltale signs (overly permissive CSP, multiple similar functions, inconsistent naming).
2. **Find the source**: Check git history to see which AI tool/session created the problematic code.
3. **Contextualize the fix**: Always include surrounding code when asking AI for corrections.
4. **Test in isolation**: Disable other features to verify the fix works independently.
5. **Document the pattern**: Add to this README so future AI sessions avoid the same mistake.

### 6.2 For Interoperability Issues  
1. **Isolate the integration**: Test each external service (widgets, DB, APIs) separately.
2. **Check the real requirements**: Consult vendor docs, not AI assumptions about what they need.
3. **Use staged rollout**: Enable integrations one at a time with monitoring.
4. **Validate cross-browser**: AI often generates code that works in Chrome but fails elsewhere.
5. **Monitor production**: Set up alerts for CSP violations, JavaScript errors, API failures.

### 6.3 Mixed Human-AI Development Process
1. **Reproduce & capture**: URL, timestamp, exact error text/code, browser/device info.
2. **Identify AI involvement**: Was this code AI-generated? Which tool? When?
3. **Packetize with context**: Use `docs/troubleshooting-packet.txt` but include AI context.
4. **Choose the right AI tool**:
   - **ChatGPT**: Quick fixes, deployment orchestration, shell commands
   - **Claude**: Long-context analysis, minimal-change fixes, code review
   - **Gemini**: Standards compliance (CSP/CORS), documentation cross-checks
   - **GitHub Copilot**: Only for small inline changes with full human oversight
5. **Apply changes surgically**: One fix at a time, test immediately, keep rollback ready.
6. **Update documentation**: Record the fix pattern to prevent AI from repeating the issue.

---

## 7) Rollback in 60 Seconds
- Remove `public/env.js` → DB-disabled (local-only mode).
- Re-deploy (or refresh locally) → app remains functional with LocalStorage only.

---

## 8) License
This bundle is provided as-is for your internal testing and deployment.
