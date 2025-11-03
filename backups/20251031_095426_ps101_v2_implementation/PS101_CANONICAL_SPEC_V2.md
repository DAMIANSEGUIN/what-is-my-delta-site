# PS101 Canonical Experience Specification (v2)

**Author:** Codex (Product Process Analyst)  
**Date:** 2025-10-30  
**Scope:** Corrected product specification for Cursor implementation — replaces `MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md`  
**Status:** FINAL for Build Approval  

---

## 1. Purpose & Success Criteria

- Deliver the canonical **10-step** PS101 problem-solving journey captured in `frontend/assets/PS101_Intro_and_Prompts.docx` / `api/ps101_flow.py`.
- Ship the **Small Experiments Framework** (Steps 6–9) **Day 1** — experiment design, tracking, reflection, and mastery must be usable in the first release.
- Preserve Mosaic’s **Peripheral Calm** aesthetic while maintaining the existing single-file, vanilla JS architecture (`frontend/index.html` + localStorage/back-end integration).
- Achieve MOSAIC success metrics: **Clarity +3**, **Action >7**, **Momentum >7** (tracked via existing metrics cards).
- Maintain current auth/chat/upload capabilities without regression.

---

## 2. Canonical PS101 Journey

The PS101 journey is a 10-step linear flow. Each step comprises **multiple prompts** (3–6) that guide deeper thinking. These prompts are non-negotiable — they are the canonical script.

| Step | Title | Purpose | Prompt Set (exact text) |
| --- | --- | --- | --- |
| 1 | Problem Identification and Delta Analysis | Define the core challenge and the delta between current and desired state | 1. What specific challenge are you currently facing in your personal or professional life?<br>2. Why is it a problem?<br>3. Reduce this to a simple problem statement.<br>4. If you were to wake up tomorrow and this problem was solved, what would be different? (Miracle Question)<br>5. What is the "delta" or gap between your current situation and your desired state?<br>6. How would solving this problem align with your long-term goals or values? |
| 2 | Current Situation Analysis | Capture context, attempted solutions, and impact | 1. Describe your current situation in detail. What factors are contributing to the problem?<br>2. What attempts have you made so far to address this issue? What were the outcomes?<br>3. Are there any patterns or recurring themes you've noticed related to this problem?<br>4. How is this problem affecting different areas of your life (e.g., career, relationships, personal growth)? |
| 3 | Root Cause Exploration | Surface assumptions and underlying causes | 1. What do you believe are the underlying causes of this problem?<br>2. Are there any assumptions you're making about the problem or its causes?<br>3. How might your own beliefs, habits, or past experiences be contributing to the situation?<br>4. If you were to view this problem from an outsider's perspective, what insights might you gain? |
| 4 | Self-Efficacy Assessment | Gauge confidence and existing assets | 1. On a scale of 1-10, how confident do you feel in your ability to solve this problem? Why?<br>2. What past experiences or skills can you draw upon to address this challenge?<br>3. How might your perception of your own capabilities be influencing your approach to this problem?<br>4. What small wins or successes have you had in the past that you can build upon? |
| 5 | Solution Brainstorming | Generate a wide field of options | 1. List at least five potential solutions to your problem, no matter how unconventional they may seem.<br>2. For each solution, what are the potential benefits and drawbacks?<br>3. Which solution feels most aligned with your values and long-term goals?<br>4. How might you combine elements from different solutions to create a more comprehensive approach? |
| 6 | Experimental Design | Design the first experiment (Small Experiments entry point) | 1. Based on your chosen solution(s), what small, low-risk experiment could you conduct to test its effectiveness?<br>2. What specific, measurable outcome would indicate that your experiment was successful?<br>3. What resources or support might you need to carry out this experiment?<br>4. How long will you run this experiment before evaluating its results? |
| 7 | Obstacle Identification | Anticipate blockers and mitigation | 1. What external factors (e.g., time, resources, other people) might hinder your progress?<br>2. What internal obstacles (e.g., self-doubt, fear, lack of knowledge) do you anticipate facing?<br>3. For each obstacle identified, brainstorm at least one strategy to overcome or mitigate it.<br>4. How can you reframe these obstacles as opportunities for growth or learning? |
| 8 | Action Planning | Convert experiment into step-by-step plan | 1. What specific steps will you take to implement your chosen experiment?<br>2. How will you measure and track your progress throughout the experiment?<br>3. What milestones can you set to celebrate small wins along the way?<br>4. Who can you enlist to provide support or accountability during this process? |
| 9 | Reflection and Iteration | Integrate experiment results | 1. After conducting your experiment, what were the results? What did you learn?<br>2. How has this experience affected your confidence in problem-solving?<br>3. Based on what you've learned, what adjustments would you make to your approach?<br>4. What new experiments or actions will you take based on these insights? |
| 10 | Building Mastery and Self-Efficacy | Reinforce momentum and future application | 1. Reflecting on this problem-solving process, what new skills or knowledge have you gained?<br>2. How can you apply what you've learned to future challenges or goals?<br>3. What strategies will you use to maintain momentum and continue building your problem-solving abilities?<br>4. How has this experience changed your perception of your own capabilities? |

