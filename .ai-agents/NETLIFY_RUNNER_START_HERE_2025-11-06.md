# Netlify Agent Runner – Start Here (2025-11-06)

**Welcome, Netlify Agent Runner (NAR)!** This note directs you to the essential documentation for completing the deployment task.

---

## 📖 Primary Documentation

### 1. **Main Project README**
**File:** `README.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/README.md`  
**Purpose:** Project overview, quick start, safety protocols, and essential documentation links  
**Start here for:** General project context and architecture understanding

### 2. **Complete File Reference** (NEW)
**File:** `.ai-agents/NETLIFY_RUNNER_FILE_REFERENCE_2025-11-06.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/NETLIFY_RUNNER_FILE_REFERENCE_2025-11-06.md`  
**Purpose:** **Complete list of all files with exact paths** - deployment scripts, verification scripts, source files, config files, documentation  
**Start here for:** Finding specific files and their exact locations

### 3. **Deployment Handoff Instructions**
**File:** `.ai-agents/HANDOFF_NETLIFY_RUNNER_2025-11-06.md`  
**Path:** `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/.ai-agents/HANDOFF_NETLIFY_RUNNER_2025-11-06.md`  
**Purpose:** Step-by-step execution instructions for the current deployment task  
**Start here for:** What to do right now

---

## 🚀 Quick Start Path

**If you're ready to deploy immediately:**

1. **Read the handoff note:**
   ```bash
   cat .ai-agents/HANDOFF_NETLIFY_RUNNER_2025-11-06.md
   ```

2. **Reference file locations:**
   ```bash
   cat .ai-agents/NETLIFY_RUNNER_FILE_REFERENCE_2025-11-06.md
   ```

3. **Follow execution steps** from the handoff note

**If you need project context first:**

1. **Read the main README:**
   ```bash
   cat README.md
   ```

2. **Then proceed to handoff note** and file reference

---

## 📋 Current Task Summary

**Objective:** Deploy consolidated frontend build (commit `0c44e11`) to Netlify production

**Blocker Resolved:** Terminal Codex had EPERM error - you should have proper Netlify CLI permissions

**Key Files:**
- Source: `mosaic_ui/index.html` (consolidated build with `initApp` + auth button fix)
- Deploy script: `scripts/deploy_frontend_netlify.sh`
- Verify script: `scripts/verify_live_deployment.sh`
- Config: `netlify.toml`

**Expected Outcome:** Production serves 3,989-line bundle (currently serving 3,992-line old bundle)

---

## 🔍 Finding Files

**All file paths are documented in:**
- `.ai-agents/NETLIFY_RUNNER_FILE_REFERENCE_2025-11-06.md`

**Quick access:**
```bash
cd /Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project
ls -la scripts/                    # Deployment scripts
ls -la mosaic_ui/                 # Frontend source
ls -la .ai-agents/                # Documentation
cat netlify.toml                  # Netlify configuration
```

---

## ⚠️ Important Notes

- **Verification Rule:** Never mark something as "working" or "fixed" until manual browser verification confirms it works in production
- **Current Production:** Still serving old bundle (expected until you deploy)
- **Site ID:** `NETLIFY_SITE_ID=resonant-crostata-90b706`
- **Production URL:** https://whatismydelta.com

---

## 📚 Additional Resources

**Netlify-Specific README (may be outdated):**
- `NETLIFY_AGENT_RUNNER_README.md` (from October 2025 - check workspace path)

**Session Protocols:**
- `.ai-agents/SESSION_START_PROTOCOL.md` - Mandatory AI agent checklist
- `.ai-agents/NEXT_SESSION_START_HERE.md` - Quick session reference

**Recovery Guides:**
- `Mosaic_Production_UI_Recovery_Playbook_2025-11-06.md` - Comprehensive recovery procedures
- `Mosaic_Deployment_Wrapper_Recovery_Guide_2025-11-06.md` - Git clean state recovery

---

## ✅ Post-Deployment Checklist

After deployment succeeds:

1. Wait 60-90 seconds for CDN propagation
2. Run: `./scripts/verify_live_deployment.sh | tee -a .verification_audit.log`
3. Perform manual browser checks (see handoff note Step 6)
4. Log results in `.verification_audit.log`
5. Update `.ai-agents/STAGE3_VERIFICATION_2025-11-05.md`
6. **DO NOT mark as "fixed" until manual verification confirms all checks pass**

---

**Start with:** `.ai-agents/HANDOFF_NETLIFY_RUNNER_2025-11-06.md`  
**Reference files:** `.ai-agents/NETLIFY_RUNNER_FILE_REFERENCE_2025-11-06.md`  
**Project context:** `README.md`

**Good luck with the deployment!**

---

**End of Start Here Note – 2025-11-06**

