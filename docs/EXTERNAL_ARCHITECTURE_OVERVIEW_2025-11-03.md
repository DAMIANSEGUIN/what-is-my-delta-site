# What Is My Delta – PS101 v2 Architecture & Operations Brief

**Date:** 2025-11-03  
**Prepared by:** Codex (Architecture & Process Lead)  
**Audience:** External stakeholders, partner engineering teams, AI governance reviewers

---

## 1. Project Snapshot
- **Product:** PS101 v2 problem-solving journey for the What Is My Delta platform
- **Goal:** Deliver a 10-step guided career decision experience with experiment tracking, inline validation, and lightweight coaching tools
- **Deployment Targets:**  
  - Netlify (static frontend)  
  - Railway (Python backend/API)
- **Delivery Constraint:** Maintain incumbent single-file architecture (`frontend/index.html`, mirrored to `mosaic_ui/index.html`)

---

## 2. System Architecture Overview
| Layer | Description | Key Artifacts |
| --- | --- | --- |
| **Frontend** | Single HTML file with embedded CSS/JS. Implements full PS101 journey, experiment framework, authentication modal, chat, uploads, and inline validation. | `frontend/index.html`, `mosaic_ui/index.html` |
| **State Management** | LocalStorage-backed state object (`ps101_v2_state`) with multi-prompt answers, experiment log, auto-save indicators, and migration from v1. | `frontend/index.html:1917` onwards |
| **Backend Integration** | REST calls via `API_BASE` (resolved through `ensureConfig()`), plus session-aware helpers (`callJson`, `authenticateUser`, `uploadToWimd`). | `frontend/index.html:1729-2140` |
| **AI/Coaching** | Hybrid approach: local CSV prompt matching + Railway `/wimd` API for fallbacks. Voice input supported when browser APIs available. | `frontend/index.html:1004-1470` |
| **Authentication** | Modal rendered beneath nav, supporting login, register, password reset, and logout with session persistence + trial gating. | `frontend/index.html:280-356`, `frontend/index.html:1729-2140` |
| **Experiment Toolkit** | Steps 6–9 expose experiment canvas, obstacles, actions, reflection with inline validation; tied into PS101 state. | `frontend/index.html:544-914`, `frontend/index.html:3092-3350` |

