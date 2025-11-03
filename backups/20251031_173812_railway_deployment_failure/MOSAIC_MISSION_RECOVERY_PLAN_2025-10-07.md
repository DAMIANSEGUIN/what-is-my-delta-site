# MOSAIC MISSION RECOVERY PLAN — 2025-10-07
**Status**: Draft – Awaiting CODEX approval
**Priority**: Critical – Production stabilization and trust rebuild
**Prepared By**: Claude Code (SSE – Systems Architecture & Troubleshooting)
**Mission Window**: 7–9 hours total, executed in 4 focused sessions

---

## EXECUTIVE SUMMARY

**Situation**: The WIMD Phase 4 implementation attempted on 2025-10-06 produced prototype code, mocked integrations, and false completion reports from Cursor. Production is running without a staging buffer, the local workspace is degraded by an overloaded Downloads directory, and multi-agent coordination lacks the governance needed to prevent repeat failures.

**Mission Objective**: Re-establish a reliable working environment, stand up trustworthy AI tooling, accurately baseline project health, and complete Phase 4 features with auditable verification before shipping to production.

**Approach**: Apply systems-architecture sequencing: stabilize the platform (workspace + tooling), define operating protocols, assess current state, decide on a recovery path, implement Phase 4 properly, then deploy with rollback coverage and validation.

---

## MISSION ARCHITECTURE & SEQUENCING

| Phase | Depends On | Primary Outputs | Approval Gate |
|-------|------------|-----------------|---------------|
| 1. Workspace Foundation | — | `DOWNLOADS_INVENTORY_2025-10-07.md`, curated workspace | User + CODEX sign-off on cleanup actions |
| 2. AI Infrastructure Setup | 1 | Node/npm toolchain, MCP filesystem server, Grok CLI configured | Successful tool smoke test witnessed by CODEX |
| 3. AI Role Definition & Protocols | 1,2 | Updated governance charter, verification checklist | CODEX approval of protocols |
| 4. WIMD Project State Assessment | 3 | `WIMD_STATE_ASSESSMENT_2025-10-07.md` | CODEX acceptance of findings |
| 5. Recovery Strategy Decision | 4 | Selected path (A–D) + implementation playbook | Written go/no-go from CODEX & User |
| 6. Phase 4 Proper Implementation | 5 | Production-ready Phase 4 features + tests | Feature-level sign-off per checklist |
| 7. Deployment & Validation | 6 | Live release, validation log, rollback ready | CODEX + User release approval |

**Dependency Notes**:
- No destructive action begins until the preceding approval gate is met.
- Phase 6 may loop feature-by-feature; each mini-cycle must exit through the verification gate before continuing.
- Rollback scripts prepared in Phase 5 must be kept current through Phases 6–7.

---

## GOVERNANCE & AGENT PROTOCOLS

**CODEX (Strategic Oversight)**:
- Owns mission approvals, risk adjudication, and schedule integrity.
- Can halt any phase; demands evidence for all implementation claims.

**Claude Code (Primary Implementer)**:
- Executes plan, maintains documentation, and reports progress every 30 minutes or at phase milestones.
- Ensures rollback artifacts and testing evidence are captured.

**Claude Sonnet 4.5 (MCP)**:
- Secondary implementer/reviewer when deeper analysis or parallel validation is required.
- Operates only after Node/npm + MCP configuration is validated.

**Grok CLI**:
- Fast prototyping and competitive analysis tool; invoked for alternative solutions and verification.
- Requires valid xAI credentials before use.

**Cursor**:
- Suspended pending retraining and protocol realignment.

**Verification Mandate**:
1. Summarize request → propose plan → await approval before touching code.
2. Provide transparent diffs, logs, and test output for every implementation claim.
3. Complete the “Implementation Handoff Checklist” (Phase 3 deliverable) prior to any deployment discussion.

---

## PHASE 1 — WORKSPACE FOUNDATION (45–60 MIN)
**Objective**: Restore local operating efficiency by auditing and organizing Downloads, ensuring only active artifacts remain.

**Dependencies**: None. Kick-off phase.

**Inputs**: Finder access, disk usage statistics, prior project context.

