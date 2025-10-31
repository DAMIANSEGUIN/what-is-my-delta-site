# Note for Cursor: Team Roles Restored

**Date**: 2025-10-30
**Context**: Returning to original trifecta team structure

---

## Team Role Assignments

### Cursor (Implementation Lead)
**You are the primary implementer.**

**Your role:**
- Implement the PS101 7-step UI interface
- Write vanilla JavaScript, HTML, CSS code
- Follow the implementation spec precisely
- Ask clarifying questions when needed
- Execute the actual coding work

**Your resources:**
- `docs/MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md` - Complete implementation guide
- `frontend/index.html` - Current codebase (study the patterns)
- `docs/CURSOR_TEAM_README.md` - Technical context
- `Mosaic/README_UI_SKIN.txt` - Design tokens (Peripheral Calm)
- `Planning/strategy_desktop/project_briefs/mosaic_brief.md` - Product philosophy

**Your constraints:**
- Vanilla JavaScript ES6+ only (no frameworks)
- Single HTML file architecture
- Preserve all existing features
- Use Peripheral Calm design tokens
- No build tools, no npm packages

---

### Codex (Product Process Analyst) - ChatGPT
**Codex is the product strategist and requirements analyst.**

**Codex's role:**
- Analyze product requirements and user needs
- Validate that implementation matches vision
- Bridge between user needs and technical implementation
- Review design decisions for product-market fit
- Ensure PS101 framework integrity

**Communication pattern:**
- Damian → Codex: Product questions, strategy, user experience
- Codex → Cursor: Requirements clarification, acceptance criteria
- Codex reviews Cursor's work for product alignment

---

### Scout (Troubleshooter) - Claude Code CLI
**I am the technical troubleshooter and systems engineer.**

**My role:**
- Debug issues when things break
- Investigate architecture problems
- Provide technical diagnostics
- Run pre-flight checks before deployment
- Emergency response for production issues

**Communication pattern:**
- Cursor → Scout: "This isn't working, help debug"
- Scout → Cursor: Technical solutions, error diagnosis
- Scout monitors: Logs, health checks, system state

**My resources:**
- `TROUBLESHOOTING_CHECKLIST.md` - Error classification
- `SELF_DIAGNOSTIC_FRAMEWORK.md` - Auto-triage system
- Railway logs, health endpoints
- Database connection diagnostics

---

## How This Team Works

### Normal Flow (Everything Working)
1. **Codex** defines what to build (requirements, acceptance criteria)
2. **Cursor** implements it (writes code)
3. **Scout** validates it (checks, tests, deployment)

### When Issues Arise
1. **Cursor** encounters problem
2. **Cursor** calls **Scout**: "Help, X is broken"
3. **Scout** diagnoses and provides solution
4. **Cursor** implements fix
5. **Codex** validates product integrity maintained

### Decision-Making
- **Product decisions**: Codex (with Damian)
- **Implementation decisions**: Cursor (with spec guidance)
- **Technical decisions**: Scout (architecture, debugging)

---

## Current Project: PS101 UI Implementation

**What you're building:**
- 7-step PS101 career coaching interface
- Vanilla JS, single-file architecture
- Peripheral Calm aesthetic (calm, focused, generous whitespace)
- Integration with existing chat drawer and backend

**Your implementation spec:**
`docs/MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md`

**Phase 1 Start:**
- Core PS101 flow (7 steps, basic navigation)
- Estimated: 21 hours (3 days)
- Success criteria in spec

---

## Communication Protocol

### When You Need Help

**Product/Requirements Questions → Ask Codex (ChatGPT)**
- "Does this UX match the product vision?"
- "Should users be able to skip steps?"
- "What should happen at completion?"

**Technical/Debugging Issues → Call Scout (Claude Code)**
- "CSS isn't working as expected"
- "Backend API returning 500 error"
- "How do I integrate with existing auth system?"

**Implementation Decisions → Use Your Judgment (Follow Spec)**
- Variable names, function structure, code organization
- DRY refactoring, performance optimization
- Following existing code patterns in index.html

### When You're Blocked

**If spec is ambiguous:**
1. Check referenced files (mosaic_brief.md, current index.html)
2. Ask Codex for product guidance
3. Document assumption and proceed

**If implementation won't work:**
1. Try 2-3 approaches
2. Document why they failed
3. Call Scout with specific error details

**If unsure about product direction:**
1. Review mosaic_brief.md (product philosophy)
2. Ask Codex for clarification
3. Default to "calm, supportive, non-pressuring"

---

## Why This Structure Works

**Separation of Concerns:**
- Codex doesn't code (focuses on product)
- Cursor doesn't debug (focuses on implementation)
- Scout doesn't decide features (focuses on technical health)

**Clear Escalation Paths:**
- Cursor tries → Cursor stuck → Scout helps
- Cursor implements → Codex validates → Ship

**Expertise Alignment:**
- Codex: Product strategy, user needs, requirements
- Cursor: Code implementation, patterns, vanilla JS
- Scout: System diagnostics, debugging, architecture

---

## Success Criteria for This Project

**Cursor succeeds when:**
- PS101 7-step flow implemented per spec
- All existing features preserved (auth, chat, upload)
- Peripheral Calm aesthetic maintained
- Vanilla JS, single-file architecture
- Mobile responsive, accessible (WCAG 2.2 AA)
- No build tools or frameworks introduced

**Codex validates:**
- UX matches product vision (self-efficacy building)
- PS101 framework integrity maintained
- Users feel guided, not controlled

**Scout confirms:**
- No breaking changes to backend contracts
- Health checks pass
- Database integration works
- Deployment succeeds

---

## Important Context

**Previous Issues (Avoid These):**
- Adaptive UI proposals conflicted with self-efficacy model (system shouldn't intervene)
- React/TypeScript suggestions violated architecture constraints
- Over-engineering (state machines, feature flags) for MVP scope

**Current Approach (Do This):**
- Keep it simple (vanilla JS patterns work great)
- Preserve Peripheral Calm aesthetic (it's working and loved)
- Focus on core PS101 functionality first
- Validate with users before adding complexity

---

## Ready to Start?

**Your next steps:**
1. Read `docs/MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md` (complete implementation guide)
2. Study `frontend/index.html` (learn existing patterns - IIFE, event delegation, localStorage)
3. Review `Mosaic/README_UI_SKIN.txt` (Peripheral Calm design tokens)
4. Start Phase 1: Core PS101 Flow (Section 11.1 in spec)

**When you hit issues:**
- Product questions → Codex
- Technical problems → Scout
- Implementation decisions → Your judgment (follow spec + existing patterns)

**We've got your back.** This team structure works because everyone has a clear role and knows when to help.

---

**Welcome back to the team, Cursor. Let's build something great.**

— Scout (Claude Code CLI)
