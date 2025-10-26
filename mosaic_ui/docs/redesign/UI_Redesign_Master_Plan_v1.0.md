# Mosaic Interface Redesign — **Master Plan** (v1.0)

Prepared_by: GPT-5 (SSE)
Reviewed_by: Claude_Code (Implementation Lead)
Approved_by: Damian Seguin (Project Lead)
Date: 2025-10-26

---

## 0) Canon & Scope

**Canonical root:** `~/Mosaic/`  
**Planning location:** `~/Mosaic/Planning/` (mirrored to `Drive:/Mosaic/Planning/`)  
**This file:** `UI_Redesign_Master_Plan_v1.0.md` — the *single* source for UI redesign scope, rules, and hand‑off to implementation.

**Do first (preflight for all AIs):**
1. Read `~/Mosaic/manifest.json` and confirm directories + rules.
2. Confirm `~/Mosaic/Documentation/task_registry.json` exists.
3. Obey `never_edit_in_place = true`; create new files/branches, archive on replace.

---

## 1) Objectives

1. Maintain **Alpha/Main** (stable) and add **Beta** (experimental) UI in parallel.
2. Ship a **Channel Chooser** so learners (and testers) can pick **Standard** or **Beta** without changing task flow.
3. Implement Adaptive Growth visual layer: calm-tech motion, tokenized themes, reflection timing **after** task completion.
4. Meet adult‑learning, a11y, and performance targets without altering IA or API contracts.

---

## 2) Design Principles (Scandi × Japanese × Islamic, adult-learning)

- One focus region per screen; generous *ma* (deliberate negative space).
- Minimalist grid (8pt) and 1:√2 modular type scale (target 66–72ch text width).
- Subtle geometric lattice in headers/dividers at 1–2% contrast for wayfinding (Islamic pattern logic, not decoration).
- Motion: 220–280ms fades; respect `prefers-reduced-motion` → 80ms.
- Tone: neutral, competence-oriented microcopy; no praise inflation.
- A11y: WCAG 2.2 AA, explicit focus rings (2px/4px offset), targets ≥ 40×40px.

---

## 3) Architecture & Contracts (unchanged)

**APIs (read-only for UI):**
- `GET /ux/state -> {state, since, reason}`
- `POST /ux/signal -> {event, value}`
- `GET /flags -> {guided_mode, dense_cards, reveal_helper}`
- `GET /copy?key=… -> {text}`

**States (XState):** `calm`, `focus`, `recovery`, `explore`  
**Window:** rolling 120s (10s hop)  
**Guards:**  
- `STRUGGLE` if `backtrack>=3 || errors>=2 || idle>=45000`  
- `STABLE_FOCUS` if `task_duration>=90s && errors==0`  
- `COMPLETE→explore` when completion then `open_suggestions` ≤ 30s  
**Dwell:** min 20s between transitions

---

## 4) Tokenized Skin (no component forks)

Use CSS variables; apply per‑state overrides via `body[data-state="…"]`.

```css
:root{
  --mx-font-base:16px; --mx-line:1.55; --mx-radius:16px; --mx-stroke:1.5px;
  --mx-surface-0:oklch(98% 0 0); --mx-surface-1:oklch(96% .01 230);
  --mx-text:oklch(28% .03 230); --mx-muted:oklch(60% .02 230);
  --mx-accent:oklch(65% .10 220); --mx-focus-ring:oklch(55% .12 220);
  --mx-ease:cubic-bezier(.45,.05,.55,.95); --mx-duration:240ms;
  --mx-lattice:conic-gradient(from 45deg at 50% 50%,transparent 0 88%,oklch(30% .02 230 / .02) 0 100%);
}
body[data-state="focus"]{--mx-font-base:17.3px;--mx-duration:220ms;--mx-accent:oklch(60% .08 220);}
body[data-state="recovery"]{--mx-duration:280ms;--mx-line:1.65;--mx-surface-1:oklch(97% .01 230);}
body[data-state="explore"]{--mx-surface-1:oklch(95% .02 230);--mx-accent:oklch(68% .12 220);}
```

**Components:** AppBar (with faint lattice), ProgressRail (circle/hex/square outlines), StepCard (single region), SupportPopover, ReflectionCard (post‑completion), ChannelChooser.

---

## 5) Channel Chooser (user‑facing)

**UX:** Settings → Appearance (“Experience Mode: Standard | Beta”).  
**Rules:**  
- No mid‑task switches: defer until step end.  
- Precedence: URL `?channel=` → account pref → localStorage → Unleash cohort → env default.  
**Telemetry:** log `channel_resolved` and `channel_set` with `{channel, source}` and tag all subsequent events.

---

## 6) Deliverables (implementation package)

**Files (repo paths illustrative):**
```
/components/ChannelChooser.tsx
/components/UxFrame.tsx
/components/ProgressRail.tsx
/lib/fsm.ts
/lib/channel.ts
/styles/tokens.css
/content/copy.json              # standard + guided variants
/config/unleash.json            # feature_channel beta, guided_mode
/docs/observability.md          # event dictionary, sampling, retention
/docs/a11y-checks.md            # focus order, contrast matrix, motion policy
```

**Copy keys (examples):**  
- `resume_guided_intro`, `resume_focus_hint`, `recovery_breath_prompt`, `explore_suggestions_title` (each has `standard`/`guided`).

---

## 7) Acceptance Criteria (Definition of Done)

- Dual-mode UI loads via Channel Chooser; selection persists and is reversible.  
- No IA or route changes; APIs untouched.  
- FSM fixtures pass (all states & guards) and dwell prevents flapping.  
- Token swaps produce visual deltas without component conditionals.  
- A11y Lighthouse ≥ 95; `prefers-reduced-motion` honored.  
- Telemetry cleanly separates `channel` and `source`; p95 error parity with Alpha.  
- README & file paths comply with `manifest.json`; no writes outside canon.

---

## 8) File Governance & Backups

- Before first commit: run `~/Mosaic/bin/mosaic_preflight.command`. Fail if manifest/registry missing.  
- Archive any non‑canonical `README*` to `~/Mosaic/Archive/old_readmes_YYYYMMDD/`.  
- Create a dated ZIP in `~/Mosaic/Backups/` on each Beta iteration.

---

## 9) Timeline (10 days)

- D1–D2: Branch + scaffolds + tokens + chooser
- D3–D5: Copy keys, motion tuning, reflection timing
- D6–D7: A11y + perf + fixtures
- D8–D9: Beta cohort enablement + smoke
- D10: Review metrics; merge token learnings

---

## 10) Risks & Mitigations

- Token drift → lock `ux-tokens@1.0.x` snapshots  
- State flapping → enforce 20s dwell + guard debouncing  
- Learner fatigue → reflection frequency caps + opt‑out Beta

---

## 11) Handoff Notes for Claude_Code

- Treat this file as **the** implementation scope.
- Confirm manifest presence and task registry entry before coding.
- Use *tokens over branches*; keep IA/API as-is.
- Submit PR: “Mosaic UI – Secondary Beta Build (Guided/Motion/Reflection)” with screenshots of all states.

---