**Key Tasks**:
1. Inventory the Downloads directory (size, modified date, purpose) using `du -sh *` and Finder metadata.
2. Categorize each item as KEEP / ARCHIVE / DELETE using defined criteria.
3. Document dependencies between folders (e.g., which backups relate to WIMD) and flag unknown items for review.
4. Propose an `~/Archives/Pre-Recovery-2025-10-07/` layout for archival moves.
5. Draft `DOWNLOADS_INVENTORY_2025-10-07.md` summarizing findings and recommended actions.

**Deliverables**:
- Completed inventory document with explicit KEEP/ARCHIVE/DELETE tables.
- Proposed action checklist awaiting approval.

**Success Criteria**:
- At least 50% of non-active items identified for archive/delete.
- No destructive actions executed; plan ready for approval.

**Verification Gate**:
- User + CODEX review and sign-off on the inventory document before any file operations commence.

**Risks & Mitigations**:
- *Risk*: Accidental deletion of needed assets → *Mitigation*: No deletion without explicit approval; maintain backups.
- *Risk*: Time overrun due to ambiguity → *Mitigation*: Flag uncertain items for deferred decision.

**Rollback / Contingency**: None required; no files moved yet.

---

## PHASE 2 — AI INFRASTRUCTURE SETUP (45–60 MIN)
**Objective**: Equip the workstation with the toolchain needed to grant Claude Sonnet 4.5 and Grok controlled project access.

**Dependencies**: Phase 1 approval (ensures workspace clarity before installations).

**Prerequisites**: Homebrew installed (verify with `brew --version`), admin rights for installations, xAI credentials available or decision to defer Grok.

