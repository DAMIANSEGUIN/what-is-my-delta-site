# DOWNLOADS FOLDER INVENTORY & CLEANUP PLAN
**Date**: 2025-10-07
**Phase**: 1 - Workspace Foundation
**Status**: AWAITING APPROVAL

---

## EXECUTIVE SUMMARY

**Current State**: 27 duplicate/related project folders consuming disk space and creating confusion
**Primary Issues**:
- Multiple WIMD project copies (6+)
- Multiple Mosaic/RRT integration folders (10+)
- Old job data CSV files (7 files, ~5MB total from August)
- Obsolete backup folders and archives

**Recommendation**: Archive 70% of content, keep only active projects

---

## FOLDER ANALYSIS

### ACTIVE PROJECTS (KEEP)

| Folder | Size | Last Modified | Rationale |
|--------|------|---------------|-----------|
| **WIMD-Railway-Deploy-Project** | 6.3MB | 2025-10-07 | PRIMARY - Active production project |
| **Foundation_Vault** | 1.6MB | 2025-09-27 | Active knowledge base (confirm with user) |

**Action**: KEEP - No changes

---

### OBSOLETE WIMD COPIES (ARCHIVE)

| Folder | Size | Last Modified | Status |
|--------|------|---------------|--------|
| WIMD_PUBLIC_TEST | 616KB | 2025-09-14 | Old test deployment |
| WIMD_FRESH_DEPLOY | 324KB | 2025-09-15 | Superseded by Railway deploy |
| wimdtest | 312KB | 2025-09-14 | Test instance |
| WIMD_Hosting_Starter | 52KB | Unknown | Obsolete starter |
| WIMD-Railway-Deploy-Backup-20250919-005711 | Unknown | 2025-09-24 | Old backup |

**Total Space**: ~1.3MB
**Action**: ARCHIVE to `~/Archives/Pre-Recovery-2025-10-07/WIMD-backups/`

---

### DUPLICATE MOSAIC/RRT FOLDERS (ARCHIVE)

| Folder | Size | Last Modified | Status |
|--------|------|---------------|--------|
| Mosaic | 16KB | Unknown | Likely obsolete |
| Mosaic Launcher.app | 20KB | Unknown | Old launcher |
| mosaic-api | 184KB | Unknown | Superseded |
| mosaic-frontend | 80KB | 2025-09-11 | Superseded |
| mosaic_vault_kit | 16KB | 2025-09-27 | Duplicate |
| MOSAIC_UPLOAD_FILES | 140KB | 2025-09-27 | Old upload test |
| RRT_Mosaic_Integration_Starter | 36KB | 2025-09-27 | Duplicate |
| RRT_Mosaic_Integration_Starter (1) | 72KB | 2025-09-27 | Duplicate |
| RRT_Mosaic_Integration_Starter (4) | 16KB | 2025-09-18 | Duplicate |

**Total Space**: ~580KB
**Action**: ARCHIVE to `~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/`

---

### OLD TOOL/UTILITY FOLDERS (ARCHIVE)

| Folder | Size | Last Modified | Status |
|--------|------|---------------|--------|
| OpportunityBridge | 992KB | 2025-09-27 | Pre-Railway project |
| jsm_csv_runner | 12KB | Unknown | Old version |
| jsm_csv_runner_v2 | 28KB | Unknown | Old version |
| jsm_csv_runner_v3 | 24KB | Unknown | Old version |
| jsm_csv_runner_v3_fixed | 24KB | 2025-09-27 | Replaced by current |
| jsm_review_v1 | 16KB | Unknown | Old review tool |
| jobsearchmaster | 36KB | Unknown | Obsolete |
| no_more_copy_paste_toolkit | 36KB | 2025-09-25 | Utility (confirm if needed) |
| ai_partner_finder | 24KB | Unknown | Old experiment |
| ai_partner_finder-1 | 28KB | Unknown | Duplicate |

**Total Space**: ~1.2MB
**Action**: ARCHIVE to `~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/`

---

### LOOSE FILES TO ARCHIVE

#### Old Job Data CSVs (August 2025)
```
jobleads_batch_20250825_134031_with_header.csv (936KB)
jobleads_batch_20250825_134031_data.csv (936KB)
jobleads_batch_20250825_134451_with_header.csv (834KB)
jobleads_batch_20250825_134451_data.csv (834KB)
jobleads_batch_20250825_124848_with_header.csv (811KB)
jobleads_batch_20250825_124848_data.csv (811KB)
jobleads_batch_20250825_123236.csv (714KB)
```
**Total**: ~5MB of old job data
**Action**: ARCHIVE to `~/Archives/Pre-Recovery-2025-10-07/Job-data-Aug2025/`

