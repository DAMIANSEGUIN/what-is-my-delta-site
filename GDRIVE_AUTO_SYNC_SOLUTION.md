# Google Drive Auto-Sync Solution
**Date:** 2025-10-26
**Purpose:** Automatic sync to GDrive so ChatGPT can reference latest files

---

## Problem Solved

ChatGPT needs to reference the latest project files to build the interface redesign plan. You will forget to manually sync files. This solution makes GDrive sync **completely automatic**.

---

## How It Works

### 1. Git Post-Commit Hook (Automatic)

**File:** `.git/hooks/post-commit`

**Behavior:**
- Triggers after EVERY git commit
- Runs `rclone sync` in background (non-blocking)
- Syncs only essential files (excludes venv, .git, node_modules, etc.)
- Logs to `/tmp/gdrive-sync.log`

**Result:** Every time you commit code, GDrive is automatically updated within ~30-60 seconds.

### 2. Initial Manual Sync (One-Time)

**Command:**
```bash
./scripts/initial_gdrive_sync.sh
```

**Purpose:**
- First-time sync of all current files to GDrive
- After this runs once, git hook handles all future syncs
- Takes 2-5 minutes for initial upload

---

## Setup Instructions

### Step 1: Run Initial Sync

```bash
cd /Users/damianseguin/Downloads/WIMD-Railway-Deploy-Project
./scripts/initial_gdrive_sync.sh
```

Wait for completion (shows progress bar).

### Step 2: Share GDrive Folder with ChatGPT

1. Open Google Drive in browser
2. Find folder: `WIMD-Railway-Deploy-Project`
3. Get shareable link or give ChatGPT access
4. Tell ChatGPT: "Reference files in my Google Drive folder: WIMD-Railway-Deploy-Project"

### Step 3: Normal Workflow (No Manual Steps)

From now on, just work normally:

```bash
# Make changes to files
vim mosaic_ui/index.html

# Commit changes
git add mosaic_ui/index.html
git commit -m "Update interface design"

# GDrive auto-syncs in background (no action needed!)
# Check sync status:
tail -f /tmp/gdrive-sync.log
```

---

## What Gets Synced

### ✅ Included
- All source code (`api/`, `mosaic_ui/`, `scripts/`)
- All documentation (`.md` files)
- Configuration files (`requirements.txt`, `.env.railway`)
- Specifications (`Planning/`, `docs/`)
- Database migrations (`data/migrations/`)

### ❌ Excluded (Not Needed by ChatGPT)
- `.git/` (version control internals)
- `node_modules/` (huge, not needed)
- `venv/`, `.venv/`, `.test-venv/`, `.claude-run/` (Python virtual envs)
- `__pycache__/`, `*.pyc` (compiled Python)
- `.DS_Store`, `*.log` (system files)

---

## Verification

### Check if Hook is Active

```bash
ls -la .git/hooks/post-commit
# Should show: -rwxr-xr-x (executable)
```

### Test the Hook

```bash
# Make a dummy commit
touch test_file.txt
git add test_file.txt
git commit -m "Test GDrive sync"

# Check sync log (wait 5 seconds)
sleep 5
tail -10 /tmp/gdrive-sync.log
# Should show: "✅ GDrive sync complete"
```

### Check GDrive Contents

```bash
/Users/damianseguin/coachvox_tools/bin/rclone ls gdrive:WIMD-Railway-Deploy-Project | head -20
```

---

## Troubleshooting

### Sync Not Running

```bash
# Check if hook is executable
chmod +x .git/hooks/post-commit

# Check if rclone is configured
/Users/damianseguin/coachvox_tools/bin/rclone listremotes
# Should show: gdrive:
```

### Sync Failing

```bash
# Check sync log for errors
cat /tmp/gdrive-sync.log

# Test rclone connection
/Users/damianseguin/coachvox_tools/bin/rclone lsd gdrive:
# Should list Google Drive folders
```

### Force Manual Sync

```bash
# If you need to sync immediately without waiting for commit
/Users/damianseguin/coachvox_tools/bin/rclone sync . gdrive:WIMD-Railway-Deploy-Project \
  --exclude ".git/**" \
  --exclude "venv/**" \
  --exclude "node_modules/**" \
  --fast-list \
  --progress
```

---

## Architecture

```
┌─────────────────┐
│  Git Commit     │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────┐
│  .git/hooks/post-commit     │
│  (automatic trigger)        │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  rclone sync (background)   │
│  - Excludes .git, venv      │
│  - Fast-list mode           │
│  - 4 parallel transfers     │
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  Google Drive Folder        │
│  WIMD-Railway-Deploy-Project│
└────────┬────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  ChatGPT References Files   │
│  (always has latest)        │
└─────────────────────────────┘
```

---

## Benefits

1. **Zero manual steps** - Sync happens automatically on commit
2. **Non-blocking** - Background sync doesn't slow down git operations
3. **Efficient** - Only syncs changed files (rclone sync)
4. **Selective** - Excludes unnecessary large files
5. **Verifiable** - Log file shows sync history
6. **Reliable** - Uses existing rclone configuration

---

## Next Steps

1. **NOW:** Run `./scripts/initial_gdrive_sync.sh` (one-time setup)
2. **THEN:** Share GDrive folder with ChatGPT
3. **DONE:** All future commits auto-sync to GDrive

---

**This solution requires ZERO ongoing manual work from you.**

The git hook handles everything automatically after the initial sync.

---

**Scout reporting:** GDrive auto-sync solution implemented. Ready for initial sync execution.
