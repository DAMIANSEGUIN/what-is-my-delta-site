# Cursor UI Bug Report - Button Overlap Issue

**Date:** 2025-11-03  
**Reported By:** User (Damian)  
**Issue:** Terminal command execution buttons overlapping

---

## Problem Description

When viewing terminal command execution prompts in Cursor, the **"Run"** button is overlapping the **"Stop"** button. This causes users to accidentally stop commands when they intend to run them.

### User Experience Impact

- User clicks "Run" but the click registers as "Stop" due to overlap
- Commands are interrupted unintentionally
- Workflow disruption and frustration
- User has to manually clarify intent: "i did not reject that, the button for run is overlapping reject"

---

## Reproduction Steps

1. AI agent proposes a terminal command
2. Command box appears with Run/Stop buttons
3. Buttons are visually overlapping
4. User clicks "Run" but system registers "Stop"

---

## Expected Behavior

- Run and Stop buttons should be clearly separated
- No visual overlap between buttons
- Click targets should match visual boundaries
- Clear visual distinction between action buttons

---

## Requested Action

Please fix the button layout in the terminal command execution UI to prevent overlap and ensure accurate click detection.

---

## Context

This bug was encountered during a critical merge operation where:
- Files needed to be synced (`frontend/index.html` ↔ `mosaic_ui/index.html`)
- Multiple verification commands were being executed
- User had to manually clarify intent multiple times due to button overlap

---

**Priority:** High - Affects user workflow and command execution accuracy

---

## Update - 2025-11-04

**Status:** Issue persists across sessions

The overlapping Run/Stop button issue continues to occur. User reports: "that issues with the overlapping stop run is persisting"

This is a persistent UI bug that affects:
- Command execution accuracy
- User workflow confidence
- Agent-user interaction reliability

**Action Required:** Cursor team needs to investigate and fix the button layout/click target alignment in the terminal command execution UI component.

