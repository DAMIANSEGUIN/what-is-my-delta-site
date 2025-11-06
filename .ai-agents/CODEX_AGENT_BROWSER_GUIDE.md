# Codex Agent (Browser) – Operational Guide

**Purpose:** Give the browser-based Codex Agent a self-serve reference so it can capture Mosaic production evidence and log outcomes without relying on human relays.

**Context:** We run two Codex agents in tandem:
- **Terminal Codex** – Handles repo work (coding, scripts, docs)
- **Codex Agent (You)** – Browser-based, traces real user flows in production

**Key Point:** Terminal Codex reads your evidence directly from Stage docs and implements fixes immediately – no human relay needed.

---

## Role & Startup

1. **Respond to “Codex Reset Protocol.”** When the reset phrase appears, re-run `.ai-agents/SESSION_START_PROTOCOL.md` steps 1–5, restate your Present State → Desired Outcome, and write a new entry to `.ai-agents/session_log.txt`.
2. **Load Stage context:** Read the most recent files before acting:
   - `.ai-agents/STAGE1_CURRENT_STATE_*`
   - `.ai-agents/STAGE2_ACTION_PLAN_*`
   - `.ai-agents/STAGE2_DIAGNOSIS_*`
   - `.ai-agents/STAGE3_VERIFICATION_*`
3. **Confirm assignment:** Use those documents to restate exactly which evidence you are collecting and which critical features must remain intact.

---

## Evidence Capture Workflow

1. Launch the production site in a fresh/incognito browser window to avoid cached `delta_session_id`.
2. Run the Stage 2 checklist commands in DevTools Console and Network tab (initializer availability, API base, auth modal state, chat `/wimd` requests, etc.).
3. Paste raw console output, network findings, and observations into `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md` (or the current diagnostics file) under the “Evidence Captured” section.
4. Attach screenshots or summarize visuals in the same document; list the filename or storage location if images are shared elsewhere.
5. Mark outstanding items (e.g., “Network tab evidence pending”) with `⚠️` so the next agent can immediately see what is missing.

---

## Communication & Requests

- **Do not wait for a human relay.** If you need additional data or clarification, document the request inline in the Stage diagnosis file and in `.ai-agents/TEAM_NOTE_STAGE2_EVIDENCE_READY_*.md` (or create a new note). Other agents monitor those files.
- **Acknowledge incoming answers** by updating the same document where the question was posed and time-stamping the response.
- **For new blockers** (site unreachable, verification failure, etc.), append a short alert to `.ai-agents/handoff_log.txt` and flag it `⚠️`.

### Artifact Requests

- When you see **“Request for Artifacts – Please share any prior screenshots, DevTools captures, or diagnostic notes from earlier agents…”**, gather the latest material from:
  - Evidence sections inside `.ai-agents/STAGE2_DIAGNOSIS_*.md`
  - Any `screenshots/` or shared asset directories referenced there
  - Prior notes in `.ai-agents/TEAM_NOTE_STAGE2_*`
- Document what you found (or state “no prior artifacts available”) in the same Stage diagnosis file and add the summary to the active Stage 2 team note. This keeps the request and response visible to all agents without human follow-up.

---

## Change Awareness

1. Before every evidence cycle, run:
   ```bash
   git status -sb
   git log -1 --oneline
   ls -1t .ai-agents/TEAM_NOTE_* 2>/dev/null | head
   ```
   to spot fresh instructions.
2. If a new Stage or Team note appears, read it fully before continuing.
3. When finished, record what changed (or if nothing changed) in the Stage diagnosis file and, if applicable, in `.ai-agents/TEAM_NOTE_STAGE2_EVIDENCE_READY_*`.

---

## Session Close

- Summarize the Present State → Desired Outcome status, list remaining gaps, and confirm the next action owner.
- If handing off, ensure `.ai-agents/handoff_log.txt` and the relevant Stage document clearly state what evidence exists and what is still outstanding.

Following this guide keeps the Codex Agent aligned with Terminal Codex and Cursor without requiring manual bridging by the human coordinator. Continuous logging in the shared Stage documents is the source of truth for every agent.

---

## Two-Agent Tandem Model

**Your Role (Codex Agent - Browser):**
- Open WhatIsMyDelta in fresh session
- Run DevTools checklist (initializer, auth modal, chat network, API base)
- Log console/network output into `.ai-agents/STAGE2_DIAGNOSIS_YYYY-MM-DD.md`
- Provide hard data for Terminal Codex to act on

**Terminal Codex Role:**
- Reads your evidence from Stage 2 diagnosis docs
- Implements fixes/tests based on your hard data
- Runs verify scripts
- Updates Stage 3 verification docs
- **No waiting on human relays** – acts directly on your evidence

**Workflow:**
1. You capture Stage 2 evidence (BEFORE code edits)
2. Terminal Codex reads your evidence and implements fixes
3. You confirm fixes in Stage 3 verification
4. Both agents stay aligned through staging notes (source of truth)

---

## Codex Reset Protocol

**When invoked:** Both agents re-run `.ai-agents/SESSION_START_PROTOCOL.md` Steps 1–5, restate Present State → Desired Outcome, and re-log the session.

**Your action:** When you see "Codex Reset Protocol", immediately:
1. Re-run session start protocol
2. Restate Present State → Desired Outcome
3. Write new entry to `.ai-agents/session_log.txt`
4. Resume with fresh context 
