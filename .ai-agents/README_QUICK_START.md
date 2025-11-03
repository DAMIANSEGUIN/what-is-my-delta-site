# AI Agent Contingency System - Quick Start

**INSTALLED: November 2, 2025**

## What This Does

Prevents AI agents from breaking critical features (like the authentication removal incident).

## For Humans: Starting a New AI Session

**Paste this to ANY new AI agent:**

```
Read and follow: .ai-agents/AI_AGENT_PROMPT.md

This project has mandatory protocols. You MUST run verification before proceeding.
```

That's it. The AI will handle the rest.

## For AI Agents: Your First Actions

**1. Run verification (MANDATORY):**
```bash
./scripts/verify_critical_features.sh
```

**2. If it passes, declare:**
```
✅ Verification passed
✅ Critical features confirmed:
   - Authentication: [count]
   - PS101: [count]
   - API: [status]

I will preserve these features.
```

**3. If it fails:**
```
❌ CRITICAL: Verification failed
🚨 Blocking all work until resolved
```

**4. Read the protocols:**
- `.ai-agents/SESSION_START_PROTOCOL.md`
- `.ai-agents/HANDOFF_PROTOCOL.md`

## What's Protected

- **Authentication UI** (login/register modals)
- **PS101 v2 flow** (10-step problem-solving)
- **API configuration** (relative paths for Netlify proxy)
- **Core functionality** (chat, upload, job search)

## How It Works

**Layer 1: Pre-commit Hook**
- Blocks commits that remove critical features
- Runs automatically on `git commit`

**Layer 2: Verification Script**
- Checks critical features present
- Run before any deploy

**Layer 3: Agent Protocols**
- Session start checklist
- Handoff procedures
- Operating rules

## Testing

**Test the system:**
```bash
# Should show current status (auth missing locally, but present in prod)
./scripts/verify_critical_features.sh

# Should create handoff manifest
./scripts/create_handoff_manifest.sh

# Try to commit removal of auth (will be BLOCKED)
# Create test file, remove auth, try to commit - hook will stop it
```

## When Agent Fails/Changes

**Outgoing agent:**
```bash
./scripts/create_handoff_manifest.sh > .ai-agents/handoff_$(date +%Y%m%d_%H%M%S).json
```

**Incoming agent:**
```bash
# Find latest handoff
ls -t .ai-agents/handoff_*.json | head -1

# Read it and verify
cat [handoff_file]
./scripts/verify_critical_features.sh
```

## Emergency Override

Only with explicit human approval:
```bash
git commit --no-verify -m "[EMERGENCY-OVERRIDE] reason"
```

Then immediately:
```bash
./scripts/verify_critical_features.sh
```

## Files Created

```
.ai-agents/
├── AI_AGENT_PROMPT.md              # Copy/paste to new AI sessions
├── SESSION_START_PROTOCOL.md       # Full session start procedure
├── HANDOFF_PROTOCOL.md             # Agent handoff procedure
├── README_QUICK_START.md           # This file
└── handoff_*.json                  # Handoff manifests (generated)

scripts/
├── verify_critical_features.sh     # Checks critical features present
└── create_handoff_manifest.sh      # Creates handoff state snapshot

.git/hooks/
└── pre-commit                      # UPDATED with feature removal blocking
```

## Current Status

✅ **Installed and Active**
- Pre-commit hook blocking feature removal
- Verification script working
- Protocols documented
- Handoff system ready

⚠️ **Known Issue**
- Authentication UI missing from local files (frontend/ and mosaic_ui/)
- Needs restoration from backup or git history
- This is the issue that prompted creating this system

## Next Steps

1. **Restore authentication** (separate task)
2. **Test with controlled agent handoff**
3. **Monitor for first real handoff**
4. **Iterate based on real-world usage**

---

**Questions?** Read `.ai-agents/SESSION_START_PROTOCOL.md` for full details.