---

## 3. Interaction Model

### 3.1 Multi-Prompt Experience (Micro-Step Pattern)
- Each PS101 step renders as a **card with stacked sub-prompts** (numbered 1..n).
- For focus, show one prompt at a time with gentle advance:
  1. Active prompt visible with textarea input and character counter.
  2. Upon meeting minimum character threshold (per prompt, default 30 chars unless specified), “Next prompt” button unlocks.
  3. Completed prompts collapse into a summary chip (`Prompt 2 ✓`) that can be re-opened for edits.
- Visual cues:
  - Step progress indicator (10 dots) at top.
  - Sub-prompt mini-progress (e.g., `Prompt 3 of 4`) below question header.
  - Smooth 180–220ms fade transitions to maintain Peripheral Calm.
- Autosave after each prompt completion to localStorage (and backend when available) with a subtle inline “Saved • 12:41” indicator (ARIA live region polite).

### 3.2 Navigation
- **Primary**: “Next Step →” enabled only after all prompts in current step meet validation.
- **Secondary**: “← Previous Step” always available.
- **Prompt Re-entry**: Inline “Edit” links in the step summary and in the completion dashboard reopen any prompt in-place without resetting later data.
- **Progress Dots**: Ten dot buttons with states:
  - Completed (filled)
  - Current (outlined with inner dot, `aria-current="step"`)
  - Upcoming (outline only; disabled until reached)
- Keyboard support: Arrow keys move between prompts within a step; Tab order respects prompt sequence.

