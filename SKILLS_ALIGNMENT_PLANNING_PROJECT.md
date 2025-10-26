# Skills Library Alignment for Planning Project
**Date:** 2025-10-25
**Purpose:** Map custom Claude Skills to Planning Project workflows and agent coordination

---

## Skills Library Catalog

### Extracted Skills (10 total)

1. **Agentic Development** - Conversational guidance for building with AI agents
2. **Prompting Pattern Library** - Comprehensive prompting patterns and frameworks
3. **Requirements Elicitation** - Bridge PM docs to technical implementation
4. **Job Search Strategist** - Job search strategy and application tactics
5. **Resume Builder** - Resume creation and optimization
6. **AI Pitch Deck Builder** - Pitch deck creation
7. **AI Vendor Evaluation** - Vendor assessment framework
8. **Excel Automation** - Complex Excel automation
9. **Excel Editing** - XLSX editing workflows
10. **Vibe Coding** - Coding workflow patterns

---

## High-Priority Skills for Planning Project Integration

### 1. **Agentic Development** ⭐⭐⭐⭐⭐
**Alignment:** PERFECT FIT - Core methodology for Planning Project

**Key Principles That Apply:**
- "Just Talk To It" - Natural conversation over elaborate frameworks
- Parallel agents in one folder (CLI, Browser, Desktop running simultaneously)
- Interrupting agents is standard practice
- Context manager pattern (already using in WIMD project)
- Screenshots as 50% of context engineering
- Agent files as organizational scar tissue (SESSION_START.md, etc.)
- Blast radius thinking (estimate file impact before changes)

**How to Integrate:**
- Replace elaborate planning systems with conversational approach
- Formalize parallel agent coordination (3-8 agents in WIMD-Railway-Deploy-Project)
- Create .claude/agent-instructions.md following organic evolution principle
- Implement screenshot-first debugging protocol
- Establish interruption checkpoints in long-running tasks

**Immediate Application:**
- Google Calendar booking: estimate blast radius (3 files: index.html, backend API, config)
- Interface skin tweaks: use screenshots to communicate design intent
- Skills templates: grow organically from actual pain points, not upfront architecture

---

### 2. **Prompting Pattern Library** ⭐⭐⭐⭐⭐
**Alignment:** CRITICAL - Foundation for all agent communication

**Key Patterns for Planning Project:**
- **Chain-of-Thought (CoT)**: Request step-by-step reasoning before changes
- **Few-Shot Learning**: Provide examples of desired task completion
- **Structured Output**: Enforce JSON/Markdown formats for consistency
- **Reflection**: Ask agents to critique their own output before finalizing
- **Decomposition**: Break complex tasks into smaller sub-tasks

**Current Usage Gaps:**
- Not using explicit CoT prompts (relying on implicit reasoning)
- No few-shot examples in SESSION_START.md
- Inconsistent structured output requirements
- Missing reflection loops (post-deployment verification)

**How to Integrate:**
- Add CoT trigger to SESSION_START.md: "Before making changes, explain your reasoning step-by-step"
- Create /examples/ folder with few-shot examples of common tasks
- Enforce structured output in DEPLOYMENT_FAILSAFES_PROTOCOL.md
- Add reflection checkpoint: "Review your changes and identify potential issues"

**References to Use:**
- `/references/prompt-patterns.md` - Full pattern catalog
- `/references/failure-modes.md` - Common failures and fixes
- `/references/model-quirks.md` - Claude vs GPT optimization

---

### 3. **Requirements Elicitation** ⭐⭐⭐⭐
**Alignment:** STRONG - Bridges Planning Project specs to implementation

**Core Philosophy Match:**
"ELICIT, DON'T INVENT" - Exactly what Planning Project needs

**5-Phase Framework:**
1. **Initial Analysis** - Read full document, identify what IS specified
2. **Question Generation** - Organized by stakeholder (PM vs Engineering)
3. **Risk Assessment** - Critical/High/Medium/Low severity
4. **Output Creation** - Gap analysis + clarifying questions
5. **Post-Clarification** - Only after conversation, create tech specs

**Current Planning Project Gaps:**
- Jumping straight to implementation without eliciting requirements
- Making assumptions about technical details
- No systematic gap analysis before starting