#### Old Prompt CSVs (August 2025)
```
Prompt_lastgood_cleaned_with_category_AI.csv (140KB)
Prompt_lastgood_FLATTENED2COL_with_categories.csv (136KB)
Prompt_lastgood_FLATTENED2COL_with_categories_TAILCLEAN_v2.csv (135KB)
Prompt_lastgood_FLATTENED2COL_with_categories_TAILCLEAN.csv (135KB)
Prompt_lastgood_finalmerged_STRICTQUOTE.csv (132KB)
Prompt.csv (132KB)
```
**Total**: ~810KB of prompt data
**Action**: ARCHIVE to `~/Archives/Pre-Recovery-2025-10-07/Prompts-legacy/`

#### Old Zip Archives
```
WIMD_PUBLIC_TEST.zip (190KB)
ResumeRewrite_FullPackage.zip (147KB)
Foundation_Vault.zip (136KB)
```
**Total**: ~473KB
**Action**: DELETE (contents already exist as folders or obsolete)

#### Miscellaneous Files
```
PHASE_3_DEPLOYMENT_COMPLETE.md (6KB, 2025-10-03)
CLAUDE.md (5KB, 2025-10-03)
V1_PRODUCTION_STATUS.md (2KB, 2025-10-03)
delta-feedback.json (175B, 2025-10-01)
delta-feedback (1).json (175B, 2025-10-01)
Damian (212KB, 2025-09-18) - unclear what this is
```
**Action**: ARCHIVE to `~/Archives/Pre-Recovery-2025-10-07/Misc/` (review Damian file before archiving)

---

## ARCHIVE STRUCTURE

```
~/Archives/Pre-Recovery-2025-10-07/
├── WIMD-backups/
│   ├── WIMD_PUBLIC_TEST/
│   ├── WIMD_FRESH_DEPLOY/
│   ├── wimdtest/
│   ├── WIMD_Hosting_Starter/
│   └── WIMD-Railway-Deploy-Backup-20250919-005711/
├── Mosaic-old-versions/
│   ├── Mosaic/
│   ├── Mosaic Launcher.app/
│   ├── mosaic-api/
│   ├── mosaic-frontend/
│   ├── mosaic_vault_kit/
│   ├── MOSAIC_UPLOAD_FILES/
│   └── RRT_Mosaic_Integration_Starter (all copies)/
├── Tools-legacy/
│   ├── OpportunityBridge/
│   ├── jsm_csv_runner (all versions)/
│   ├── jobsearchmaster/
│   ├── no_more_copy_paste_toolkit/
│   └── ai_partner_finder (both copies)/
├── Job-data-Aug2025/
│   └── (all jobleads CSV files)
├── Prompts-legacy/
│   └── (all Prompt CSV files)
└── Misc/
    ├── PHASE_3_DEPLOYMENT_COMPLETE.md
    ├── CLAUDE.md
    ├── V1_PRODUCTION_STATUS.md
    ├── delta-feedback files
    └── Damian (needs review)
```

---

## IMPACT SUMMARY

### Space Savings
- **Folders archived**: ~3.1MB
- **CSV files archived**: ~5.8MB
- **Zip files deleted**: ~473KB
- **Misc files archived**: ~225KB
- **Total space reclaimed**: ~9.6MB

### Clutter Reduction
- **Before**: 27 project-related folders + 20+ loose files
- **After**: 2 active project folders + current work files
- **Reduction**: ~70% of items removed from Downloads

### Performance Impact
- Reduced Finder indexing overhead
- Faster spotlight searches
- Cleaner working environment
- Eliminated confusion from duplicate folders

---

## EXECUTION PLAN

### Step 1: Create Archive Directory
```bash
mkdir -p ~/Archives/Pre-Recovery-2025-10-07/{WIMD-backups,Mosaic-old-versions,Tools-legacy,Job-data-Aug2025,Prompts-legacy,Misc}
```

