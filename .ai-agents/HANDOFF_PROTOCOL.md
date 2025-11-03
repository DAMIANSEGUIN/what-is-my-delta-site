# AI Agent Handoff Protocol

**CRITICAL: Run this checklist when ANY agent change occurs**

## Pre-Handoff (Outgoing Agent)

Before ending session, outgoing agent MUST:

- [ ] Run verification: `./scripts/verify_critical_features.sh`
- [ ] Generate handoff manifest: `./scripts/create_handoff_manifest.sh`
- [ ] Document current state in handoff file
- [ ] Commit any uncommitted work or create WIP commit

**Output:** `.ai-agents/handoff_YYYYMMDD_HHMMSS.json`

## Post-Handoff (Incoming Agent)

**MANDATORY FIRST ACTIONS - Before ANY code changes:**

1. **Read handoff manifest:**
   ```bash
   cat .ai-agents/handoff_*.json | tail -1
   ```

2. **Verify critical features:**
   ```bash
   ./scripts/verify_critical_features.sh
   ```
   - If this fails: STOP. Do not proceed. Escalate to human.

3. **Acknowledge critical features:**
   ```
   I confirm the following features are present and MUST BE PRESERVED:
   - Authentication UI (authModal, loginForm, registerForm)
   - PS101 v2 flow (PS101State references)
   - API_BASE configuration (relative paths)
   - [Any other features listed in manifest]
   ```

4. **Check for existing issues:**
   - Read recent commits: `git log -5 --oneline`
   - Check deployment status: `curl https://whatismydelta.com/health`
   - Review any URGENT_* files in repo

## Handoff Failure Response

**If verification fails:**

```bash
❌ STOP - Do not make code changes
⚠️  Escalate to human with message:
"Critical feature verification failed during handoff.
 Run ./scripts/verify_critical_features.sh for details."
```

## Critical Features List (Current)

These features CANNOT be removed without explicit human approval:

1. **Authentication System**
   - UI: Login/register modals
   - Backend: /auth/* endpoints
   - Session management

2. **PS101 v2 Flow**
   - 10-step problem-solving sequence
   - Experiment components
   - State persistence

3. **API Integration**
   - API_BASE = '' (relative paths)
   - Netlify proxy configuration
   - Railway backend endpoints

4. **Core Functionality**
   - Chat interface
   - File upload
   - Job search (when enabled)

## Emergency Handoff (Agent Unavailable)

If primary agent crashes/unavailable:

1. Human creates: `.ai-agents/emergency_handoff.txt`
2. Backup agent reads emergency handoff
3. Backup agent runs: `./scripts/verify_critical_features.sh`
4. Backup agent operates in **CONSERVATIVE MODE**:
   - No file replacements
   - No architectural changes
   - Bug fixes only with verification
   - All changes require human review before commit

## Handoff Log

Document all handoffs in: `.ai-agents/handoff_log.txt`

Format:
```
[TIMESTAMP] [OUTGOING_AGENT] → [INCOMING_AGENT]
Reason: [Why handoff occurred]
Status: [Success/Failed]
Issues: [Any problems during handoff]
```