**How to Integrate:**
- Add Phase 1 checklist to SESSION_START.md
- Create /templates/gap_analysis_template.md
- Create /templates/clarifying_questions_template.md
- Enforce "ELICIT, DON'T INVENT" in agent instructions

**Immediate Application:**
- Google Calendar booking: Run Phase 1-2 before coding
  - What booking scenarios? (1-on-1, group, recurring?)
  - Calendar provider? (Google only? Outlook? Both?)
  - Timezone handling? User preferences?
  - Conflict resolution? Double-booking prevention?

---

### 4. **Job Search Strategist** ⭐⭐⭐
**Alignment:** DOMAIN-SPECIFIC - Directly supports WIMD/Mosaic mission

**Relevant for WIMD Platform:**
- Phase 1: Deep job posting analysis (already core WIMD feature)
- Phase 2: Conversational skills-matching (PS101 flow)
- Phase 3: Skill development strategy (coaching layer)
- Phase 4: Creative application strategy (resume optimization)

**WIMD Feature Gaps This Reveals:**
- Missing red/green flag detection in job postings
- No company culture research integration
- Limited skills-matching conversation depth
- No portfolio/proof development guidance

**How to Integrate into WIMD:**
- Add `/references/job-posting-flags.md` to prompt library
- Enhance PS101 flow with Phase 2 interview structure
- Add Phase 3 skill development roadmap to coaching
- Integrate Phase 4 application tactics to resume builder

**Planning Project Use:**
- Use Phase 2 conversational interview as template for agent elicitation
- Adapt "cultural fit" assessment to "technical fit" for tasks
- Apply weighted prioritization model (40/40/20) to task selection

---

### 5. **Vibe Coding** ⭐⭐⭐
**Alignment:** MODERATE - Coding workflow patterns

**Need to Review:**
- `/references/prompt-patterns.md` - Coding-specific patterns
- `/references/security-checklist.md` - Security best practices
- `/references/tool-comparison.md` - Tool selection guidance

**Potential Application:**
- Security checklist for WIMD deployment
- Tool comparison for Planning Project agent selection
- Coding prompt patterns for complex features

---

## Skills NOT Prioritized (Lower Relevance)

### 6. Resume Builder ⭐⭐
- **Relevance:** Medium - WIMD feature, but already implemented
- **Action:** Review for potential WIMD enhancements, not Planning Project

### 7. AI Pitch Deck Builder ⭐
- **Relevance:** Low - Not directly applicable
- **Action:** Archive for future reference

### 8. AI Vendor Evaluation ⭐
- **Relevance:** Low - Not current need
- **Action:** Archive for future reference

### 9. Excel Automation ⭐
- **Relevance:** Low - Not applicable to current stack
- **Action:** Archive for future reference

### 10. Excel Editing ⭐
- **Relevance:** Low - Not applicable to current stack
- **Action:** Archive for future reference

---

## Integration Roadmap

### Immediate (This Session)
1. **Apply Agentic Development principles to Google Calendar booking**
   - Estimate blast radius before starting
   - Use screenshots for UI spec
   - Allow interruption/steering during implementation

2. **Apply Requirements Elicitation to booking feature**
   - Run Phase 1-2: Elicit requirements before coding
   - Create gap analysis document
   - Generate clarifying questions list

3. **Use Prompting Pattern Library for interface tweaks**
   - Provide few-shot examples of desired aesthetic
   - Request CoT reasoning for design decisions
   - Enforce structured output (before/after screenshots)

### Short-Term (Next 7 Days)
1. **Create Planning Project Agent Instructions File**
   - Based on Agentic Development principles
   - Organic evolution model (add as pain points arise)
   - Git instructions for parallel agent workflows
   - Preferred patterns (context manager, PostgreSQL syntax)
   - Error handling conventions

2. **Build Prompt Pattern Library for WIMD**
   - Extract patterns from custom skills
   - Create /prompts/patterns/ directory
   - Document failure modes specific to WIMD

3. **Integrate Job Search Strategist into WIMD Feature Roadmap**
   - Add red/green flag detection
   - Enhance PS101 conversational depth
   - Build skill development roadmap feature