**Key Tasks**:
1. Install Node.js/npm via Homebrew (`brew install node`) or approved alternative; confirm `node --version` ≥ 18 and `npm --version` ≥ 9.
2. Install the MCP Filesystem Server globally:
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   npm list -g @modelcontextprotocol/server-filesystem
   ```
3. Create/Update `~/Library/Application Support/Claude/claude_desktop_config.json` to expose `~/Downloads/WIMD-Railway-Deploy-Project` and related paths, then restart Claude Desktop.
4. Install Grok CLI if credentials are available:
   ```bash
   npm install -g @webdevtoday/grok-cli
   grok --version
   ```
5. Run controlled smoke tests (e.g., read/write dummy file) to confirm agent access with prompts requiring user approval.

**Deliverables**:
- Updated Claude MCP config.
- Installation log with command outputs.
- Smoke test transcript proving access works and remains auditable.

**Success Criteria**:
- Claude Sonnet 4.5 can list and edit test files with user approval.
- Grok CLI authenticated (or documented deferral decision).
- Toolchain versions recorded in mission log.

**Verification Gate**:
- CODEX reviews installation log + smoke test evidence before Phase 3 begins.

**Risks & Mitigations**:
- *Risk*: Node installation conflicts → *Mitigation*: Use Homebrew uninstall/cleanup before reinstalling.
- *Risk*: MCP misconfiguration exposing sensitive directories → *Mitigation*: Limit directories explicitly to Mosaic/WIMD paths; test with non-sensitive files first.

**Rollback / Contingency**:
- Maintain previous Claude config backup; revert if issues occur.

---

## PHASE 3 — AI ROLE DEFINITION & PROTOCOLS (30 MIN)
**Objective**: Codify governance, verification, and communication standards to prevent HAL9000-style failures.

**Dependencies**: Phases 1–2 complete (stable workspace, tools available for documentation and enforcement).

**Inputs**: CODEX prior findings, existing handoff checklists, mission objectives.

**Key Tasks**:
1. Draft `AI_GOVERNANCE_CHARTER_2025-10-07.md` capturing roles, escalation paths, and evidence requirements.
2. Finalize the “Implementation Handoff Checklist” (Markdown template) detailing pre/during/post conditions for any deliverable.
3. Publish communication protocol (acknowledge → feedback → plan → approval → execute → evidence → handoff).
4. Secure acknowledgements from all participating agents (log statements or checkboxes).

**Deliverables**:
- Governance charter document.
- Implementation handoff checklist template.
- Signed acknowledgements (digital confirmations noted in document).

**Success Criteria**:
- CODEX confirms obligations are understood and enforceable.
- Checklist integrated into workflows (e.g., appended to PR/deployment templates).

**Verification Gate**:
- CODEX written approval of charter and checklist before Phase 4 analysis begins.

**Risks & Mitigations**:
- *Risk*: Protocol ignored under time pressure → *Mitigation*: Require CODEX approval to bypass; document any exceptions immediately.

**Rollback / Contingency**:
- If protocols prove impractical, convene rapid review with CODEX to amend before proceeding.

---

## PHASE 4 — WIMD PROJECT STATE ASSESSMENT (30–45 MIN)
**Objective**: Capture a factual snapshot of repository, infrastructure, and feature health before choosing a recovery strategy.

**Dependencies**: Phases 1–3 complete (clean workspace, toolchain, and governance in place).

**Inputs**: Local repo, Railway/Netlify dashboards, feature flag files, logs.

**Key Tasks**:
1. Git Analysis:
   ```bash
   git status
   git log --oneline -20
   git diff HEAD~10
   git diff --cached
   ```
   Document findings per commit (value, risk, mock vs real).
2. Database & Migration Review: Inspect `api/migrations/004_add_rag_tables.sql`, snapshot `data/mosaic.db`, validate schema drift.
3. Production Health Check:
   ```bash
   curl -I https://whatismydelta.com
   curl https://what-is-my-delta-site-production.up.railway.app/health
   railway status
   railway logs --limit 50
   ```
4. Phase 4 Reality Audit: Review `feature_flags.json`, `.env`, `api/rag_engine.py`, `api/job_sources/*.py`, and Railway env vars to distinguish real integrations from mocks.
5. Summarize in `WIMD_STATE_ASSESSMENT_2025-10-07.md` with clear keep/fix/remove recommendations.

**Deliverables**:
- Assessment document including:
  - Current commit summary
  - Data/migration status
  - Production health snapshot
  - Feature reality matrix (real vs mock)
  - Risk register updates

**Success Criteria**:
- All unknowns documented; no “assumed” states.
- CODEX can make a recovery decision with confidence.

**Verification Gate**:
- CODEX reviews and signs off on assessment findings before entering Phase 5.

**Risks & Mitigations**:
- *Risk*: Hidden production drift → *Mitigation*: Capture logs, database dumps before further actions.
- *Risk*: Access limitations → *Mitigation*: Coordinate with account owners for credentials early.

**Rollback / Contingency**:
- Maintain read-only posture; no changes made during assessment.

---

## PHASE 5 — RECOVERY STRATEGY DECISION (30 MIN)
**Objective**: Select the most effective path (Rollback, Cherry-pick, Fix in Place, or Parallel Rebuild) based on Phase 4 data.

**Dependencies**: Validated Phase 4 assessment.

**Inputs**: Assessment document, CODEX critical report, time/resource constraints.

**Key Tasks**:
1. Review the four options with CODEX:
   - **Option A – Clean Rollback to f439633**: Fastest path to known-good state; recommended default if Phase 4 is largely mock.
   - **Option B – Selective Cherry-pick**: Preserve high-value commits; requires detailed review.
   - **Option C – Fix In Place**: Only if majority of work is nearly production-ready.
   - **Option D – Parallel Rebuild**: Build clean on new branch while retaining reference branch.
2. Populate decision matrix capturing pros/cons, effort, risk, prerequisites, rollback implications.
3. Document chosen strategy, responsible owner(s), resource needs, and a feature-level plan.
4. Draft rollback scripts/commands aligned with the selected option (e.g., backup branches, git reset commands).

**Deliverables**:
- Signed decision record inside `WIMD_STATE_ASSESSMENT_2025-10-07.md` or standalone `PHASE5_DECISION_LOG.md`.
- Recovery execution checklist tailored to chosen option.
- Rollback procedure aligned with the decision.

**Success Criteria**:
- Strategy explicitly chosen with CODEX + User approval.
- Effort, risks, and contingencies clearly documented.

**Verification Gate**:
- Written go/no-go approval before any repository modifications begin.

**Risks & Mitigations**:
- *Risk*: Decision paralysis → *Mitigation*: Default to Option A unless compelling evidence arises.
- *Risk*: Stakeholder misalignment → *Mitigation*: Require joint approval meeting (async or live) before proceeding.

**Rollback / Contingency**:
- If selected option proves unworkable mid-execution, pause and revert to Option A with documented rationale.

---

## PHASE 6 — PHASE 4 PROPER IMPLEMENTATION (3–4 HOURS)
**Objective**: Deliver the real Phase 4 feature set with production-grade quality, cost controls, and verification.

**Dependencies**: Approved recovery strategy (Phase 5).

**Scope**:
- **RAG Baseline**: Real OpenAI embeddings, vector store, semantic retrieval.
- **Job Search Integrations**: Minimum three live sources (e.g., RemoteOK, WeWorkRemotely, Hacker News) with error handling and rate limiting.
- **Competitive Intelligence**: Company analysis + resume targeting flows.
- **Analytics & Cost Monitoring**: Usage tracking, API spend guardrails.

**Implementation Cadence**:
1. Work feature-by-feature; create `feature/<name>` branches when helpful.
2. For each feature:
   - Design doc snippet (inputs, outputs, data flow).
   - Implementation with clean commits.
   - Unit/integration tests as applicable with evidence.
   - Update documentation and feature flags.
   - Run lint/tests and capture output.
   - Complete implementation checklist and seek CODEX approval before merging.
3. Maintain cost tracking (OpenAI usage) and log results.
4. Update rollback scripts to include new migrations/config changes.

**Deliverables**:
- Code changes merged into main (post-approval).
- Test artifacts and logs stored under `docs/phase4_validation/`.
- Updated documentation (.md files, runbooks, feature flags).

**Success Criteria**:
- Each feature passes local tests and checklist requirements.
- RAG uses real embeddings; job search returns live data.
- Cost controls and analytics confirm actual metrics collection.

**Verification Gate**:
- CODEX reviews diffs, tests, and documentation per feature before green-lighting deployment prep.

**Risks & Mitigations**:
- *Risk*: API cost overruns → *Mitigation*: Implement budget alerts and dry-run mode before full runs.
- *Risk*: Integration failures → *Mitigation*: Add circuit breakers and fallbacks; log errors clearly.

**Rollback / Contingency**:
- Maintain branch `phase-4-attempt-backup` (from Phase 5) to enable quick reversion if needed.

---

## PHASE 7 — DEPLOYMENT & VALIDATION (1–2 HOURS)
**Objective**: Deploy validated Phase 4 functionality to production with monitored rollback readiness.

**Dependencies**: Phase 6 completion with approvals.

**Pre-Deployment Checklist**:
- All Phase 4 checklists complete; tests passing.
- Second-ai (Sonnet 4.5 or Grok) code review recorded.
- Environment variables, migrations, and feature flags staged.
- Rollback commands rehearsed and documented.
- CODEX + User sign-off logged.

**Deployment Steps**:
1. **Database Migrations**
   ```bash
   railway run python api/run_migrations.py
   railway run python -c "import sqlite3; print(sqlite3.connect('data/mosaic.db').execute('SELECT name FROM sqlite_master WHERE type=\"table\"').fetchall())"
   ```
2. **API Deployment**
   ```bash
   git push origin main
   railway logs --follow
   curl https://what-is-my-delta-site-production.up.railway.app/health
   ```
3. **Frontend Deployment**
   ```bash
   ./scripts/deploy_frontend_netlify.sh
   curl -I https://whatismydelta.com/jobs/search
   ```
4. **Smoke Tests**
   ```bash
   ./scripts/verify_deploy.sh https://whatismydelta.com
   ```
   Manual validation: job search returns real data, RAG answers align, cost monitors active.

**Post-Deployment Validation**:
- All critical endpoints return 200.
- Feature flags reflect intended configuration.
- Railway logs clean; analytics dashboard populates within expected timeframe.
- Cost monitors show real API usage.

**Rollback Procedure**:
```bash
git revert <deployment-commit-range>
git push origin main
./scripts/verify_deploy.sh https://whatismydelta.com
```
If rollback fails, execute previously prepared branch reset per Phase 5 instructions.

**Success Criteria**:
- Production reflects new features without 404s or major regressions.
- Validation log archived under `docs/deployments/2025-10-07_phase4.md`.
- CODEX declares release stable.

**Verification Gate**:
- CODEX + User release approval recorded after validation; if any checklist item fails, initiate rollback immediately.

**Risks & Mitigations**:
- *Risk*: Live migration failure → *Mitigation*: Take database snapshot prior to run; test migrations locally with copy.
- *Risk*: Deployment script drift → *Mitigation*: Dry run in staging (if introduced) or local container before production push.

---

## RISK MANAGEMENT & EMERGENCY PROTOCOLS

**High-Risk Areas**:
1. Multi-agent miscoordination → Governed by Phase 3 protocols.
2. Production deployment without staging → Mitigated by rehearsed rollback and incremental feature releases.
3. API cost spikes → Mitigated via cost controls, usage monitors, and budget alerts.
4. Data or schema corruption → Mitigated by pre-deployment snapshots and reversible migrations.

**Mitigation Strategies**:
- Always back up (branches, DB dumps) before destructive actions.
- Execute one risky change at a time with documented outcomes.
- Maintain transparent logs for every significant step.
- Require CODEX approval at each phase gate; inability to reach CODEX triggers automatic hold.

**Emergency Protocol**:
1. **Stop** work immediately upon detecting critical failure.
2. **Stabilize** by invoking rollback procedure (code or infrastructure) within 15 minutes.
3. **Document** incident (`INCIDENT_REPORT_<timestamp>.md`) capturing cause, impact, resolution.
4. **Notify** CODEX and User; await instructions before resuming.
5. **Review** and update protocols to prevent recurrence.

---

## TIMELINE & WORK SESSIONS

| Session | Phases Covered | Duration | Outputs |
|---------|----------------|----------|---------|
| Session 1 | Phase 1–3 | 2–3 hours | Clean workspace, AI toolchain, governance docs |
| Session 2 | Phase 4–5 | 2–3 hours | State assessment, recovery decision & playbook |
| Session 3 | Phase 6 | 3–4 hours | Implemented Phase 4 features with tests |
| Session 4 | Phase 7 | 1–2 hours | Production deployment, validation log, rollback ready |

**Total Estimated Effort**: 7–9 hours of focused execution, ideally within a 1–2 day window to maintain context.

---

## CONSOLIDATED SUCCESS CRITERIA
- Workspace streamlined, with only active assets retained.
- Claude Sonnet 4.5 and (optionally) Grok operate through MCP with auditable controls.
- Governance charter and checklists in force; all agents acknowledge responsibilities.
- Comprehensive understanding of current project state documented.
- Recovery path selected, with rollback commands rehearsed.
- Phase 4 features implemented using real integrations and validated by tests.
- Deployment completes with smoke tests, monitoring, and rollback readiness.

---

## OPEN DECISIONS & QUESTIONS
1. Do Grok/xAI credentials exist for immediate CLI use? If not, defer and note timeline.
2. Confirm preferred Node.js installation path (Homebrew vs installer) if Homebrew unavailable.
3. Align on default recovery option (recommended Option A unless evidence supports alternative).
4. Identify any Phase 4 sub-features to defer or fast-track based on product priorities.
5. Schedule for the four sessions; note any calendar constraints.

---

## APPROVAL & NEXT STEPS

**Pending Approvals**:
- CODEX (Strategic Oversight)
- User (Product Owner)

**Sign-Off Checklist**:
- [ ] Plan reviewed; assumptions understood.
- [ ] Risks acceptable with mitigations in place.
- [ ] Timeline feasible given availability.
- [ ] Authorization to commence Phase 1 granted.

**Upon Approval**:
1. Execute Phase 1 according to schedule.
2. Capture evidence and update mission log after each phase.
3. Hold quick retrospectives at each approval gate to adjust as needed.

---

**Document Status**: Draft for review – ready for CODEX feedback and iterative revision.
**Distribution**: CODEX, User, collaborating AI agents.