### Step 2: Move WIMD Backups
```bash
cd ~/Downloads
mv WIMD_PUBLIC_TEST ~/Archives/Pre-Recovery-2025-10-07/WIMD-backups/
mv WIMD_FRESH_DEPLOY ~/Archives/Pre-Recovery-2025-10-07/WIMD-backups/
mv wimdtest ~/Archives/Pre-Recovery-2025-10-07/WIMD-backups/
mv WIMD_Hosting_Starter ~/Archives/Pre-Recovery-2025-10-07/WIMD-backups/
mv WIMD-Railway-Deploy-Backup-20250919-005711 ~/Archives/Pre-Recovery-2025-10-07/WIMD-backups/
```

### Step 3: Move Mosaic Old Versions
```bash
mv Mosaic ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv "Mosaic Launcher.app" ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv mosaic-api ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv mosaic-frontend ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv mosaic_vault_kit ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv MOSAIC_UPLOAD_FILES ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv RRT_Mosaic_Integration_Starter ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv "RRT_Mosaic_Integration_Starter (1)" ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
mv "RRT_Mosaic_Integration_Starter (4)" ~/Archives/Pre-Recovery-2025-10-07/Mosaic-old-versions/
```

### Step 4: Move Legacy Tools
```bash
mv OpportunityBridge ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv jsm_csv_runner ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv jsm_csv_runner_v2 ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv jsm_csv_runner_v3 ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv jsm_csv_runner_v3_fixed ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv jsm_review_v1 ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv jobsearchmaster ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv no_more_copy_paste_toolkit ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv ai_partner_finder ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
mv ai_partner_finder-1 ~/Archives/Pre-Recovery-2025-10-07/Tools-legacy/
```

### Step 5: Move Old CSV Data
```bash
mv jobleads_batch_*.csv ~/Archives/Pre-Recovery-2025-10-07/Job-data-Aug2025/
mv Prompt*.csv ~/Archives/Pre-Recovery-2025-10-07/Prompts-legacy/
mv Prompt_lastgood* ~/Archives/Pre-Recovery-2025-10-07/Prompts-legacy/
```

### Step 6: Delete Duplicate Zips
```bash
rm WIMD_PUBLIC_TEST.zip
rm ResumeRewrite_FullPackage.zip
rm Foundation_Vault.zip
```

### Step 7: Move Miscellaneous Files
```bash
mv PHASE_3_DEPLOYMENT_COMPLETE.md ~/Archives/Pre-Recovery-2025-10-07/Misc/
mv CLAUDE.md ~/Archives/Pre-Recovery-2025-10-07/Misc/
mv V1_PRODUCTION_STATUS.md ~/Archives/Pre-Recovery-2025-10-07/Misc/
mv delta-feedback*.json ~/Archives/Pre-Recovery-2025-10-07/Misc/
mv Damian ~/Archives/Pre-Recovery-2025-10-07/Misc/  # Review this first
```

### Step 8: Verification
```bash
# Confirm only active projects remain
ls -la ~/Downloads/WIMD-Railway-Deploy-Project
ls -la ~/Downloads/Foundation_Vault

# Confirm archives exist
ls -la ~/Archives/Pre-Recovery-2025-10-07/

# Check space reclaimed
du -sh ~/Downloads
```

---

## QUESTIONS FOR USER

1. **Foundation_Vault** (1.6MB) - Is this still actively used? Keep or archive?
2. **"Damian" file** (212KB) - What is this? Safe to archive?
3. **no_more_copy_paste_toolkit** - Still needed or archive?
4. **Additional folders to keep?** - Any other folders I missed that should stay?

---

## RISKS & MITIGATIONS

**Risk**: Accidentally archive needed files
**Mitigation**: Using `mv` (move) not `rm` (delete) - all files recoverable from Archives

**Risk**: Breaking active project dependencies
**Mitigation**: Only touching clearly obsolete/duplicate folders; active projects untouched

**Risk**: User needs archived file later
**Mitigation**: Archives organized by category with clear naming; easy to find and restore

---

## APPROVAL CHECKLIST

- [ ] User confirms Foundation_Vault status (keep/archive)
- [ ] User identifies what "Damian" file is
- [ ] User confirms no_more_copy_paste_toolkit needed or not
- [ ] User approves archive structure
- [ ] User approves deletion of duplicate zips
- [ ] User authorizes execution of cleanup

**No file operations will occur until all checkboxes are marked.**

---

**Document Status**: DRAFT - AWAITING USER APPROVAL
**Prepared By**: Claude Code
**Next Step**: User review and approval, then execute cleanup