### Medium-Term (Next 30 Days)
1. **Create Claude Skills for Planning Project**
   - Session initialization skill (enforces SESSION_START.md)
   - Deployment workflow skill (automates fail-safe protocol)
   - Git safety skill (prevents dangerous operations)
   - Agent coordination skill (standardizes CLI/Browser/Desktop interaction)

2. **Formalize Requirements Elicitation Protocol**
   - Add to TEAM_ORCHESTRATION_README.md
   - Create templates in Planning folder
   - Train all agents on ELICIT, DON'T INVENT principle

3. **Audit WIMD Against Job Search Strategist Framework**
   - Gap analysis: missing features
   - Prioritization: high-impact additions
   - Implementation plan: phased integration

---

## Skills Template Structure for Planning Project

### Template Format (Based on Agentic Development + Requirements Elicitation)

```markdown
---
name: [skill-name]
description: [when to use this skill]
trigger_phrases: [user phrases that activate skill]
---

# [Skill Name]

## Core Philosophy
[1-2 sentence principle - e.g., "ELICIT, DON'T INVENT"]

## When to Use This Skill
[Specific scenarios, trigger phrases]

## Workflow
[Sequential phases with clear deliverables]

## Reference Files
[Bundled knowledge: checklists, templates, examples]

## Best Practices
[Dos and don'ts, common pitfalls]

## Integration with Planning Project
[How this skill connects to team workflows]
```

### Skills to Create for Planning Project

1. **session-initialization**
   - Enforces SESSION_START.md checklist
   - Loads relevant documentation
   - Verifies prerequisites
   - Sets context for agent role

2. **deployment-workflow**
   - Baseline snapshot
   - Safety checkpoint
   - Incremental commit
   - Health verification
   - Rollback plan

3. **git-safety**
   - Context manager pattern check
   - PostgreSQL syntax validation
   - Idempotent operation check
   - Pre-push safety verification

4. **requirements-elicitation** (adapt existing skill)
   - 5-phase framework
   - Gap analysis
   - Clarifying questions
   - Risk assessment
   - ELICIT, DON'T INVENT

5. **agent-coordination**
   - Parallel agent management
   - Blast radius estimation
   - Interruption protocol
   - Handoff documentation
   - Context preservation

---

## Key Takeaways

### From Agentic Development:
- **"Just Talk To It"** - Conversation beats ceremony
- **Parallel agents** - 3-8 agents in one folder
- **Screenshots** - 50% of context engineering
- **Interruption** - Agents are interruptible and resumable
- **Organic evolution** - Agent files grow from pain points

### From Prompting Pattern Library:
- **CoT for critical tasks** - Step-by-step reasoning
- **Few-shot examples** - Show don't tell
- **Structured output** - Consistency through templates
- **Reflection loops** - Self-critique before finalization

### From Requirements Elicitation:
- **ELICIT, DON'T INVENT** - Ask questions, don't assume
- **5-phase framework** - Systematic gap analysis
- **Risk assessment** - Critical/High/Medium/Low
- **Stakeholder organization** - PM vs Engineering questions

### From Job Search Strategist:
- **Research-driven** - Web search for non-obvious insights
- **Weighted prioritization** - 40/40/20 model
- **Conversational interview** - Elicit through dialogue
- **Measurable** - KPIs and pipeline tracking

---

## Next Steps

1. **Review Skills References** (read detailed docs):
   - Agentic Development: No additional refs (all in SKILL.md)
   - Prompting Pattern Library: Read `/references/prompt-patterns.md`
   - Requirements Elicitation: Read `/references/technical_dimensions.md`, `/references/question_templates.md`
   - Job Search Strategist: Read `/references/job-posting-flags.md`, `/references/templates-and-examples.md`

2. **Apply to Current Tasks**:
   - Google Calendar booking: Run requirements elicitation first
   - Interface tweaks: Use screenshots + CoT prompting
   - Skills creation: Follow agentic development organic growth

3. **Create Planning Project Skills**:
   - Start with session-initialization (highest ROI)
   - Add deployment-workflow (prevents data loss)
   - Build git-safety (enforces patterns)

4. **Document Integration**:
   - Update TEAM_ORCHESTRATION_README.md with skills references
   - Add skills library path to SESSION_START.md
   - Create /skills/ directory in Planning folder

---

**END OF SKILLS ALIGNMENT DOCUMENT**
