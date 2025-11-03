# Mosaic PS101 UI Implementation Specification v1.0
**For Cursor Implementation - Vanilla JavaScript Single-File Architecture**

**Created:** 2025-10-30
**Author:** Claude (Scout) - Senior Systems Engineer
**Purpose:** Complete specification for implementing PS101 7-step coaching interface in vanilla JavaScript

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [PS101 Framework Definition](#ps101-framework-definition)
3. [Interface Structure Specification](#interface-structure-specification)
4. [Component Specifications](#component-specifications)
5. [Technical Integration](#technical-integration)
6. [Implementation Phases](#implementation-phases)
7. [Accessibility Requirements](#accessibility-requirements)
8. [Visual Design Patterns](#visual-design-patterns)
9. [Testing & Validation](#testing--validation)
10. [Implementation Checklist](#implementation-checklist)

---

## Executive Summary

### What This Spec Delivers

A complete, implementable specification for the PS101 7-step guided coaching interface that:
- ✅ Works in vanilla JavaScript ES6+ (no frameworks, no build tools)
- ✅ Preserves Peripheral Calm aesthetic (Scandi × Japanese × Islamic)
- ✅ Integrates with existing backend (`POST /wimd/ask`)
- ✅ Maintains all existing features (auth, chat, upload, trial timer)
- ✅ Achieves WCAG 2.2 AA accessibility
- ✅ Supports mobile/responsive design

### Success Criteria

**User Experience:**
- Users complete PS101 flow intuitively (no confusion)
- Progress feels encouraging, not pressuring
- Users can review/edit previous answers easily
- Interface guides without controlling
- Calm, supportive, non-bureaucratic feel

**Technical:**
- Zero framework dependencies
- Single HTML file (`frontend/index.html`)
- Works with existing API contracts
- No breaking changes to current features
- Implementable by Cursor in 1-2 weeks

### Core Design Decisions

Based on comprehensive documentation review, these decisions optimize for:
- Self-efficacy building (not dependency creation)
- Simplicity over complexity (solo developer maintenance)
- Calm, focused user experience (Peripheral Calm aesthetic)
- Incremental enhancement (preserve what works)

**Key Decisions:**
1. **Flow Structure:** Single-screen step progression (not wizard, not accordion)
2. **Progress Indication:** Minimal step counter + subtle visual timeline
3. **Navigation:** Forward/back buttons with smart validation
4. **Chat Integration:** Keep existing bottom drawer, add contextual prompts per step
5. **Answer Display:** Expandable summary cards below current step
6. **Mobile Behavior:** Responsive grid → stack, maintain all functionality

---

## PS101 Framework Definition

### The 7 Canonical Steps

**Source:** `work_playbooks.md` lines 140-232, `mosaic_brief.md`, `CHATGPT_UI_DESIGN_BRIEF_PS101.md`

#### Step 1: WIMD - What Is My Delta?
**Question:** "Describe your current situation in 2-3 sentences. What's the gap between where you are and where you want to be?"

**Coaching Stance:** Reflective listening, non-judgmental
**Input Type:** Textarea (min 50 chars, max 500 chars)
**Validation:** At least 2 complete sentences
**Output:** Clear delta statement (problem/gap/challenge)

#### Step 2: What Matters Most?
**Question:** "Of all the aspects of this situation, what matters MOST to you? What's at the core of this?"

**Coaching Stance:** Prioritization, focus
**Input Type:** Textarea (min 30 chars, max 300 chars)
**Validation:** Single clear priority statement
**Output:** Prioritized focus (avoid solving everything at once)

#### Step 3: What Do I Know?
**Question:** "What facts do you already have? What's definitely true about this situation?"

**Coaching Stance:** Evidence-based, separating facts from assumptions
**Input Type:** Textarea or bullet list (min 50 chars)
**Validation:** At least 2 factual statements
**Output:** Evidence base (what's known/verified)

#### Step 4: What Do I Need to Know?
**Question:** "What information are you missing? What would you need to know to move forward?"

**Coaching Stance:** Identifying gaps, research questions
**Input Type:** Textarea or bullet list (min 30 chars)
**Validation:** At least 1 information gap
**Output:** Research questions, data needs

#### Step 5: What Are My Options?
**Question:** "Given what you know, what are at least 3 different ways you could approach this?"

**Coaching Stance:** Divergent thinking, avoiding binary choices
**Input Type:** Textarea or numbered list (min 100 chars)
**Validation:** At least 3 distinct options mentioned
**Output:** Multiple pathways (not just A or B)

#### Step 6: What's the Experiment?
**Question:** "Which option can you test first, in the smallest/safest way, to gather real data?"

**Coaching Stance:** Low-stakes action, learning orientation
**Input Type:** Textarea (min 50 chars, max 400 chars)
**Validation:** Specific experiment described
**Output:** Testable hypothesis (not full commitment)

#### Step 7: What's the Next Commitment?
**Question:** "What specific action will you take, by when, to run this experiment?"

**Coaching Stance:** Action-oriented, time-bound accountability
**Input Type:** Textarea with optional date picker (min 30 chars)
**Validation:** Action + deadline mentioned
**Output:** Time-bound commitment

### Quality Checks (Post-Completion)

After Step 7, system confirms:
- ✅ User can articulate problem clearly (Step 1)
- ✅ User has specific next action (Step 7)
- ✅ User has timeline for follow-up
- ✅ User feels increased clarity (self-report)

---

## Interface Structure Specification

### Flow Structure: Single-Screen Step Progression

**Rationale:**
- Maintains focus on one question at a time
- Reduces cognitive load (Peripheral Calm principle)
- Easy to implement in vanilla JS
- Clear progress indication
- Supports back/forward navigation

**Layout Pattern:**
```
┌─────────────────────────────────────────────────────────────┐
│  Header: "What Is My Delta — Career Coaching"              │
│  Progress: ● ● ○ ○ ○ ○ ○  (Step 2 of 7)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Previous Answers - Expandable Summary]                    │
│  (Collapsed by default, shows completed steps)             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Current Question (Large, Calm Typography)                  │
│  ─────────────────────────────────────────                  │
│  "What matters MOST to you about this situation?"           │
│                                                             │
│  [Coaching Hint - Optional, Expandable]                     │
│  (Contextual help per step)                                │
│                                                             │
│  ┌─────────────────────────────────────────────────┐       │
│  │                                                 │       │
│  │  [User Input - Textarea]                        │       │
│  │  Generous padding, clear focus state            │       │
│  │  Character count: 0 / 300                       │       │
│  │                                                 │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
│  [< Back]                            [Next >]              │
│  (Secondary)                         (Primary)             │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Chat Coach (Collapsed)  —  [Need Help? Ask Coach ↑]       │
└─────────────────────────────────────────────────────────────┘
```

### ASCII Diagrams - Key States

#### State 1: Welcome / Entry to PS101
```
┌──────────────────────────────────────────────────────────────┐
│  What Is My Delta                                            │
│  Career Coaching Platform                                    │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Welcome to PS101 — Problem Solving 101                      │
│  ─────────────────────────────────────────────               │
│                                                              │
│  A 7-step framework to get clarity on your career            │
│  challenge and create an action plan.                        │
│                                                              │
│  ⏱ Takes 15-30 minutes                                       │
│  💾 Progress auto-saves                                      │
│  ✏️ You can edit previous answers anytime                    │
│                                                              │
│  [Start PS101 Flow]  [Learn More]                            │
│                                                              │
│  Already started? Your progress is saved.                    │
│  [Continue Where I Left Off]                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

#### State 2: Active Step (Step 3 Example)
```
┌──────────────────────────────────────────────────────────────┐
│  Step 3 of 7: What Do I Know?                                │
│  ● ● ● ○ ○ ○ ○                                              │
├──────────────────────────────────────────────────────────────┤
│  ▼ Previous Answers (2 steps completed)  [Expand/Collapse]   │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  What facts do you already have?                             │
│  What's definitely true about this situation?                │
│  ───────────────────────────────────────                     │
│                                                              │
│  ⓘ Separate facts from assumptions. What can you prove?     │
│     [Show Example]                                           │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │ I've been in my current role for 3 years...       │     │
│  │ My manager told me there's no promotion path...   │     │
│  │                                                    │     │
│  │                                                    │     │
│  │                                                    │     │
│  │                                                    │     │
│  └────────────────────────────────────────────────────┘     │
│  Characters: 87 / 500                                        │
│                                                              │
│  [< Back to Step 2]              [Continue to Step 4 >]      │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│  💬 Need help? [Ask Coach]                                   │
└──────────────────────────────────────────────────────────────┘
```

#### State 3: Completion Summary
```
┌──────────────────────────────────────────────────────────────┐
│  PS101 Complete — Your Action Plan                           │
│  ● ● ● ● ● ● ●  (All 7 steps completed)                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Well done! You've created a clear action plan.              │
│                                                              │
│  Your Next Commitment (Step 7):                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │ "Contact 3 people in my target field by Friday    │     │
│  │  to learn about their career paths"                │     │
│  │                                                    │     │
│  │  Deadline: November 3, 2025                        │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ▼ View All Answers  [Expand]                                │
│                                                              │
│  Self-Assessment:                                            │
│  How clear are you on your next steps? ●●●●○○○ (4/7)        │
│  How likely are you to follow through? ●●●●●○○ (5/7)        │
│                                                              │
│  [Download Summary]  [Email to Myself]  [Start Over]         │
│                                                              │
│  Next Steps:                                                 │
│  - Set a reminder for your commitment deadline               │
│  - Explore job opportunities that match your delta           │
│  - Work with coach to refine your resume                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Progress Indication

**Visual Design:**
```
Step 1 of 7: What Is My Delta?

● ● ○ ○ ○ ○ ○
^-- Current

[Completed]  [Current]  [Upcoming]
   Solid       Ring        Outline
```

**HTML Structure:**
```html
<div class="ps101-progress" role="navigation" aria-label="PS101 Progress">
  <div class="progress-header">
    <span class="step-label">Step 2 of 7: What Matters Most?</span>
  </div>
  <div class="progress-dots">
    <button class="dot completed" aria-label="Step 1: WIMD (completed)" data-step="1">1</button>
    <button class="dot active" aria-label="Step 2: What Matters Most (current)" aria-current="step" data-step="2">2</button>
    <button class="dot" aria-label="Step 3: What I Know" data-step="3">3</button>
    <button class="dot" aria-label="Step 4: What I Need to Know" data-step="4">4</button>
    <button class="dot" aria-label="Step 5: Options" data-step="5">5</button>
    <button class="dot" aria-label="Step 6: Experiment" data-step="6">6</button>
    <button class="dot" aria-label="Step 7: Commitment" data-step="7">7</button>
  </div>
</div>
```

**CSS (Using Peripheral Calm Tokens):**
```css
.ps101-progress {
  max-width: var(--max);
  margin: 0 auto 40px;
  padding: 20px;
}

.progress-header {
  text-align: center;
  margin-bottom: 16px;
}

.step-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--fg);
  letter-spacing: 0.02em;
}

.progress-dots {
  display: flex;
  justify-content: center;
  gap: 12px;
  align-items: center;
}

.progress-dots .dot {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid var(--line);
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  color: var(--muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.progress-dots .dot:hover {
  border-color: var(--hair);
  transform: translateY(-1px);
}

.progress-dots .dot.completed {
  background: linear-gradient(145deg, #f5f5f5 0%, #eeeeee 100%);
  color: var(--fg);
  border-color: var(--hair);
}

.progress-dots .dot.active {
  background: linear-gradient(145deg, #ffffff 0%, #f8f8f8 100%);
  box-shadow: 0 3px 8px rgba(0,0,0,0.12);
  color: var(--fg);
  font-weight: 600;
  border-color: var(--hair);
}

.progress-dots .dot:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* Mobile */
@media (max-width: 768px) {
  .progress-dots {
    gap: 8px;
  }

  .progress-dots .dot {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }
}
```

### Navigation Controls

**HTML:**
```html
<div class="ps101-nav">
  <button class="nav-btn nav-back quiet" id="ps101-back" aria-label="Go back to previous step">
    ← Back
  </button>

  <button class="nav-btn nav-next quiet" id="ps101-next" aria-label="Continue to next step">
    Next →
  </button>
</div>
```

**CSS:**
```css
.ps101-nav {
  display: flex;
  justify-content: space-between;
  margin-top: 32px;
  gap: 16px;
}

.nav-btn {
  /* Inherits from .quiet (existing button style) */
  min-width: 120px;
  padding: 10px 20px;
  font-size: 13px;
}

.nav-back {
  /* Secondary style - more subtle */
  background: transparent;
  border-color: var(--line);
}

.nav-next {
  /* Primary style - more prominent */
  background: linear-gradient(145deg, #ffffff 0%, #f8f8f8 100%);
  border-color: var(--hair);
  font-weight: 500;
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Mobile */
@media (max-width: 768px) {
  .ps101-nav {
    flex-direction: column-reverse;
  }

  .nav-btn {
    width: 100%;
  }
}
```

### Previous Answers Display

**Expandable Summary Cards:**

```html
<details class="previous-answers" id="previous-answers">
  <summary>
    <span class="summary-text">▼ Previous Answers (2 steps completed)</span>
    <span class="summary-hint">Click to review or edit</span>
  </summary>

  <div class="answer-list">
    <div class="answer-card" data-step="1">
      <div class="answer-header">
        <span class="answer-step">Step 1: What Is My Delta?</span>
        <button class="answer-edit" aria-label="Edit Step 1">Edit</button>
      </div>
      <div class="answer-content">
        I've been a marketing coordinator for 3 years but feel stuck.
        I want to move into a strategic role with more autonomy and impact...
      </div>
    </div>

    <div class="answer-card" data-step="2">
      <div class="answer-header">
        <span class="answer-step">Step 2: What Matters Most?</span>
        <button class="answer-edit" aria-label="Edit Step 2">Edit</button>
      </div>
      <div class="answer-content">
        Having more autonomy and being able to shape strategy, not just execute it.
      </div>
    </div>
  </div>
</details>
```

**CSS:**
```css
.previous-answers {
  margin-bottom: 32px;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
  padding: 16px;
}

.previous-answers summary {
  cursor: pointer;
  user-select: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}

.previous-answers summary:hover .summary-text {
  color: var(--fg);
}

.summary-text {
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  transition: color 0.2s ease;
}

.summary-hint {
  font-size: 11px;
  color: var(--muted);
}

.answer-list {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.answer-card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 12px;
  transition: box-shadow 0.2s ease;
}

.answer-card:hover {
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.answer-step {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--fg);
}

.answer-edit {
  font-size: 11px;
  padding: 4px 8px;
  border: 1px solid var(--line);
  background: transparent;
  cursor: pointer;
  border-radius: 2px;
  transition: all 0.2s ease;
}

.answer-edit:hover {
  background: var(--line);
}

.answer-content {
  font-size: 12px;
  line-height: 1.5;
  color: var(--muted);
  white-space: pre-wrap;
}
```

### Chat Integration

**Bottom Drawer (Keep Existing, Enhance Context):**

Current implementation: Bottom-right chat drawer (320px wide)

**Enhancement: Contextual Prompts Per Step**

```javascript
// In PS101 state management
const CONTEXTUAL_PROMPTS = {
  1: [
    "Help me articulate my delta more clearly",
    "I'm not sure how to describe my situation",
    "Give me an example of a good delta statement"
  ],
  2: [
    "How do I prioritize when everything feels important?",
    "I have multiple things that matter - which to focus on?",
    "Help me identify what's at the core"
  ],
  3: [
    "How do I separate facts from assumptions?",
    "What counts as evidence vs. opinion?",
    "Give me examples of factual statements"
  ],
  // ... prompts for steps 4-7
};

function updateChatContextualPrompts(currentStep) {
  const prompts = CONTEXTUAL_PROMPTS[currentStep] || [];
  const chatSuggestions = document.getElementById('chat-suggestions');

  chatSuggestions.innerHTML = prompts.map(prompt =>
    `<button class="chat-suggestion" data-prompt="${prompt}">${prompt}</button>`
  ).join('');
}
```

**Add Suggestions to Chat Drawer:**
```html
<aside class="chat" id="chat" role="dialog" aria-labelledby="chatTitle">
  <header>
    <div id="chatTitle">Coach</div>
    <button class="x" id="closeChat" title="Close" aria-label="Close chat">×</button>
  </header>

  <!-- NEW: Contextual suggestions -->
  <div class="chat-suggestions" id="chat-suggestions">
    <button class="chat-suggestion" data-prompt="Help me with this step">Help me with this step</button>
    <button class="chat-suggestion" data-prompt="Give me an example">Give me an example</button>
  </div>

  <main id="chatLog" aria-live="polite"></main>
  <footer>
    <input id="chatInput" placeholder="Ask coach..." aria-label="Chat input" autocomplete="off">
    <button class="btn" id="sendMsg">Send</button>
  </footer>
</aside>
```

**CSS for Suggestions:**
```css
.chat-suggestions {
  padding: 8px 12px;
  border-bottom: 1px solid var(--line);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chat-suggestion {
  font-size: 11px;
  padding: 6px 10px;
  background: #f8f8f8;
  border: 1px solid var(--line);
  border-radius: 12px;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
}

.chat-suggestion:hover {
  background: #fff;
  border-color: var(--hair);
  transform: translateX(2px);
}
```

---

## Component Specifications

### 1. PS101 Container Component

**Purpose:** Main wrapper for PS101 flow, replaces or enhances existing module

**HTML Structure:**
```html
<section id="ps101-flow" class="ps101-container" aria-label="PS101 Coaching Flow">
  <!-- Progress indicator -->
  <div class="ps101-progress" role="navigation" aria-label="Progress">
    <!-- See progress section above -->
  </div>

  <!-- Previous answers (expandable) -->
  <details class="previous-answers" id="previous-answers">
    <!-- See previous answers section above -->
  </details>

  <!-- Current step question -->
  <div class="ps101-question" id="ps101-question">
    <h2 class="question-text" id="question-text">
      <!-- Dynamic: Current step question -->
    </h2>

    <!-- Optional coaching hint -->
    <details class="coaching-hint" id="coaching-hint">
      <summary>💡 Coaching Hint</summary>
      <p id="hint-text">
        <!-- Dynamic: Step-specific guidance -->
      </p>
    </details>
  </div>

  <!-- User input area -->
  <div class="ps101-input" id="ps101-input">
    <textarea
      id="step-answer"
      class="step-textarea"
      placeholder="Type your answer here..."
      aria-label="Your answer"
      rows="6"
    ></textarea>
    <div class="char-count" id="char-count" aria-live="polite">
      <span id="char-current">0</span> / <span id="char-max">500</span>
    </div>
  </div>

  <!-- Navigation -->
  <div class="ps101-nav">
    <!-- See navigation section above -->
  </div>

  <!-- Auto-save indicator -->
  <div class="autosave-indicator" id="autosave-indicator" aria-live="polite">
    <span class="autosave-text">Saved</span>
  </div>
</section>
```

**CSS:**
```css
.ps101-container {
  max-width: var(--max);
  margin: 0 auto;
  padding: 40px 20px;
}

.ps101-question {
  margin-bottom: 32px;
}

.question-text {
  font-size: 18px;
  font-weight: 400;
  line-height: 1.5;
  color: var(--fg);
  margin: 0 0 16px;
}

.coaching-hint {
  margin-top: 12px;
  padding: 12px;
  background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
  border: 1px solid var(--line);
  border-radius: 4px;
}

.coaching-hint summary {
  font-size: 12px;
  cursor: pointer;
  user-select: none;
  color: var(--muted);
}

.coaching-hint summary:hover {
  color: var(--fg);
}

.coaching-hint p {
  margin: 8px 0 0;
  font-size: 12px;
  line-height: 1.5;
  color: var(--muted);
}

.ps101-input {
  margin-bottom: 24px;
}

.step-textarea {
  width: 100%;
  min-height: 120px;
  padding: 12px;
  border: 1px solid var(--line);
  border-radius: 4px;
  font: inherit;
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
  transition: all 0.2s ease;
}

.step-textarea:focus {
  outline: none;
  border-color: var(--hair);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.char-count {
  margin-top: 8px;
  font-size: 11px;
  color: var(--muted);
  text-align: right;
}

.autosave-indicator {
  margin-top: 16px;
  text-align: center;
  font-size: 11px;
  color: var(--muted);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.autosave-indicator.visible {
  opacity: 1;
}

/* Mobile */
@media (max-width: 768px) {
  .ps101-container {
    padding: 24px 16px;
  }

  .question-text {
    font-size: 16px;
  }

  .step-textarea {
    min-height: 100px;
  }
}
```

### 2. Welcome / Entry Screen Component

**Purpose:** First screen users see when starting PS101

**HTML:**
```html
<div class="ps101-welcome" id="ps101-welcome">
  <div class="welcome-content">
    <h1 class="welcome-title">Welcome to PS101</h1>
    <p class="welcome-subtitle">Problem Solving 101</p>

    <div class="welcome-description">
      <p>A 7-step framework to get clarity on your career challenge and create an action plan.</p>

      <ul class="welcome-features">
        <li>⏱ Takes 15-30 minutes</li>
        <li>💾 Progress auto-saves</li>
        <li>✏️ Edit previous answers anytime</li>
      </ul>
    </div>

    <div class="welcome-actions">
      <button class="quiet welcome-btn-primary" id="start-ps101">
        Start PS101 Flow
      </button>

      <button class="quiet welcome-btn-secondary" id="learn-more-ps101">
        Learn More
      </button>
    </div>

    <div class="welcome-resume" id="welcome-resume" style="display: none;">
      <p class="resume-text">Already started? Your progress is saved.</p>
      <button class="quiet" id="continue-ps101">
        Continue Where I Left Off
      </button>
    </div>
  </div>
</div>
```

**CSS:**
```css
.ps101-welcome {
  max-width: 640px;
  margin: 80px auto;
  padding: 40px 20px;
  text-align: center;
}

.welcome-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px;
  color: var(--fg);
}

.welcome-subtitle {
  font-size: 14px;
  font-weight: 400;
  color: var(--muted);
  margin: 0 0 32px;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.welcome-description {
  margin-bottom: 32px;
  text-align: left;
}

.welcome-description p {
  font-size: 14px;
  line-height: 1.6;
  color: var(--fg);
  margin-bottom: 16px;
}

.welcome-features {
  list-style: none;
  padding: 0;
  margin: 0;
}

.welcome-features li {
  font-size: 13px;
  line-height: 2;
  color: var(--muted);
}

.welcome-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.welcome-btn-primary {
  /* Inherits from .quiet, make more prominent */
  font-weight: 500;
  background: linear-gradient(145deg, #ffffff 0%, #f8f8f8 100%);
  border-color: var(--hair);
}

.welcome-btn-secondary {
  /* Inherits from .quiet, more subtle */
  background: transparent;
  border-color: var(--line);
}

.welcome-resume {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
}

.resume-text {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 12px;
}

/* Mobile */
@media (max-width: 768px) {
  .ps101-welcome {
    margin: 40px auto;
    padding: 24px 16px;
  }

  .welcome-title {
    font-size: 24px;
  }
}
```

### 3. Completion Summary Component

**Purpose:** Final screen after completing all 7 steps

**HTML:**
```html
<div class="ps101-completion" id="ps101-completion">
  <div class="completion-header">
    <h2 class="completion-title">PS101 Complete — Your Action Plan</h2>
    <div class="completion-progress">
      ● ● ● ● ● ● ●
      <span class="completion-label">All 7 steps completed</span>
    </div>
  </div>

  <div class="completion-message">
    <p>Well done! You've created a clear action plan.</p>
  </div>

  <!-- Highlighted commitment -->
  <div class="commitment-highlight">
    <h3 class="commitment-label">Your Next Commitment (Step 7):</h3>
    <div class="commitment-text" id="commitment-text">
      <!-- Dynamic: User's Step 7 answer -->
    </div>
    <div class="commitment-deadline" id="commitment-deadline">
      <!-- Dynamic: Deadline if provided -->
    </div>
  </div>

  <!-- Expandable full summary -->
  <details class="completion-summary" open>
    <summary>▼ View All Answers</summary>
    <div class="answer-list" id="completion-answers">
      <!-- Dynamic: All 7 steps with answers -->
    </div>
  </details>

  <!-- Self-assessment (optional) -->
  <div class="completion-assessment">
    <h3>Self-Assessment</h3>

    <div class="assessment-item">
      <label for="clarity-rating">How clear are you on your next steps?</label>
      <input
        type="range"
        id="clarity-rating"
        min="1"
        max="7"
        value="4"
        aria-label="Clarity rating from 1 to 7"
      >
      <span class="rating-value" id="clarity-value">4/7</span>
    </div>

    <div class="assessment-item">
      <label for="action-rating">How likely are you to follow through?</label>
      <input
        type="range"
        id="action-rating"
        min="1"
        max="7"
        value="5"
        aria-label="Action rating from 1 to 7"
      >
      <span class="rating-value" id="action-value">5/7</span>
    </div>
  </div>

  <!-- Actions -->
  <div class="completion-actions">
    <button class="quiet" id="download-summary">Download Summary</button>
    <button class="quiet" id="email-summary">Email to Myself</button>
    <button class="quiet" id="start-over">Start Over</button>
  </div>

  <!-- Next steps suggestions -->
  <div class="next-steps">
    <h3>Next Steps</h3>
    <ul>
      <li>Set a reminder for your commitment deadline</li>
      <li><a href="#jobs">Explore job opportunities</a> that match your delta</li>
      <li><a href="#resume">Work with coach</a> to refine your resume</li>
    </ul>
  </div>
</div>
```

**CSS:**
```css
.ps101-completion {
  max-width: var(--max);
  margin: 40px auto;
  padding: 40px 20px;
}

.completion-header {
  text-align: center;
  margin-bottom: 32px;
}

.completion-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--fg);
  margin: 0 0 16px;
}

.completion-progress {
  font-size: 16px;
  color: var(--fg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.completion-label {
  font-size: 12px;
  color: var(--muted);
}

.completion-message {
  text-align: center;
  margin-bottom: 32px;
}

.completion-message p {
  font-size: 14px;
  color: var(--muted);
}

.commitment-highlight {
  background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 20px;
  margin-bottom: 32px;
}

.commitment-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--fg);
  margin: 0 0 12px;
}

.commitment-text {
  font-size: 14px;
  line-height: 1.6;
  color: var(--fg);
  margin-bottom: 8px;
  white-space: pre-wrap;
}

.commitment-deadline {
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
}

.completion-summary {
  margin-bottom: 32px;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 16px;
}

.completion-summary summary {
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  user-select: none;
}

.completion-assessment {
  margin-bottom: 32px;
  padding: 20px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 4px;
}

.completion-assessment h3 {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 16px;
  color: var(--fg);
}

.assessment-item {
  margin-bottom: 16px;
}

.assessment-item label {
  display: block;
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 8px;
}

.assessment-item input[type="range"] {
  width: 100%;
  margin-bottom: 4px;
}

.rating-value {
  font-size: 12px;
  color: var(--fg);
  font-weight: 500;
}

.completion-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.next-steps {
  padding: 20px;
  background: linear-gradient(145deg, #fafafa 0%, #f5f5f5 100%);
  border-radius: 4px;
}

.next-steps h3 {
  font-size: 14px;
  font-weight: 600;
  margin: 0 0 12px;
  color: var(--fg);
}

.next-steps ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.next-steps li {
  font-size: 12px;
  line-height: 2;
  color: var(--muted);
}

.next-steps a {
  color: var(--fg);
  text-decoration: underline;
}

/* Mobile */
@media (max-width: 768px) {
  .completion-actions {
    flex-direction: column;
  }

  .completion-actions button {
    width: 100%;
  }
}
```

---

## Technical Integration

### Backend Integration

**Existing Endpoint: `POST /wimd/ask`**

**Request Format:**
```json
{
  "prompt": "User's answer to current step question",
  "step": 3,
  "session_id": "uuid-session-id"
}
```

**Response Format:**
```json
{
  "result": {
    "message": "Coach's reflective response or next question",
    "step_saved": true
  }
}
```

**Session State Storage:**

Backend already supports `session.user_data` JSONB field:
```json
{
  "ps101": {
    "current_step": 3,
    "started_at": "2025-10-30T10:00:00Z",
    "last_updated": "2025-10-30T10:15:00Z",
    "answers": {
      "1": "I've been a marketing coordinator for 3 years...",
      "2": "Having more autonomy and being able to shape strategy...",
      "3": "I know I have strong analytical skills..."
    },
    "completion": {
      "clarity_score": 4,
      "action_score": 5,
      "completed_at": null
    }
  }
}
```

**Progress Persistence:**

Table: `wimd_outputs`
```sql
INSERT INTO wimd_outputs (user_id, step_number, response_text, clarity_score, created_at)
VALUES ($1, $2, $3, $4, NOW())
ON CONFLICT (user_id, step_number)
DO UPDATE SET response_text = $3, clarity_score = $4, updated_at = NOW();
```

**Auto-save Mechanism:**

```javascript
// Debounced auto-save (existing pattern in index.html)
let autosaveTimeout;

function autosaveAnswer(stepNumber, answerText) {
  clearTimeout(autosaveTimeout);

  autosaveTimeout = setTimeout(async () => {
    // Save to localStorage (immediate)
    const ps101State = JSON.parse(localStorage.getItem('ps101_state') || '{}');
    ps101State.answers = ps101State.answers || {};
    ps101State.answers[stepNumber] = answerText;
    ps101State.last_updated = new Date().toISOString();
    localStorage.setItem('ps101_state', JSON.stringify(ps101State));

    // Save to backend (if authenticated)
    if (isAuthenticated()) {
      try {
        await fetch(`${API_BASE}/wimd/ask`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getSessionToken()}`
          },
          body: JSON.stringify({
            prompt: answerText,
            step: stepNumber,
            session_id: getSessionId()
          })
        });

        showAutosaveIndicator('Saved');
      } catch (error) {
        console.error('Autosave failed:', error);
        showAutosaveIndicator('Save failed - will retry');
      }
    }
  }, 1000); // 1 second debounce
}

function showAutosaveIndicator(message) {
  const indicator = document.getElementById('autosave-indicator');
  const text = indicator.querySelector('.autosave-text');

  text.textContent = message;
  indicator.classList.add('visible');

  setTimeout(() => {
    indicator.classList.remove('visible');
  }, 2000);
}
```

### Frontend State Management

**PS101 State Object (Vanilla JS):**

```javascript
// IIFE Pattern (existing pattern in index.html)
(function() {
  'use strict';

  // PS101 Framework Definition
  const PS101_STEPS = [
    {
      number: 1,
      title: 'What Is My Delta?',
      question: 'Describe your current situation in 2-3 sentences. What\'s the gap between where you are and where you want to be?',
      hint: 'Focus on the difference between your current reality and your desired future. What needs to change?',
      minChars: 50,
      maxChars: 500,
      placeholder: 'Example: I\'ve been a marketing coordinator for 3 years but feel stuck. I want to move into a strategic role with more autonomy and impact...'
    },
    {
      number: 2,
      title: 'What Matters Most?',
      question: 'Of all the aspects of this situation, what matters MOST to you? What\'s at the core of this?',
      hint: 'Prioritize. If you could only focus on one thing, what would it be?',
      minChars: 30,
      maxChars: 300,
      placeholder: 'Example: Having more autonomy and being able to shape strategy, not just execute it.'
    },
    {
      number: 3,
      title: 'What Do I Know?',
      question: 'What facts do you already have? What\'s definitely true about this situation?',
      hint: 'Separate facts from assumptions. What can you prove or verify?',
      minChars: 50,
      maxChars: 500,
      placeholder: 'Example: I know I have strong analytical skills from my work on the Q3 campaign...'
    },
    {
      number: 4,
      title: 'What Do I Need to Know?',
      question: 'What information are you missing? What would you need to know to move forward?',
      hint: 'Identify gaps in your knowledge. What questions need answers?',
      minChars: 30,
      maxChars: 500,
      placeholder: 'Example: I need to know what skills strategic roles actually require...'
    },
    {
      number: 5,
      title: 'What Are My Options?',
      question: 'Given what you know, what are at least 3 different ways you could approach this?',
      hint: 'Brainstorm multiple paths. Avoid binary thinking (this OR that).',
      minChars: 100,
      maxChars: 500,
      placeholder: 'Example: 1) Ask for more strategic projects in current role, 2) Look for strategy roles at other companies, 3) Get training/certification in strategic planning...'
    },
    {
      number: 6,
      title: 'What\'s the Experiment?',
      question: 'Which option can you test first, in the smallest/safest way, to gather real data?',
      hint: 'Small experiment = low stakes, quick learning. What can you test this week?',
      minChars: 50,
      maxChars: 400,
      placeholder: 'Example: Ask my manager if I can lead the strategy portion of next quarter\'s planning meeting...'
    },
    {
      number: 7,
      title: 'What\'s the Next Commitment?',
      question: 'What specific action will you take, by when, to run this experiment?',
      hint: 'Be specific: What action? By when? Make it time-bound and measurable.',
      minChars: 30,
      maxChars: 300,
      placeholder: 'Example: Schedule a 1:1 with my manager by Friday to discuss taking on strategic planning work...'
    }
  ];

  // State Object
  const PS101State = {
    currentStep: 1,
    answers: {},
    startedAt: null,
    lastUpdated: null,
    completed: false,
    completionScores: {
      clarity: null,
      action: null
    },

    // Initialize state
    init() {
      // Try to load from localStorage first
      const savedState = localStorage.getItem('ps101_state');
      if (savedState) {
        try {
          const parsed = JSON.parse(savedState);
          Object.assign(this, parsed);
        } catch (e) {
          console.error('Failed to parse saved PS101 state:', e);
        }
      }

      // Try to load from backend (if authenticated)
      if (isAuthenticated()) {
        this.loadFromBackend();
      }

      // If never started, initialize
      if (!this.startedAt) {
        this.startedAt = new Date().toISOString();
      }
    },

    // Load state from backend
    async loadFromBackend() {
      try {
        const response = await fetch(`${API_BASE}/auth/me`, {
          headers: {
            'Authorization': `Bearer ${getSessionToken()}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          const ps101Data = data.session?.user_data?.ps101;

          if (ps101Data) {
            this.currentStep = ps101Data.current_step || 1;
            this.answers = ps101Data.answers || {};
            this.startedAt = ps101Data.started_at;
            this.lastUpdated = ps101Data.last_updated;
            this.completed = ps101Data.completion?.completed_at != null;
            this.completionScores = ps101Data.completion || {};
          }
        }
      } catch (error) {
        console.error('Failed to load PS101 state from backend:', error);
      }
    },

    // Save state
    save() {
      this.lastUpdated = new Date().toISOString();

      // Save to localStorage
      localStorage.setItem('ps101_state', JSON.stringify(this));

      // Save to backend (if authenticated)
      if (isAuthenticated()) {
        this.saveToBackend();
      }
    },

    // Save to backend
    async saveToBackend() {
      // Backend save happens via autosaveAnswer() on each step
      // This method is for full state sync if needed
    },

    // Get current step data
    getCurrentStep() {
      return PS101_STEPS.find(s => s.number === this.currentStep);
    },

    // Get answer for step
    getAnswer(stepNumber) {
      return this.answers[stepNumber] || '';
    },

    // Set answer for step
    setAnswer(stepNumber, answer) {
      this.answers[stepNumber] = answer;
      this.save();
    },

    // Navigate to step
    goToStep(stepNumber) {
      if (stepNumber >= 1 && stepNumber <= PS101_STEPS.length) {
        this.currentStep = stepNumber;
        this.save();
        renderCurrentStep();
      }
    },

    // Next step
    nextStep() {
      if (this.currentStep < PS101_STEPS.length) {
        this.currentStep++;
        this.save();
        renderCurrentStep();
      } else {
        // All steps complete
        this.completed = true;
        this.save();
        renderCompletionScreen();
      }
    },

    // Previous step
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--;
        this.save();
        renderCurrentStep();
      }
    },

    // Reset
    reset() {
      this.currentStep = 1;
      this.answers = {};
      this.startedAt = new Date().toISOString();
      this.lastUpdated = null;
      this.completed = false;
      this.completionScores = {};
      this.save();
      renderWelcomeScreen();
    }
  };

  // Initialize on page load
  PS101State.init();

  // Expose to global scope (for event handlers)
  window.PS101State = PS101State;
  window.PS101_STEPS = PS101_STEPS;

})();
```

### Rendering Functions

**Render Current Step:**

```javascript
function renderCurrentStep() {
  const state = window.PS101State;
  const currentStep = state.getCurrentStep();

  if (!currentStep) {
    console.error('Invalid step number:', state.currentStep);
    return;
  }

  // Hide welcome/completion, show main flow
  document.getElementById('ps101-welcome')?.classList.add('hidden');
  document.getElementById('ps101-completion')?.classList.add('hidden');
  document.getElementById('ps101-flow')?.classList.remove('hidden');

  // Update progress indicator
  updateProgressIndicator(state.currentStep);

  // Update question text
  document.getElementById('question-text').textContent = currentStep.question;

  // Update hint
  const hintText = document.getElementById('hint-text');
  if (hintText) {
    hintText.textContent = currentStep.hint;
  }

  // Update textarea
  const textarea = document.getElementById('step-answer');
  textarea.value = state.getAnswer(currentStep.number);
  textarea.placeholder = currentStep.placeholder;
  textarea.setAttribute('maxlength', currentStep.maxChars);

  // Update character count
  updateCharCount(textarea.value.length, currentStep.maxChars);

  // Update navigation buttons
  updateNavButtons(state.currentStep);

  // Update previous answers
  renderPreviousAnswers(state.currentStep);

  // Update chat contextual prompts
  updateChatContextualPrompts(state.currentStep);

  // Focus textarea
  textarea.focus();
}

function updateProgressIndicator(currentStep) {
  const dots = document.querySelectorAll('.progress-dots .dot');

  dots.forEach((dot, index) => {
    const stepNumber = index + 1;

    // Remove all state classes
    dot.classList.remove('completed', 'active');

    // Add appropriate class
    if (stepNumber < currentStep) {
      dot.classList.add('completed');
      dot.disabled = false;
    } else if (stepNumber === currentStep) {
      dot.classList.add('active');
      dot.setAttribute('aria-current', 'step');
      dot.disabled = false;
    } else {
      // Future step
      dot.disabled = true;
    }
  });

  // Update step label
  const stepLabel = document.querySelector('.step-label');
  const step = window.PS101_STEPS[currentStep - 1];
  stepLabel.textContent = `Step ${currentStep} of 7: ${step.title}`;
}

function updateCharCount(current, max) {
  document.getElementById('char-current').textContent = current;
  document.getElementById('char-max').textContent = max;

  const charCount = document.querySelector('.char-count');
  if (current > max * 0.9) {
    charCount.style.color = '#d63638'; // Warning color
  } else {
    charCount.style.color = 'var(--muted)';
  }
}

function updateNavButtons(currentStep) {
  const backBtn = document.getElementById('ps101-back');
  const nextBtn = document.getElementById('ps101-next');

  // Back button
  if (currentStep === 1) {
    backBtn.disabled = true;
  } else {
    backBtn.disabled = false;
  }

  // Next button text
  if (currentStep === 7) {
    nextBtn.textContent = 'Complete PS101 →';
  } else {
    nextBtn.textContent = 'Next →';
  }
}

function renderPreviousAnswers(currentStep) {
  const state = window.PS101State;
  const previousSteps = currentStep - 1;

  if (previousSteps === 0) {
    // No previous answers yet
    document.getElementById('previous-answers').style.display = 'none';
    return;
  }

  document.getElementById('previous-answers').style.display = 'block';

  // Update summary text
  const summaryText = document.querySelector('.summary-text');
  summaryText.textContent = `▼ Previous Answers (${previousSteps} step${previousSteps > 1 ? 's' : ''} completed)`;

  // Render answer cards
  const answerList = document.querySelector('.previous-answers .answer-list');
  answerList.innerHTML = '';

  for (let i = 1; i < currentStep; i++) {
    const step = window.PS101_STEPS[i - 1];
    const answer = state.getAnswer(i);

    const card = document.createElement('div');
    card.className = 'answer-card';
    card.dataset.step = i;

    card.innerHTML = `
      <div class="answer-header">
        <span class="answer-step">Step ${i}: ${step.title}</span>
        <button class="answer-edit" data-step="${i}" aria-label="Edit Step ${i}">Edit</button>
      </div>
      <div class="answer-content">${escapeHtml(answer)}</div>
    `;

    answerList.appendChild(card);
  }

  // Add click handlers for edit buttons
  document.querySelectorAll('.answer-edit').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const stepNumber = parseInt(e.target.dataset.step);
      state.goToStep(stepNumber);
    });
  });
}

function renderWelcomeScreen() {
  const state = window.PS101State;

  // Show welcome, hide others
  document.getElementById('ps101-welcome')?.classList.remove('hidden');
  document.getElementById('ps101-flow')?.classList.add('hidden');
  document.getElementById('ps101-completion')?.classList.add('hidden');

  // Check if user has progress
  const hasProgress = Object.keys(state.answers).length > 0;
  const resumeSection = document.getElementById('welcome-resume');

  if (hasProgress && !state.completed) {
    resumeSection.style.display = 'block';
  } else {
    resumeSection.style.display = 'none';
  }
}

function renderCompletionScreen() {
  const state = window.PS101State;

  // Show completion, hide others
  document.getElementById('ps101-completion')?.classList.remove('hidden');
  document.getElementById('ps101-flow')?.classList.add('hidden');
  document.getElementById('ps101-welcome')?.classList.add('hidden');

  // Render commitment highlight
  const commitmentText = document.getElementById('commitment-text');
  commitmentText.textContent = state.getAnswer(7);

  // Render all answers
  const completionAnswers = document.getElementById('completion-answers');
  completionAnswers.innerHTML = '';

  window.PS101_STEPS.forEach(step => {
    const answer = state.getAnswer(step.number);

    const card = document.createElement('div');
    card.className = 'answer-card';
    card.innerHTML = `
      <div class="answer-header">
        <span class="answer-step">Step ${step.number}: ${step.title}</span>
      </div>
      <div class="answer-content">${escapeHtml(answer)}</div>
    `;

    completionAnswers.appendChild(card);
  });

  // Initialize rating sliders
  initializeRatings();
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
```

### Event Handlers

**Event Listener Setup:**

```javascript
// Add event listeners when DOM is ready
document.addEventListener('DOMContentLoaded', () => {

  // Welcome screen buttons
  document.getElementById('start-ps101')?.addEventListener('click', () => {
    window.PS101State.currentStep = 1;
    window.PS101State.save();
    renderCurrentStep();
  });

  document.getElementById('continue-ps101')?.addEventListener('click', () => {
    renderCurrentStep();
  });

  document.getElementById('learn-more-ps101')?.addEventListener('click', () => {
    // Show modal or scroll to about section
    scrollToSection('about');
  });

  // Navigation buttons
  document.getElementById('ps101-back')?.addEventListener('click', () => {
    window.PS101State.prevStep();
  });

  document.getElementById('ps101-next')?.addEventListener('click', () => {
    const isValid = validateCurrentStep();
    if (isValid) {
      // Save current answer
      const textarea = document.getElementById('step-answer');
      window.PS101State.setAnswer(window.PS101State.currentStep, textarea.value);

      // Auto-save to backend
      autosaveAnswer(window.PS101State.currentStep, textarea.value);

      // Move to next step
      window.PS101State.nextStep();
    }
  });

  // Progress dots (click to jump to step)
  document.querySelectorAll('.progress-dots .dot').forEach(dot => {
    dot.addEventListener('click', (e) => {
      if (!e.target.disabled) {
        const stepNumber = parseInt(e.target.dataset.step);
        window.PS101State.goToStep(stepNumber);
      }
    });
  });

  // Textarea input (auto-save + char count)
  const textarea = document.getElementById('step-answer');
  textarea?.addEventListener('input', (e) => {
    const currentStep = window.PS101State.getCurrentStep();
    updateCharCount(e.target.value.length, currentStep.maxChars);

    // Debounced auto-save
    autosaveAnswer(window.PS101State.currentStep, e.target.value);
  });

  // Completion screen buttons
  document.getElementById('download-summary')?.addEventListener('click', downloadSummary);
  document.getElementById('email-summary')?.addEventListener('click', emailSummary);
  document.getElementById('start-over')?.addEventListener('click', () => {
    if (confirm('Are you sure you want to start over? This will clear all your answers.')) {
      window.PS101State.reset();
    }
  });

  // Rating sliders
  document.getElementById('clarity-rating')?.addEventListener('input', (e) => {
    document.getElementById('clarity-value').textContent = `${e.target.value}/7`;
    window.PS101State.completionScores.clarity = parseInt(e.target.value);
    window.PS101State.save();
  });

  document.getElementById('action-rating')?.addEventListener('input', (e) => {
    document.getElementById('action-value').textContent = `${e.target.value}/7`;
    window.PS101State.completionScores.action = parseInt(e.target.value);
    window.PS101State.save();
  });

});
```

### Validation

**Step Validation:**

```javascript
function validateCurrentStep() {
  const state = window.PS101State;
  const currentStep = state.getCurrentStep();
  const textarea = document.getElementById('step-answer');
  const answer = textarea.value.trim();

  // Check minimum length
  if (answer.length < currentStep.minChars) {
    alert(`Please provide at least ${currentStep.minChars} characters for this step.`);
    textarea.focus();
    return false;
  }

  // Check maximum length
  if (answer.length > currentStep.maxChars) {
    alert(`Please keep your answer under ${currentStep.maxChars} characters.`);
    textarea.focus();
    return false;
  }

  // Step-specific validation
  switch (currentStep.number) {
    case 1: // WIMD - need at least 2 sentences
      const sentences = answer.split(/[.!?]+/).filter(s => s.trim().length > 0);
      if (sentences.length < 2) {
        alert('Please provide at least 2 sentences describing your situation.');
        return false;
      }
      break;

    case 5: // Options - need at least 3 options
      // Simple heuristic: look for numbers 1-3 or bullet points
      const hasNumbers = /[1-3]/.test(answer);
      const hasBullets = /[•\-\*]/.test(answer);
      if (!hasNumbers && !hasBullets) {
        alert('Please list at least 3 different options you could pursue.');
        return false;
      }
      break;

    case 7: // Commitment - should mention a timeframe
      const timewords = ['by', 'before', 'on', 'this week', 'next', 'friday', 'monday', 'deadline'];
      const hasTime = timewords.some(word => answer.toLowerCase().includes(word));
      if (!hasTime) {
        const confirmed = confirm('Your commitment doesn\'t seem to include a deadline. Continue anyway?');
        if (!confirmed) return false;
      }
      break;
  }

  return true;
}
```

---

## Implementation Phases

### Phase 1: Core PS101 Flow (Week 1)
**Estimated effort: 3-5 days**

**Deliverables:**
- ✅ Welcome screen with start/continue
- ✅ 7-step progression (forward/back navigation)
- ✅ Progress indicator (dots + step counter)
- ✅ Question display per step
- ✅ Textarea input with char count
- ✅ Basic validation
- ✅ Auto-save to localStorage

**Testing:**
- User can start PS101 flow
- User can navigate forward/back
- Progress saves on refresh
- All 7 steps display correctly
- Validation prevents skipping steps

### Phase 2: Backend Integration & Previous Answers (Week 2)
**Estimated effort: 3-4 days**

**Deliverables:**
- ✅ Auto-save to backend (`POST /wimd/ask`)
- ✅ Load state from backend on auth
- ✅ Previous answers display (expandable)
- ✅ Edit previous step functionality
- ✅ Completion screen
- ✅ Self-assessment ratings

**Testing:**
- Answers persist across devices (if logged in)
- User can review/edit previous answers
- Completion screen shows all answers
- Ratings save correctly

### Phase 3: Chat Integration & Polish (Week 3)
**Estimated effort: 2-3 days**

**Deliverables:**
- ✅ Contextual prompts per step in chat
- ✅ Coaching hints (expandable)
- ✅ Download summary (JSON/PDF)
- ✅ Email summary (if email service ready)
- ✅ Visual polish (transitions, hover states)
- ✅ Mobile responsiveness

**Testing:**
- Chat suggestions change per step
- Hints provide useful guidance
- Download/email work correctly
- Mobile experience smooth
- Transitions feel calm (not jarring)

### Phase 4: Accessibility & Edge Cases (Week 4)
**Estimated effort: 2-3 days**

**Deliverables:**
- ✅ WCAG 2.2 AA compliance
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Screen reader support (ARIA labels)
- ✅ Focus management (focus trap in modal)
- ✅ Error handling (network failures, validation)
- ✅ Edge cases (incomplete sessions, timeouts)

**Testing:**
- Keyboard-only navigation works
- Screen reader announces correctly
- Focus indicators visible
- Errors handled gracefully
- Works with network offline (localStorage fallback)

---

## Accessibility Requirements

### WCAG 2.2 AA Compliance

**Keyboard Navigation:**
- ✅ All interactive elements reachable via Tab
- ✅ Logical tab order (top to bottom, left to right)
- ✅ Enter/Space activates buttons
- ✅ Escape closes modals/dropdowns
- ✅ Arrow keys navigate progress dots (optional)

**Screen Readers:**
- ✅ ARIA labels on all inputs
- ✅ ARIA live regions for auto-save notifications
- ✅ ARIA current="step" on active progress dot
- ✅ Descriptive button labels (not just "Next")
- ✅ Hidden elements marked aria-hidden="true"

**Visual:**
- ✅ Focus indicators visible (2px outline, high contrast)
- ✅ Color contrast ratios ≥4.5:1 (text/background)
- ✅ No color-only indicators (use text + color)
- ✅ Text resizable to 200% without breaking layout
- ✅ Touch targets ≥44x44px (mobile)

**Code Example - Focus Styles:**

```css
/* Focus indicators (WCAG 2.2 AA compliant) */
*:focus {
  outline: 2px solid var(--hair);
  outline-offset: 2px;
}

button:focus,
input:focus,
textarea:focus,
a:focus {
  outline: 2px solid var(--hair);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  *:focus {
    outline: 3px solid #000;
    outline-offset: 2px;
  }
}
```

**Code Example - ARIA Labels:**

```html
<!-- Progress navigation -->
<nav class="ps101-progress" aria-label="PS101 Progress">
  <button
    class="dot active"
    aria-label="Step 2: What Matters Most (current step)"
    aria-current="step"
    data-step="2"
  >
    2
  </button>
</nav>

<!-- Input with label -->
<label for="step-answer" class="visually-hidden">
  Your answer to: What matters most to you?
</label>
<textarea
  id="step-answer"
  aria-describedby="step-hint"
  aria-required="true"
  aria-invalid="false"
></textarea>

<!-- Hint text -->
<p id="step-hint" class="coaching-hint">
  Prioritize. If you could only focus on one thing, what would it be?
</p>

<!-- Auto-save notification -->
<div
  class="autosave-indicator"
  role="status"
  aria-live="polite"
  aria-atomic="true"
>
  Saved
</div>
```

**Visually Hidden Helper:**

```css
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

---

## Visual Design Patterns

### Peripheral Calm Principles (PRESERVE)

**From README_UI_SKIN.txt and current index.html:**

**Colors:**
```css
:root {
  --fg: #000;              /* Foreground text */
  --muted: #666;           /* Secondary text */
  --line: #e8e8e8;         /* Borders */
  --hair: #111;            /* Hairline accents */
  --max: 980px;            /* Max content width */
}

/* Gradients (subtle, calm) */
body {
  background: linear-gradient(135deg, #f5f5f5 0%, #eeeeee 100%);
}

.wrap, .ps101-container {
  background: linear-gradient(145deg, #ffffff 0%, #fafafa 100%);
}
```

**Shadows (Subtle Depth):**
```css
box-shadow:
  0 2px 6px rgba(0,0,0,0.06),
  0 1px 3px rgba(0,0,0,0.03);
```

**Transitions (Calm, Purposeful):**
```css
transition: all 0.2s ease; /* Not too fast, not too slow */
```

**Typography:**
```css
font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
font-size: 12px; /* Base, scale up for headings */
line-height: 1.75; /* Generous breathing room */
```

**Whitespace (Generous):**
```css
/* Prefer more spacing than less */
margin: 32px 0; /* Not 16px */
padding: 20px;  /* Not 10px */
gap: 16px;      /* Not 8px */
```

**Hover States (Subtle Lift):**
```css
.quiet:hover,
.nav-btn:hover,
.dot:hover {
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(0,0,0,0.12);
}

.quiet:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
```

### Animation Philosophy

**Duration:**
- Fast interactions: 150ms (button clicks)
- Medium interactions: 200ms (hover states, focus)
- Slow interactions: 300ms (screen transitions)

**Easing:**
- `ease` - Default (natural acceleration/deceleration)
- `ease-out` - Screen exits
- `ease-in-out` - Smooth transitions

**When to Animate:**
- ✅ Hover states (lift, shadow change)
- ✅ Focus states (outline appearance)
- ✅ Progress indicator (dot state changes)
- ✅ Auto-save notification (fade in/out)
- ❌ Content loading (no spinners unless >3s)
- ❌ Text changes (instant, not fade)
- ❌ Navigation (instant, not slide)

**Respect User Preferences:**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Testing & Validation

### Manual Testing Checklist

**Functional Testing:**
- [ ] User can start PS101 flow from welcome screen
- [ ] User can navigate forward through all 7 steps
- [ ] User can navigate backward to previous steps
- [ ] User can click progress dots to jump to completed steps
- [ ] User cannot jump to future steps (disabled)
- [ ] Textarea accepts input for each step
- [ ] Character count updates in real-time
- [ ] Validation prevents advancing with insufficient input
- [ ] Auto-save indicator shows "Saved" after 1 second
- [ ] Previous answers display correctly when expanded
- [ ] Edit button takes user back to that step
- [ ] Completion screen shows after Step 7
- [ ] All 7 answers display in completion summary
- [ ] Self-assessment sliders work
- [ ] Download summary button works
- [ ] Start Over button resets state

**Integration Testing:**
- [ ] Answers save to backend (check `wimd_outputs` table)
- [ ] State loads from backend on page refresh (if authenticated)
- [ ] localStorage fallback works (if not authenticated)
- [ ] Session persists across page refreshes
- [ ] Chat contextual prompts update per step
- [ ] Chat suggestions work when clicked
- [ ] Existing features still work (auth, file upload, trial timer)

**Visual Testing:**
- [ ] Progress dots styled correctly (completed/active/future)
- [ ] Hover states work on all interactive elements
- [ ] Focus indicators visible on keyboard nav
- [ ] Transitions feel smooth (not jarring)
- [ ] Typography readable and calm
- [ ] Whitespace feels generous (not cramped)
- [ ] Colors match Peripheral Calm tokens
- [ ] Shadows subtle (not heavy)

**Responsive Testing:**
- [ ] Layout works on desktop (>980px)
- [ ] Layout works on tablet (768-980px)
- [ ] Layout works on mobile (<768px)
- [ ] Progress dots readable on mobile
- [ ] Buttons stack vertically on mobile
- [ ] Textarea full width on mobile
- [ ] Touch targets ≥44x44px
- [ ] No horizontal scroll on mobile

**Accessibility Testing:**
- [ ] Keyboard-only navigation works (Tab, Enter, Escape)
- [ ] Screen reader announces progress ("Step 2 of 7")
- [ ] Screen reader announces current step question
- [ ] Screen reader announces auto-save status
- [ ] Focus indicators visible (2px outline)
- [ ] Color contrast ≥4.5:1 (use WebAIM tool)
- [ ] Text resizable to 200% without breaking
- [ ] ARIA labels present on all inputs
- [ ] ARIA live regions announce dynamic content

**Error Handling:**
- [ ] Network failure shows error message
- [ ] Backend timeout handled gracefully
- [ ] Invalid session shows login prompt
- [ ] Validation errors clear and helpful
- [ ] Auto-save failures retry after delay

### Automated Testing (Optional)

**Golden Dataset Tests:**

```javascript
// Test PS101 flow with known good data
describe('PS101 Flow', () => {
  const GOLDEN_ANSWERS = {
    1: "I've been a marketing coordinator for 3 years but feel stuck. I want to move into a strategic role with more autonomy and impact on company direction.",
    2: "Having more autonomy and being able to shape strategy, not just execute someone else's plans.",
    3: "I know I have strong analytical skills from the Q3 campaign analysis. My manager says I'm good at presenting data. I've been in this role for 3 years with no promotion path discussed.",
    4: "What specific skills do strategic marketing roles require that I don't have yet? What's the typical career path from coordinator to strategist? What internal opportunities exist at my company?",
    5: "1) Ask for more strategic projects in my current role to build experience. 2) Look for strategy roles at other companies where I can make a lateral move. 3) Get a marketing strategy certification to strengthen my credentials. 4) Network with people in strategic roles to learn from their paths.",
    6: "Ask my manager if I can lead the strategy portion of next quarter's planning meeting, specifically the competitive analysis and positioning recommendations.",
    7: "Schedule a 1:1 with my manager by Friday to discuss taking on the strategic planning work for Q1. Prepare a proposal showing my analytical work from Q3 as evidence I'm ready."
  };

  it('should accept all golden answers', () => {
    PS101_STEPS.forEach(step => {
      const answer = GOLDEN_ANSWERS[step.number];
      const isValid = validateAnswer(step, answer);
      expect(isValid).toBe(true);
    });
  });

  it('should progress through all 7 steps', () => {
    const state = PS101State;
    state.reset();

    PS101_STEPS.forEach(step => {
      expect(state.currentStep).toBe(step.number);
      state.setAnswer(step.number, GOLDEN_ANSWERS[step.number]);
      state.nextStep();
    });

    expect(state.completed).toBe(true);
  });
});
```

**Regression Tests:**

```javascript
// Ensure existing features still work
describe('Existing Features', () => {
  it('should preserve auth modal functionality', () => {
    // Test login modal still opens
    // Test registration still works
  });

  it('should preserve chat drawer functionality', () => {
    // Test chat opens/closes
    // Test messages send/receive
  });

  it('should preserve file upload functionality', () => {
    // Test file picker works
    // Test upload processes
  });

  it('should preserve trial timer functionality', () => {
    // Test 5-min timer starts for unauthenticated
    // Test timer shows remaining time
  });
});
```

---

## Implementation Checklist

### Pre-Implementation (Before Cursor Starts)

- [ ] Review all source documents (this spec + references)
- [ ] Understand Peripheral Calm aesthetic (README_UI_SKIN.txt)
- [ ] Study current index.html patterns (IIFE, event delegation)
- [ ] Confirm access to all referenced files
- [ ] Set up local development environment
- [ ] Test backend API endpoints work

### Phase 1: Core Flow (Week 1)

- [ ] Create PS101State object (vanilla JS IIFE)
- [ ] Define PS101_STEPS array (7 steps with metadata)
- [ ] Implement renderWelcomeScreen()
- [ ] Implement renderCurrentStep()
- [ ] Create progress indicator HTML/CSS
- [ ] Create question display HTML/CSS
- [ ] Create textarea input HTML/CSS
- [ ] Create navigation buttons HTML/CSS
- [ ] Add event listeners (start, next, back, textarea input)
- [ ] Implement validateCurrentStep()
- [ ] Implement auto-save to localStorage
- [ ] Test full flow (all 7 steps)

### Phase 2: Backend Integration (Week 2)

- [ ] Implement autosaveAnswer() to backend
- [ ] Implement loadFromBackend() on init
- [ ] Test backend persistence (check database)
- [ ] Create previous answers HTML/CSS
- [ ] Implement renderPreviousAnswers()
- [ ] Add edit functionality (click to go back)
- [ ] Create completion screen HTML/CSS
- [ ] Implement renderCompletionScreen()
- [ ] Add self-assessment ratings
- [ ] Test state persistence across sessions

### Phase 3: Chat & Polish (Week 3)

- [ ] Add contextual prompts per step
- [ ] Implement updateChatContextualPrompts()
- [ ] Add chat suggestions HTML/CSS
- [ ] Create coaching hints (expandable)
- [ ] Implement downloadSummary() (JSON export)
- [ ] Implement emailSummary() (if email service ready)
- [ ] Add transitions/animations
- [ ] Test mobile responsiveness
- [ ] Polish hover states
- [ ] Test on multiple browsers

### Phase 4: Accessibility (Week 4)

- [ ] Add ARIA labels to all interactive elements
- [ ] Add ARIA live regions for notifications
- [ ] Test keyboard-only navigation
- [ ] Add focus indicators (2px outline)
- [ ] Test with screen reader (NVDA/JAWS/VoiceOver)
- [ ] Check color contrast ratios (WebAIM tool)
- [ ] Add visually-hidden labels where needed
- [ ] Test text resize to 200%
- [ ] Add prefers-reduced-motion support
- [ ] Test error handling edge cases

### Post-Implementation (After Cursor Completes)

- [ ] Code review (check IIFE pattern, no globals)
- [ ] Visual review (matches Peripheral Calm aesthetic)
- [ ] Functional testing (manual checklist above)
- [ ] Accessibility audit (WCAG 2.2 AA)
- [ ] Performance check (no lag on transitions)
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile device testing (iOS, Android)
- [ ] Integration testing (backend API calls work)
- [ ] User acceptance testing (beta users)
- [ ] Deploy to production (Railway + Netlify)

---

## Success Criteria (Final Validation)

### User Experience Goals

**Clarity:**
- [ ] User understands what PS101 is from welcome screen
- [ ] User knows where they are in flow (progress indicator)
- [ ] User knows what to do (clear question, helpful hint)
- [ ] User knows progress is saved (auto-save indicator)
- [ ] User can review previous answers easily

**Encouragement:**
- [ ] Progress indicator feels encouraging (not pressuring)
- [ ] Questions feel conversational (not interrogative)
- [ ] Interface guides (doesn't control)
- [ ] Completion feels like accomplishment (not bureaucracy)
- [ ] User feels supported (coaching hints, chat available)

**Usability:**
- [ ] User can complete flow in 15-30 minutes
- [ ] User can edit previous answers without confusion
- [ ] User can pause and resume (state persists)
- [ ] Mobile experience smooth (no pinch-zoom needed)
- [ ] No confusion about what to do next

### Technical Goals

**Architecture:**
- [ ] Zero framework dependencies
- [ ] Single HTML file (frontend/index.html)
- [ ] Works with existing API contracts
- [ ] No breaking changes to current features
- [ ] Follows existing IIFE patterns

**Performance:**
- [ ] Page load <2 seconds (no added bloat)
- [ ] Transitions smooth (60fps, no jank)
- [ ] Auto-save doesn't block UI
- [ ] Network failures handled gracefully

**Accessibility:**
- [ ] WCAG 2.2 AA compliant
- [ ] Keyboard navigation works
- [ ] Screen reader announces correctly
- [ ] Focus indicators visible
- [ ] Works with 200% text zoom

**Quality:**
- [ ] No console errors
- [ ] No visual regressions
- [ ] No functional regressions
- [ ] Code follows existing style
- [ ] Comments explain complex logic

### Product Goals

**Alignment:**
- [ ] Matches Peripheral Calm aesthetic perfectly
- [ ] Supports self-efficacy model (user-driven)
- [ ] Integrates with existing coach/chat
- [ ] Preserves all existing features
- [ ] Ready for MVP validation (10+ beta users)

**Metrics (to track after launch):**
- [ ] PS101 completion rate >60%
- [ ] Clarity score increase ≥3 points (1-10)
- [ ] Action score ≥7 (likelihood of follow-through)
- [ ] 30-day retention ≥40%
- [ ] User feedback positive (>4/5 stars)

---

## Key Design Decisions (Rationale)

### Decision 1: Single-Screen Step Progression

**Options Considered:**
- Wizard flow (full screen per step)
- Sidebar navigation (all steps visible)
- Accordion (expand/collapse)
- Single-screen progression (chosen)

**Rationale:**
- Maintains focus on one question at a time (Peripheral Calm principle)
- Reduces cognitive load (user sees one clear task)
- Easy to implement in vanilla JS (no complex routing)
- Supports linear PS101 flow (steps must be in order)
- Previous answers available but not distracting (expandable)

### Decision 2: Minimal Progress Indicator

**Options Considered:**
- Progress bar (horizontal/vertical)
- Breadcrumbs with step names
- Visual timeline with icons
- Simple dots (chosen)

**Rationale:**
- Dots are calm, not bureaucratic
- Takes minimal space (doesn't dominate)
- Clickable for navigation (completed steps)
- Accessible (ARIA labels provide context)
- Matches aesthetic (simple, geometric)

### Decision 3: Keep Existing Chat Drawer

**Options Considered:**
- Remove chat (PS101 only)
- Side panel (always visible)
- Mode toggle (guided vs. chat)
- Keep bottom drawer + enhance (chosen)

**Rationale:**
- Bottom drawer already works (preserve what's good)
- Contextual prompts make it PS101-aware (adds value)
- User can choose when to ask for help (self-efficacy)
- Doesn't compete with PS101 questions (peripheral, not central)
- Mobile-friendly (drawer slides up, doesn't take permanent space)

### Decision 4: Expandable Previous Answers

**Options Considered:**
- Always visible (sidebar/timeline)
- Hidden unless editing
- Modal popup
- Expandable summary (chosen)

**Rationale:**
- Available but not distracting (user controls visibility)
- Doesn't clutter current step
- Easy to review/edit (clear action buttons)
- Feels like progress log (encouraging)
- Works on mobile (expands vertically)

### Decision 5: No Adaptive UI (Yet)

**Options Considered:**
- State machine with telemetry (detect struggle)
- Dynamic UI morphing (calm/focus/recovery)
- Static, simple UI (chosen)

**Rationale:**
- MVP scope - validate foundation first
- Conflicts with self-efficacy (system shouldn't intervene)
- Adds complexity (React/XState/telemetry)
- PS101 is linear - adaptive UI not needed
- Can add later if user research shows need

---

## Ambiguities Requiring User Input

### 1. PS101 Step Count Clarification

**Issue:** Documentation shows 3 different versions:
- Source doc (Oct 2): "10-step PS101"
- Project brief (Oct 22): "7-step framework"
- Current implementation: 3 questions

**This spec uses:** 7 steps (from project brief + design brief)

**Confirmation needed:** Is 7 steps canonical?

### 2. Email Service Integration

**Issue:** Password reset sends placeholder message. Email summary feature depends on email service.

**This spec includes:** Email summary button (disabled until service ready)

**Confirmation needed:** When will email service be integrated?

### 3. Nate Skills Framework PDFs

**Issue:** Redesign doc references Nate Skills PDFs as validation source. Not found on local system.

**This spec:** Proceeds without them (assumes not critical for vanilla JS UI)

**Confirmation needed:** Should these be located and reviewed?

### 4. Download Summary Format

**Issue:** Unclear if summary should be JSON (developer-friendly) or PDF (user-friendly)

**This spec includes:** JSON download (easy to implement)

**Confirmation needed:** Do users need PDF? (requires library or backend generation)

### 5. Self-Assessment Requirement

**Issue:** Unclear if self-assessment is mandatory or optional after Step 7

**This spec includes:** Optional ratings (user can skip)

**Confirmation needed:** Should it be required?

---

## Estimated Implementation Effort

### Breakdown by Phase

**Phase 1: Core PS101 Flow**
- HTML structure: 4 hours
- CSS styling: 4 hours
- JavaScript state management: 6 hours
- Event handlers: 4 hours
- Validation: 3 hours
- Total: **21 hours (3 days)**

**Phase 2: Backend Integration & Previous Answers**
- Backend API calls: 4 hours
- State loading: 3 hours
- Previous answers UI: 4 hours
- Completion screen: 4 hours
- Testing: 4 hours
- Total: **19 hours (2.5 days)**

**Phase 3: Chat Integration & Polish**
- Contextual prompts: 3 hours
- Coaching hints: 2 hours
- Download/email: 3 hours
- Visual polish: 4 hours
- Mobile responsive: 4 hours
- Total: **16 hours (2 days)**

**Phase 4: Accessibility & Edge Cases**
- ARIA labels: 3 hours
- Keyboard navigation: 4 hours
- Screen reader testing: 3 hours
- Error handling: 4 hours
- Edge case fixes: 4 hours
- Total: **18 hours (2.5 days)**

**Overall Estimate: 74 hours (10 working days / 2 calendar weeks)**

**Assumptions:**
- Cursor AI assistance reduces manual coding time by ~30%
- Existing patterns (IIFE, event delegation) speed implementation
- No major refactoring needed (preserves current architecture)
- Backend API endpoints work as documented

**Risk Factors:**
- Backend API issues: +2-3 days
- Unexpected browser compatibility: +1-2 days
- Accessibility fixes: +1-2 days
- User feedback requiring changes: +1-3 days

**Best Case:** 10 days
**Most Likely:** 12-14 days
**Worst Case:** 18-20 days

---

## File Location

**Specification saved to:**
`/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/docs/MOSAIC_UI_IMPLEMENTATION_SPEC_V1_FOR_CURSOR.md`

**Related files to include in Cursor workspace:**
- `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/frontend/index.html` (current working implementation)
- `/Users/damianseguin/AI_Workspace/WIMD-Railway-Deploy-Project/CLAUDE.md` (architecture context)
- `/Users/damianseguin/AI_Workspace/Planning/strategy_desktop/context_library/work_playbooks.md` (PS101 coaching playbook)
- `/Users/damianseguin/AI_Workspace/Planning/strategy_desktop/project_briefs/mosaic_brief.md` (product philosophy)
- `/Users/damianseguin/AI_Workspace/Mosaic/README_UI_SKIN.txt` (Peripheral Calm design tokens)

---

**END OF SPECIFICATION**

**Status:** Complete and ready for Cursor implementation

**Next Steps:**
1. User reviews spec and confirms decisions
2. User resolves ambiguities (if any)
3. User opens Cursor in WIMD-Railway-Deploy-Project workspace
4. User provides this spec to Cursor
5. Cursor implements Phase 1 (Core PS101 Flow)
6. User tests and provides feedback
7. Cursor iterates through Phases 2-4
