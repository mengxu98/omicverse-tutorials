# Documentation Translation Synchronization System

This document describes the hash-tracking system for maintaining English-Chinese documentation synchronization in the omicverse-tutorials repository.

## Overview

The synchronization system tracks which English files have been translated to Chinese by storing SHA256 hashes of each file. This allows automated detection of:

1. **Modified English files** - When English docs change, we know which Chinese versions are now outdated
2. **New English files** - When new notebooks or guides are added, we know what needs translation
3. **Translation status** - Quick overview of which files are synced vs. need work

## Files in the System

### 1. `generate_hash_manifest.py`
**Purpose:** Generate and maintain the hash manifest file

**Usage:**
```bash
python3 generate_hash_manifest.py
```

**What it does:**
- Scans all tracked files in `docs/` and `docs_zh/`
- Calculates SHA256 hashes for each file
- Creates/updates `docs_sync_manifest.json` with file mappings
- Reports summary statistics
- Compares with previous manifest to detect changes

**Output:**
```
Generated hash manifest for 413 English files
- 179 files have Chinese translations
- 234 files need Chinese translation or are auto-generated
```

### 2. `check_sync_status.py`
**Purpose:** Check which files need translation work

**Basic Usage:**
```bash
# Show full status report
python3 check_sync_status.py

# Show only new files
python3 check_sync_status.py --new

# Show only modified files
python3 check_sync_status.py --modified

# Show priority list (new > modified)
python3 check_sync_status.py --priority

# Export status to markdown file
python3 check_sync_status.py --export sync_status.md
```

**Output Example:**
```
DOCUMENTATION SYNCHRONIZATION STATUS

✨ NEW English files (135):
   (No Chinese translation yet)
   + Example_dataset.md
   + Installation_guide_zh.md
   + api/reference/omicverse.bulk.Deconvolution.rst
   ...

📝 MODIFIED English files (0):
   (Chinese versions are now outdated)

✅ SYNCED files in Chinese (167)

PRIORITY: 135 files need translation work
```

### 3. `docs_sync_manifest.json`
**Purpose:** Central manifest file tracking all file hashes

**Structure:**
```json
{
  "files": {
    "Installation_guild.md": {
      "english_hash": "912327aa24faffe0b140bcf21a3865a7940abde...",
      "chinese_path": "Installation_guild.md",
      "chinese_hash": "5c3cead5306a10913f2f980914bd42aacae49...",
      "status": "ok"
    },
    "Example_dataset.md": {
      "english_hash": "fe2ff5a450a75dd740e6cd6420ffa3eef412e4...",
      "chinese_path": "Example_dataset.md",
      "chinese_hash": null,
      "status": "missing_chinese"
    }
  },
  "stats": {
    "total_english_files": 413,
    "total_chinese_files": 182,
    "mapped": 179,
    "missing_chinese": 234,
    "generated_at": "2026-04-03T10:30:00.000000"
  }
}
```

**File Status Values:**
- `"ok"` - File has Chinese translation with matching structure
- `"missing_chinese"` - File has no Chinese translation yet
- `"new"` - New English file added since last manifest generation

## Workflow for Translation Maintenance

### Step 1: Generate Initial Manifest
After translating a batch of files or at major milestones:

```bash
python3 generate_hash_manifest.py
git add docs_sync_manifest.json
git commit -m "Update translation manifest after Chinese docs completion"
```

### Step 2: Modify English Documentation
When updating English files:

1. Modify the English files in `docs/`
2. Run status check to see what changed:
   ```bash
   python3 check_sync_status.py --modified
   ```
3. This shows which Chinese files are now outdated and need updating

### Step 3: Add New English Files
When adding new tutorials or guides:

1. Add files to `docs/`
2. Check what needs translation:
   ```bash
   python3 check_sync_status.py --new
   ```
3. Add corresponding Chinese translations to `docs_zh/`
4. Update the manifest once translations are complete

### Step 4: Update Manifest After Changes
After translating modified or new files:

```bash
python3 generate_hash_manifest.py
```

This updates all hashes and should show:
- Modified files now synced
- New files now have Chinese translations

## File Types Tracked

The system tracks these file extensions:
- `.md` - Markdown documentation pages
- `.ipynb` - Jupyter notebooks
- `.py` - Python scripts
- `.rst` - reStructuredText API reference files

Auto-generated files are excluded from default checks:
- `_build/` - Build artifacts
- `.ipynb_checkpoints/` - Jupyter checkpoint files
- `api/reference/` - Auto-generated API docs

## Important Notes

### Why Use Hashes?

Hashes provide:
1. **Accuracy** - Detect even small text changes
2. **Automation** - Programmatically find outdated translations
3. **History** - Track sync status over time
4. **Simplicity** - No manual tracking needed

### When to Regenerate Manifest

Regenerate (`generate_hash_manifest.py`) after:
- Completing a batch of Chinese translations
- Making significant English documentation updates
- Adding new tutorial notebooks
- Monthly maintenance (recommended)

### Auto-Generated Files

The following are NOT tracked for translation:
- **`_build/`** - HTML output (regenerated from source)
- **`.ipynb_checkpoints/`** - Jupyter cache
- **`api/reference/`** - Auto-generated from docstrings (lower priority)

These can be safely ignored in translation work.

### Notebook Markdown Translation

For Jupyter notebooks (`.ipynb`):
- Only **markdown cells** are translated
- **Code cells** remain unchanged
- Cell structure and metadata are preserved
- Outputs are auto-generated when built

## Current Status

As of manifest generation:

- **Total files tracked:** 413
- **Files with Chinese:** 179 (key notebooks + main guides)
- **Needing translation:** 234 (mostly auto-gen + index pages)
- **Modified files:** 0 (fully synced)

**Priority areas for future translation:**
1. Tutorial index files (10 files)
2. Example dataset guide (1 file)
3. API reference auto-generated docs (128 files) - lower priority
4. New notebooks added in future

## Automation Possibilities

The system enables several automation scenarios:

### Option 1: CI/CD Check
```bash
# In GitHub Actions workflow
python3 check_sync_status.py --modified
if [ $? -ne 0 ]; then exit 1; fi
```

### Option 2: Translation Tracking
```bash
# Generate monthly status report
python3 check_sync_status.py --priority --export sync_status_$(date +%Y%m%d).md
```

### Option 3: Webhook Notification
- When English files change, automatically flag corresponding Chinese files
- Create issues for translation updates
- Assign to translation team

## Troubleshooting

### Manifest shows different file count than expected

**Issue:** After adding new files, manifest shows unexpected counts

**Solution:**
```bash
# Regenerate manifest to refresh all hashes
python3 generate_hash_manifest.py
```

### Hash changed unexpectedly

**Issue:** File hash changed even though content looks the same

**Cause:** Likely whitespace, encoding, or line ending differences
- Check file encoding (should be UTF-8)
- Verify line endings (LF, not CRLF)

**Solution:**
```bash
# Check the actual hash of your file
sha256sum docs/path/to/file.md
```

### Chinese file marked as missing but file exists

**Issue:** Status shows "missing_chinese" for a file that exists in `docs_zh/`

**Cause:** File was added after last manifest generation

**Solution:**
```bash
python3 generate_hash_manifest.py
```

## See Also

- `/Users/fernandozeng/Desktop/analysis/omicverse-project/omicverse-tutorials/docs/` - English documentation source
- `/Users/fernandozeng/Desktop/analysis/omicverse-project/omicverse-tutorials/docs_zh/` - Chinese documentation source
- `Makefile` - Build commands for both English and Chinese documentation
