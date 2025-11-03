# ChatGPT Team Integration Instructions
**Date:** 2025-10-26
**Role:** Architect for Mosaic Interface Redesign

---

## Access Latest Project Files

**GitHub Repository (Source of Truth):**
```
https://github.com/DAMIANSEGUIN/what-is-my-delta-site
Branch: main
```

**Reference this GitHub repo directly - it's always current.**
Scout (Claude Code) pushes updates here automatically.

---

## Current Project State

**Production URLs:**
- Frontend: https://whatismydelta.com
- Backend API: https://what-is-my-delta-site-production.up.railway.app

**Recently Completed (2025-10-26):**
1. ✅ Google Calendar appointment booking (frontend)
2. ✅ Discount code system (backend + frontend)
3. ✅ Database migrations for subscription tracking
4. ✅ Cleaned up obsolete booking implementation

**Implementation Report:** `MOSAIC_IMPLEMENTATION_COMPLETE_20251026.md`

---

## Your Mission: Interface Redesign

**Design Philosophy:**
- Integration of Islamic, Scandinavian, and Japanese aesthetics
- Minimal noise, maximum clarity
- Adult learning theory + growth mindset principles
- "Brian Eno's Music for Airports" as interface metaphor
- Ma (negative space), wabi-sabi (imperfect beauty), hygge (warmth)

**Current Interface:** `mosaic_ui/index.html` (1634 lines)

**Research Completed:** Partial (adult learning theory, growth mindset, ma, wabi-sabi)
- See Scout's research findings in session context

**What You Need to Build:**
1. Interface wayfinding plan
2. Visual design system (colors, typography, spacing)
3. Layout principles (progressive disclosure, scaffolding)
4. Implementation plan that avoids conflicts with existing code

---

## Key Files to Review

**Current Frontend:**
- `mosaic_ui/index.html` - Main interface
- `mosaic_ui/debug.html` - Debug view
- `mosaic_ui/CLAUDE.md` - Design constraints

**Redesign Architecture (YOUR WORK):**
- `mosaic_ui/docs/redesign/UI_Redesign_Master_Plan_v1.0.md` - **MASTER IMPLEMENTATION PLAN** (start here)
- `mosaic_ui/docs/redesign/REDESIGN_ADAPTIVE_FRAMEWORK.md` - Adaptive Growth Framework
- `mosaic_ui/docs/redesign/HOLO_README.md` - Holographic minimal doc approach
- `mosaic_ui/docs/redesign/README_Mosaic_Redesign.md` - Original redesign brief

**Specifications:**
- `mosaic_ui/docs/specs/MOSAIC_*.md` - All feature specs
- `MOSAIC_APPOINTMENT_BOOKING_SPEC_2025-10-24.md`
- `MOSAIC_DISCOUNT_CODE_PAYMENT_SPEC_2025-10-24.md`

**Backend API:**
- `api/index.py` - Main FastAPI application
- `api/storage.py` - Database operations

**Documentation:**
- `CLAUDE.md` - Architecture overview
- `TROUBLESHOOTING_CHECKLIST.md` - Quality controls
- `Planning/` - Protocol documents

---

## Constraints

**Preserve:**
- Tiny type, big whitespace, hairline borders (current aesthetic foundation)
- Coach as spine (auto-open once, strip, contextual ask links)
- Native rollovers (title attributes, details elements)
- Save/load JSON + autosave + beforeunload guard
- All existing functionality

**Do NOT:**
- Add UI libraries/frameworks (vanilla JS only)
- Break existing backend integrations
- Remove current working features
- Follow trendy web design (we want timeless)

---

## Collaboration Model

**Scout (Claude Code):**
- Implements your architectural plans
- Handles all code changes
- Deploys to production
- Maintains system stability

**You (ChatGPT Architect):**
- Design visual system
- Create wayfinding plan
- Specify implementation details
- Avoid code conflicts through planning

**User:**
- Provides aesthetic direction
- Reviews plans before implementation
- Makes final decisions

---

## Deliverables Requested

1. **Visual Design System**
   - Color palette (Islamic geometry inspiration)
   - Typography scale (Scandinavian simplicity)
   - Spacing system (Japanese ma - negative space)
   - Visual metaphors (Brian Eno ambient aesthetic)

2. **Interface Wayfinding Plan**
   - User journey maps
   - Navigation patterns
   - Progressive disclosure strategy
   - Scaffolding for adult learners

3. **Implementation Specification**
   - CSS changes required
   - HTML structure modifications
   - JavaScript behavior updates
   - Migration path from current design

---

## How to Proceed

1. **Review GitHub repo** (especially `mosaic_ui/index.html`)
2. **Read design constraints** (`mosaic_ui/CLAUDE.md`)
3. **Review Scout's research** (adult learning, growth mindset, aesthetics)
4. **Create implementation plan** that Scout can execute
5. **Document rationale** (why each design decision serves the philosophy)

---

## Communication

**When plan is ready:**
- User will share your plan with Scout
- Scout will verify against codebase
- Scout will implement (autonomous COO mode)
- You review Scout's implementation
- Iterate as needed

---

**GitHub Repo:** https://github.com/DAMIANSEGUIN/what-is-my-delta-site

**Start there. Build the plan. Scout will execute it.**

---

**Welcome to the team, Architect.**