### 3.3 Peripheral Calm Visuals
- Reuse root token palette (`frontend/index.html:6-30`). Any new colors derive from existing vars (`--fg`, `--muted`, `--line`, `--hair`).
- Generous whitespace, calm typography (system sans @ 13–15px). Avoid bold reds; use neutral greys for error states and soft amber (#f5d48a) highlight token for focus, matching Mosaic minimal UI cues.

---

## 4. Small Experiments Framework — Day 1 Deliverable

The Small Experiments Framework is woven through Steps 6–9 and culminates in Step 10. Ship the following components now:

### 4.1 Experiment Canvas (Step 6 Primary Output)
- **Captured Fields:**
  - Experiment name (auto-suggest `Experiment 1` editable)
  - Hypothesis statement (textarea)
  - Success metric (measurable outcome)
  - Duration/start & review date pickers (fallback: free-form text if date picker unavailable)
  - Required resources/support (textarea)
- Upon completing Step 6 prompts, render a structured experiment card summarizing these fields.
- Allow multiple experiments (user can add another experiment card if Step 5 produced multiple options). Additional experiments stay in backlog but mark one as “Active”.

### 4.2 Obstacle Mapping (Step 7)
- Link obstacles to the active experiment:
  - Capture external/internal obstacles as tagged list.
  - Strategy textarea per obstacle (paired inputs).
  - Display them within the experiment card (“Obstacle: Time — Strategy: Block 30-minute focus sprints”).

### 4.3 Action Plan (Step 8)
- Convert experiment into a checklist:
  - Step-by-step tasks (minimum 3) with target dates.
  - Progress tracking toggle (checkbox) with timestamp when marked complete.
  - Accountability assignment (free text + optional email for future integrations).
- Checklist persists within the experiment card (localStorage structure described in §5).

### 4.4 Reflection Log (Step 9)
- Post-experiment log fields:
  - Outcomes (rich textarea)
  - Learning summary
  - Confidence delta (numeric slider 1–10, prefilled from Step 4 value for comparison)
  - Next iteration decision: `Continue`, `Pivot`, `Archive`
- Logging a reflection automatically archives completed tasks and marks experiment stage to “Reviewed”.

### 4.5 Mastery Dashboard (Step 10)
- Present aggregated view:
  - Key skills gained (user input from Step 10 prompts).
  - Momentum tracker (auto-calc Action/Momentum metrics vs baseline).
  - “Next experiment” suggestion button prefilled with insights from Step 9.
  - Summary export (JSON blob prepared for future download/email).

---

## 5. State & Data Model

### 5.1 Local State (Browser)
- Store in `localStorage` under `ps101_v2_state`.
```json
{
  "currentStep": 4,
  "currentPromptIndex": 2,
  "steps": {
    "1": {
      "prompts": [
        {"response": "...", "completedAt": "2025-10-30T19:55:00Z"},
        ...
      ]
    },
    ...
  },
  "experiments": [
    {
      "id": "exp-001",
      "title": "Experiment 1",
      "hypothesis": "...",
      "successMetric": "...",
      "duration": {"start": "...", "review": "..."},
      "resources": "...",
      "obstacles": [
        {"type": "external", "label": "Time", "strategy": "..."}
      ],
      "actions": [
        {"label": "Schedule 30-min block", "due": "2025-11-02", "done": false}
      ],
      "reflection": {
        "outcome": "...",
        "learning": "...",
        "confidence": {"before": 5, "after": 7},
        "nextMove": "Continue"
      },
      "status": "active"
    }
  ],
  "startedAt": "2025-10-30T19:50:00Z",
  "lastUpdated": "2025-10-30T20:05:12Z",
  "completionScores": {"clarity": 8, "action": 8, "momentum": 7}
}
```

### 5.2 Backend Integration
- When user is authenticated, sync state through existing `/wimd/ask` pipeline (payload extension to include `experiments` array).
- Debounce network writes (1s) and show inline status (“Syncing… / Saved”).
- Preserve compatibility with existing chat flow; share `experiments[0]` summary with coach prompts to enable contextual nudges (Phase 3).

---

## 6. Validation Rules

- Each prompt requires minimum 30 characters (unless prompt naturally needs more — Step 1 prompt 1 minimum 50 chars, Step 5 prompt 1 minimum 100).
- Experiments:
  - Must have hypothesis + success metric + duration before Step 6 marked complete.
  - At least one obstacle and one mitigation strategy required in Step 7.
  - Step 8 needs three actionable tasks with distinct labels.
  - Step 9 requires reflection text + confidence score update.
- Prevent advancing to Step 10 until reflection logged.
- Completion screen displays status badges: `Experiment designed`, `Action plan ready`, `Reflection logged`.

---

## 7. Accessibility Checklist

- Announce step changes via `aria-live="assertive"` on `#step-label`.
- Sub-prompt navigation uses buttons with `aria-controls` pointing to textarea.
- Experiment cards use `<section>` with `aria-labelledby`.
- Ensure all controls reachable via keyboard; focus states use 2px high-contrast outline.
- Provide descriptive error text (e.g., “Please add a success metric before continuing”).

---

## 8. Implementation Roadmap (Cursor)

1. **State Layer Upgrade**
   - Extend PS101 state object to handle multi-prompt responses and experiment data.
2. **UI Rebuild**
   - Replace 7-step container with dynamic 10-step + sub-prompt scaffolding.
   - Implement experiment canvas / obstacle mapper / checklist / reflection components.
3. **Autosave & Validation**
   - Hook each prompt completion and experiment field change to autosave.
4. **Completion Dashboard**
   - Build Step 10 view summarizing entire journey + experiment outcomes.
5. **Regression Pass**
   - Confirm existing modules (metrics cards, chat, uploads) remain intact.

Total estimated effort: 40–48 engineer hours (core flow + experiments).

---

## 9. Outstanding Items (Post-Day-1 Planning)

Track but do not block current build:
- Delta visualization (graphical representation of gap)
- Explore/Exploit balancing tools
- Proactive coaching intelligence
- Contextual resource linking
- Journey map overlays

Assign owners and schedule follow-up planning once Day 1 core ships.

---

## 10. Approvals

- **Product**: ✅ Damian Seguin (pending confirmation)
- **Implementation**: Cursor to acknowledge receipt and readiness
- **Troubleshooting**: Scout on standby for integration/debug support

Once approved, `MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md` should be archived in favor of this document.

