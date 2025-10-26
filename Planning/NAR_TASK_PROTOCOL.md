# NAR Task Protocol - How to Structure Tasks for Netlify Agent Runners
**Date:** 2025-10-26
**Priority:** HIGH
**Status:** ACTIVE

---

## What Went Wrong

**This session:**
- I created `NETLIFY_AGENT_RAILWAY_DEBUG.md` (detailed technical brief)
- I created `PROMPT_FOR_NETLIFY_AGENT.txt` (copy/paste prompt)
- User shared with NARs
- **NARs read the WRONG file** (`NETLIFY_AGENT_TASK.md` - old draggable windows task)
- NARs completed wrong task
- Wasted time

**Root cause:** Too many files, unclear which one to use, old files not cleaned up.

---

## New Protocol: Two-File System

### File 1: SHORT_TASK.txt (For User to Share)

**Purpose:** Quick, scannable task description for NARs to start with

**Content:**
- Project directory path
- 2-3 sentence problem summary
- Quick file list (5-10 files max)
- Clear deliverable
- Link to detailed brief

**Format:**
```txt
PROJECT: /path/to/project
TASK: [One sentence description]

PROBLEM:
- [Bullet point 1]
- [Bullet point 2]

KEY FILES:
- file1.py (what it does)
- file2.py (what it does)

DELIVERABLE: [What success looks like]

DETAILS: Read NAR_DETAILED_BRIEF.md for full context
```

**Length:** 15-20 lines max

---

### File 2: NAR_DETAILED_BRIEF.md (Deeper Dive)

**Purpose:** Complete technical context if NARs need it

**Content:**
- Full problem description
- Complete file tree
- Environment variables
- Code snippets
- Diagnosis steps
- Expected outcomes
- Historical context

**Length:** As long as needed

---

## File Naming Convention

**For each NAR task, create ONLY these 2 files:**

```
NAR_TASK_[DESCRIPTION].txt           # Short version to share
NAR_TASK_[DESCRIPTION]_BRIEF.md      # Detailed version
```

**Example:**
```
NAR_TASK_RAILWAY_BOOKING_ROUTES.txt
NAR_TASK_RAILWAY_BOOKING_ROUTES_BRIEF.md
```

---

## Cleanup Protocol

**BEFORE creating new NAR task files:**
1. Search for old `NAR_TASK_*` files
2. Rename them with `_COMPLETED_` or `_ARCHIVED_` prefix
3. Or move to `Planning/NAR_Archive/` folder
4. This prevents NARs from reading stale tasks

**Example:**
```bash
# Before new task
mv NAR_TASK_DRAGGABLE.md Planning/NAR_Archive/NAR_TASK_DRAGGABLE_COMPLETED.md

# Then create new task
touch NAR_TASK_RAILWAY_ROUTES.txt
```

---

## What User Should Share

**User copies/pastes:**
1. Contents of `NAR_TASK_[NAME].txt` (short version)
2. Mentions: "Full details in NAR_TASK_[NAME]_BRIEF.md if needed"

**NARs will:**
1. Read the short version first
2. Understand the task immediately
3. Read detailed brief only if they need more context

---

## Example: Good Structure

### NAR_TASK_RAILWAY_BOOKING_ROUTES.txt
```
PROJECT: /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project

TASK: Fix Railway booking routes returning 404

PROBLEM:
- Booking routes deployed but not loading
- GET /booking/promo/WIMD25 returns 404 (should be 401)
- Routes missing from /openapi.json

KEY FILES:
- api/booking.py (booking router - NOT LOADING)
- api/google_calendar_service.py (Google Calendar integration)
- api/index.py (lines 106-113: router registration)

DIAGNOSE:
- Check Railway logs for import errors
- Verify dependencies in requirements.txt
- Test if migrations ran

DELIVERABLE:
- /booking/* routes return proper HTTP codes (not 404)
- Routes appear in /openapi.json

FULL DETAILS: Read NAR_TASK_RAILWAY_BOOKING_ROUTES_BRIEF.md
```

### NAR_TASK_RAILWAY_BOOKING_ROUTES_BRIEF.md
```markdown
[Full 100+ line detailed technical brief with:
- Complete file tree
- All environment variables
- Code snippets
- Full diagnosis steps
- Historical context
- etc.]
```

---

## Benefits

**Short file approach:**
- ✅ NARs see task immediately
- ✅ No confusion about which file to read
- ✅ Scannable in 30 seconds
- ✅ Clear deliverable

**Detailed file available:**
- ✅ If NARs need more context, it's there
- ✅ Prevents information overload upfront
- ✅ User can reference it too

**Cleanup protocol:**
- ✅ No stale tasks
- ✅ Clear which task is current
- ✅ History preserved in archive

---

## Implementation Checklist

**When creating NAR task:**

```
□ Search for old NAR_TASK_* files
□ Archive/rename old files
□ Create SHORT version (.txt, 15-20 lines)
□ Create DETAILED version (_BRIEF.md)
□ User shares SHORT version
□ Mention detailed version is available
```

---

## What I Did Wrong This Session

**Created:**
- `NETLIFY_AGENT_RAILWAY_DEBUG.md` (good detailed file)
- `PROMPT_FOR_NETLIFY_AGENT.txt` (good short file)

**But also:**
- `NETLIFY_AGENT_TASK.md` already existed (old draggable windows task)
- Didn't clean it up
- NARs read the wrong one

**Should have:**
1. Archived old `NETLIFY_AGENT_TASK.md`
2. Created `NAR_TASK_RAILWAY_ROUTES.txt` (short)
3. Created `NAR_TASK_RAILWAY_ROUTES_BRIEF.md` (detailed)
4. Clean file structure, no confusion

---

## File Location

**Active tasks:** Project root
**Completed tasks:** `Planning/NAR_Archive/`

**Pattern:**
```
/project/
├── NAR_TASK_CURRENT.txt              # Active short task
├── NAR_TASK_CURRENT_BRIEF.md         # Active detailed task
└── Planning/
    └── NAR_Archive/
        ├── NAR_TASK_DRAGGABLE_COMPLETED.md
        └── NAR_TASK_OTHER_COMPLETED.txt
```

---

**Status:** ACTIVE - Use for all future NAR tasks

**Cross-Reference:**
- Works with 00_READ_TWICE_PROTOCOL.md
- Works with NETLIFY_AGENT_PROTOCOL.md

---

**END OF PROTOCOL**
