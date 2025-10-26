# Mosaic Redesign – Adaptive Growth Framework (README)
**Role**: Lead AI Interface Architect — user experience for learning environments, calm/adaptive experimental design.

**Rubric Key (for retrieval by any AI/human):** `Mosaic_Redesign_AdaptiveFramework_v1`  
**Created:** 2025-10-26 17:20:55

## Purpose
This README is the hand-off map for developers and AI agents. It points to canonical files and describes how the adaptive UI architecture morphs to fit the user experience on the fly while staying minimalist.

## Canonical Locations (Google Drive titles to search)
Use Drive search by **exact title** or the **tags** below. Keep this README with the backup zip.

- **Strategic_Systems_Integration_Plan_v0.2**  
  *Tags:* mosaic, architecture, integration, roadmap, watchdog
- **README_Plan_Archive_v1.1_full**  
  *Tags:* restoration, hierarchy, backup, canonical
- **Planning_Responses_Rebuild_v1.2**  
  *Tags:* system-memory, responses, continuity
- **Career_Pathing_Prompts**  
  *Tags:* reflection, evidence, resume, narrative
- **START Planning_Checklist_16.10.25**  
  *Tags:* planning, sequence, foundation, v2.0 systems map
- **Nate_Skills_Framework_v3.1.pdf**  
  *Tags:* adaptive growth, ergonomics, economic psychology, cultural cognition, self-efficacy
- **Nate_Skills_Framework_Notes_Mosaic_v2.pdf**  
  *Tags:* growth-state UX, reflective, deliberate, generative, integrative
- **Nate_Skills_Design_Cognition.pdf**  
  *Tags:* cognitive ergonomics, calm tech, futurism
- **Nate_Skills_Objective_Matrix.xlsx**  
  *Tags:* weighting, optimism, systems thinking, design anthropology

> Index these items under the rubric key above in any knowledge base or agent memory.

## Backup Rules
- Include this README and the manifest.json in all Mosaic backups.
- Mirror files to both **Mosaic/** and **Planning/** Drive collections.
- Preserve original titles and add the rubric key to each file’s description or first page.

## Adaptive Architecture (Yes — morphing on the fly is feasible)
We use a **Sense → Decide → Render** loop with minimal, composable parts. This keeps code small while adapting UX density and tone to user state.

### Sense (lightweight telemetry)
- Signals: `backtrack`, `idle_time`, `errors`, `task_duration`, optional `self_reported_state`.
- Store per-session aggregates (e.g., last 5 min) in a slim table.

Schema (suggested):

```
telemetry(session_id, t, event, value)
ux_state(session_id, state, since, reason)
```

### Decide (finite state machine + flags)
- **State machine (XState or equivalent):** `calm` → `focus` → `recovery` → `explore`  
- Transitions by thresholds, e.g., ≥3 backtracks/2min → `recovery`.
- **Feature flags (Unleash/OSS):** toggle density, helper reveal, guided mode without code forks.

### Render (tokens not branches)
- One layout; **design tokens** swap by state:
  - `focus`: +8% font, −40% choices, muted accent, fewer affordances.
  - `recovery`: slower easing (220–280ms), increased whitespace, optional breathing prompt.
  - `explore`: additional branches and suggestions enabled.
- Components: unstyled primitives (e.g., Radix) + Tailwind utility tokens.

### Pseudo API (thin, adaptable)
```
GET  /ux/state        → { state, since }
POST /ux/signal       → { event, value }
GET  /flags           → { guided_mode, dense_cards, reveal_helper }
GET  /copy?key=...    → { text }
GET  /prompts?mode=.. → { items: [...] }
```
**No spaghetti:** UI reads `state` + `flags`, then applies tokens.

## Minimal Stack (suggested)
- **UI primitives:** Radix (or native) + Tailwind
- **State:** XState (or reducer pattern) for clarity
- **Flags:** Unleash OSS
- **Data:** Postgres (Supabase) or Hasura GraphQL façade
- **Observability:** privacy-first analytics (dwell time, not surveillance)
- **Content:** Headless CMS (Strapi) for prompts/copy—edit without redeploys

## Design Heuristics (calm, Islamic × Scandinavian × Japanese × Eno)
- One focus region per screen; secondary actions in a single popover.
- Fade > slide; 220–280ms cubic-bezier(0.45,0.05,0.55,0.95).
- Accent hue may drift slowly with session length (never flashing).
- Asymmetric balance with abundant **ma** (negative space).
- Rhythm through repeating geometric ratios (1:√2) rather than ornament.

## Implementation Order (fast path)
1. Wireframe monochrome (test spacing & rhythm).  
2. Add tokens + states (no flags yet).  
3. Add feature flags for *Guided vs Standard*.  
4. Log 4 signals and flip states live.  
5. Only then consider AI-streamed “guided reveal” components.

## Versioning
- Version this README alongside manifest.json.
- Semantic versions for UX tokens (`ux-tokens@1.x.y`) and state machine (`ux-sm@1.x.y`).

---
**Questions / Extensions**: adopt a “quiet systems” palette, integrate day/night tone shift, or add HITL “reflection checkpoints” for mastery logging without friction.