**Design Guardrails**
- Peripheral Calm aesthetic (Decision #007) — high whitespace, neutral palette, unobtrusive transitions.
- Inline validation pattern (Decision #003) — error spans below inputs; no browser alerts in new work.
- Multi-prompt progression (Decision #008) — sequential prompts with progress dots and autosave indicators.

Reference: `docs/ARCHITECTURAL_DECISIONS.md`

---

## 3. AI Delivery Team & Responsibilities
| Agent | Focus | Core Responsibilities |
| --- | --- | --- |
| **Codex** | Product & Process Lead | Drafts canonical specs (`docs/PS101_CANONICAL_SPEC_V2.md`), owns protocol stack, performs post-implementation audits, and maintains architectural decisions. |
| **Cursor** | Implementation Reviewer | Performs pre-flight reviews (`CURSOR_REVIEW_DEPLOYMENT_ENFORCEMENT.md`), validates code integrations, and flags specification drift. |
| **Claude_Code** | Systems Operator | Executes shell-level tasks, implements deployment automation (`DEPLOYMENT_ENFORCEMENT_IMPLEMENTATION_COMPLETE.md`), and runs enforcement scripts. |

**Alignment Protocols**
- `./ai-agents/SESSION_START_PROTOCOL.md` – mandatory kickoff routine (critical feature check, handoffs, activity review).
- `./ai-agents/COMMUNICATION_PROTOCOL.md` – response expectations, prioritised behaviours, and escalation language.
- `NOTE_FOR_CURSOR_AND_CLAUDE_CODE_2025-10-27.md` – shared source of truth for cross-agent status updates.

---

## 4. Verification & Testing Stack
| Stage | Script / Artefact | Purpose |
| --- | --- | --- |
| **Critical Feature Gate** | `scripts/verify_critical_features.sh` | Confirms auth UI, PS101 flow, API_BASE configuration, and production heartbeat before any work proceeds. |
| **Pre-Push Guard** | `scripts/pre_push_verification.sh` | Wraps sanity checks, content validation, and git-tree hygiene. Invoked automatically by tracked pre-push hook. |
| **Deployment Verification** | `scripts/verify_live_deployment.sh` | Validates live Netlify deployment (line counts, title, auth, PS101). Used post-deploy and during automation. |
| **Manual Checklist** | `DEPLOYMENT_CHECKLIST.md` | Human-friendly checklist with common failure modes, wrapper command usage, and rollback notes. |

**CI Roadmap:** `.github/workflows/deploy-verification.yml` mirrors local enforcement once GitHub secrets are supplied.

---

## 5. Tool-Augmented Deployment Enforcement
Implemented on 2025-11-03 (Claude_Code with Cursor review), documented in `DEPLOYMENT_ENFORCEMENT_IMPLEMENTATION_COMPLETE.md`.

| Layer | Implementation | Notes |
| --- | --- | --- |
| **Tracked Git Hook** | `.githooks/pre-push` (activated via `scripts/setup_hooks.sh`) | Blocks pushes to `railway-origin` unless verification passes. Bypass allowed only with `SKIP_VERIFICATION=true` + reason (logged to `.verification_audit.log`). |
| **Wrapper Commands** | `scripts/push.sh`, `scripts/deploy.sh` | Enforces verification, standardises deploy flows, and integrates logging. Replaces raw `git push` / `netlify deploy`. |
| **Automation** | `.github/workflows/deploy-verification.yml` | CI pipeline aligning with local checks; awaits credentials before activation. |
| **Documentation Reinforcement** | Updates across `.ai-agents/SESSION_START_PROTOCOL.md`, `.ai-agents/COMMUNICATION_PROTOCOL.md`, `DEPLOYMENT_CHECKLIST.md`, `CLAUDE.md` | Redirects agents to wrappers and clarifies forbidden commands. |

---

## 6. Incident Summary – Alignment Failures
| Date | Incident | Root Cause | Reference |
| --- | --- | --- | --- |
| 2025-11-03 | Authentication loss after rollback | Claude_Code restored snapshot `890d2bc` without verifying features; auth modal removed, triggering blocking incident. | `docs/incidents/2025-11-03_AUTH_LOSS_RECOVERY.md` |
| 2025-11-03 | Spec drift warning | Cursor raised alarm: verification doc initially contradictory (claimed auth missing then “safe to deploy”), requiring clarification. | `docs/incidents/2025-11-03_SPEC_VERIFICATION.md` |
| 2025-11-03 | Merge paralysis | Cursor’s handoff (`URGENT_TEAM_HANDOFF.md`) reported inability to merge auth into new UI due to tool/context limits; session halted pending human review. | `URGENT_TEAM_HANDOFF.md` |
| 2025-11-03 | Post-handoff merge | Cursor later executed auth merge successfully (`docs/AUTH_MERGE_EXECUTION_2025-11-03.md`), but left logout controls hidden; Codex audit restored them pre-deploy. | `docs/AUTH_MERGE_EXECUTION_2025-11-03.md` |

**Key Lessons**
1. Spec alignment and verification must be automated (hence enforcement stack).
2. Agent handoffs need explicit instructions (`SESSION_START_PROTOCOL`, `URGENT_TEAM_HANDOFF.md`).
3. Human oversight remains essential for contextual judgement (e.g., logout UI regression).

---

## 7. Document Library & Paths
| Topic | File | Path |
| --- | --- | --- |
| Product specification | `docs/PS101_CANONICAL_SPEC_V2.md` | `docs/PS101_CANONICAL_SPEC_V2.md` |
| Architecture decisions | `docs/ARCHITECTURAL_DECISIONS.md` | `docs/ARCHITECTURAL_DECISIONS.md` |
| Alignment protocols | `./ai-agents/SESSION_START_PROTOCOL.md`, `./ai-agents/COMMUNICATION_PROTOCOL.md` | `.ai-agents/SESSION_START_PROTOCOL.md`, `.ai-agents/COMMUNICATION_PROTOCOL.md` |
| Inline validation standard | `docs/PS101_INLINE_VALIDATION_PROTOCOL.md` | `docs/PS101_INLINE_VALIDATION_PROTOCOL.md` |
| Deployment enforcement plan | `docs/DEPLOYMENT_AUTOMATION_ENFORCEMENT_PLAN.md` | `docs/DEPLOYMENT_AUTOMATION_ENFORCEMENT_PLAN.md` |
| Enforcement implementation log | `DEPLOYMENT_ENFORCEMENT_IMPLEMENTATION_COMPLETE.md` | `DEPLOYMENT_ENFORCEMENT_IMPLEMENTATION_COMPLETE.md` |
| Auth merge execution | `docs/AUTH_MERGE_EXECUTION_2025-11-03.md` | `docs/AUTH_MERGE_EXECUTION_2025-11-03.md` |
| Urgent handoff narrative | `URGENT_TEAM_HANDOFF.md` | `URGENT_TEAM_HANDOFF.md` |
| Incident retrospectives | `docs/incidents/2025-11-03_AUTH_LOSS_RECOVERY.md`, `docs/incidents/2025-11-03_SPEC_VERIFICATION.md`, `docs/incidents/2025-11-03_VERSION_ANALYSIS.md` | See paths |
| Verification scripts | `scripts/verify_critical_features.sh`, `scripts/pre_push_verification.sh`, `scripts/verify_live_deployment.sh` | Under `scripts/` |

**Packaging for External Share**
```bash
# create compressed bundle of key docs
mkdir -p dist
tar -czf dist/WIMD_PS101_Architecture_Pack_2025-11-03.tgz \
  docs/EXTERNAL_ARCHITECTURE_OVERVIEW_2025-11-03.md \
  docs/PS101_CANONICAL_SPEC_V2.md \
  docs/ARCHITECTURAL_DECISIONS.md \
  docs/PS101_INLINE_VALIDATION_PROTOCOL.md \
  docs/DEPLOYMENT_AUTOMATION_ENFORCEMENT_PLAN.md \
  DEPLOYMENT_ENFORCEMENT_IMPLEMENTATION_COMPLETE.md \
  docs/AUTH_MERGE_EXECUTION_2025-11-03.md \
  URGENT_TEAM_HANDOFF.md \
  docs/incidents/2025-11-03_AUTH_LOSS_RECOVERY.md \
  docs/incidents/2025-11-03_SPEC_VERIFICATION.md \
  scripts/verify_critical_features.sh \
  scripts/pre_push_verification.sh \
  scripts/verify_live_deployment.sh
```
Upload `dist/WIMD_PS101_Architecture_Pack_2025-11-03.tgz` to your preferred sharing layer (e.g., Google Drive, S3, internal portal) and distribute the link.

---

## 8. Current Status & Next Actions
- ✅ Auth integrated into PS101 v2 (file size ~3,873 lines mirrored across frontend + marketing shell).
- ✅ Deployment enforcement stack operational locally; awaiting GitHub secrets to activate CI enforcement.
- ✅ Logout controls restored and visible alongside session badge.
- 🔄 Documentation cleanup still in progress (`docs/incidents/2025-11-03_VERSION_ANALYSIS.md` requires completion).
- 🔄 Remediation backlog: replace residual `alert()/confirm()` usage per `docs/PS101_INLINE_VALIDATION_PROTOCOL.md`.

**Recommended Next Steps**
1. **Final Verification & Deploy:** Run wrapper scripts, verify live site, monitor Netlify deploy.
2. **CI Enablement:** Populate Netlify secrets in GitHub and enable `.github/workflows/deploy-verification.yml`.
3. **Protocol Refresh:** Circulate this brief + associated bundle to external reviewers; ensure all agents acknowledge.
4. **Incident Follow-Up:** Close out pending analyses (`docs/incidents/2025-11-03_VERSION_ANALYSIS.md`) to prevent regression.

---

*For questions or escalation, contact Codex or refer to the incident reports listed above.*

