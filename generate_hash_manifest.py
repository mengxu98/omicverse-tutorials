#!/usr/bin/env python3
"""
Hash tracking system for omicverse-tutorials documentation synchronization.

This script generates a manifest file that tracks English and Chinese file
correspondence via SHA256 hashes. Used to detect which Chinese files need
updating when English files are modified or new notebooks are added.

Usage:
    python generate_hash_manifest.py

Output:
    - docs_sync_manifest.json: Maps English files → Chinese files with hashes
    - Summary: Files added, removed, modified
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


def calculate_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error hashing {file_path}: {e}")
        return ""


def get_relative_path(file_path: Path, base_dir: Path) -> str:
    """Get relative path from base directory."""
    return str(file_path.relative_to(base_dir))


def map_files(docs_dir: Path, docs_zh_dir: Path) -> Dict[str, Dict]:
    """
    Map English files to Chinese files with hashes.

    Returns dict: {
        "files": {
            "english_relative_path": {
                "english_hash": "...",
                "chinese_path": "chinese_relative_path",
                "chinese_hash": "...",
                "status": "ok|missing_chinese|new|modified"
            }
        },
        "stats": {
            "total_english_files": N,
            "total_chinese_files": N,
            "mapped": N,
            "missing_chinese": N,
            "new_english": N
        },
        "generated_at": "ISO timestamp"
    }
    """

    manifest = {
        "files": {},
        "stats": {
            "total_english_files": 0,
            "total_chinese_files": 0,
            "mapped": 0,
            "missing_chinese": 0,
            "new_english": 0,
        },
        "generated_at": datetime.now().isoformat(),
    }

    # File extensions to track
    tracked_extensions = {".md", ".ipynb"}

    # Directories to exclude from tracking
    excluded_dirs = {"_build", ".ipynb_checkpoints", "api"}

    def should_track(f: Path, base_dir: Path) -> bool:
        rel = f.relative_to(base_dir)
        return not any(part in excluded_dirs for part in rel.parts)

    # Get all English files
    english_files = [
        f for f in docs_dir.rglob("*")
        if f.is_file() and f.suffix in tracked_extensions and should_track(f, docs_dir)
    ]

    # Get all Chinese files
    chinese_files_set = {
        get_relative_path(f, docs_zh_dir)
        for f in docs_zh_dir.rglob("*")
        if f.is_file() and f.suffix in tracked_extensions and should_track(f, docs_zh_dir)
    }

    manifest["stats"]["total_english_files"] = len(english_files)
    manifest["stats"]["total_chinese_files"] = len(chinese_files_set)

    # Map each English file
    for eng_file in sorted(english_files):
        eng_rel_path = get_relative_path(eng_file, docs_dir)
        eng_hash = calculate_hash(eng_file)

        # Look for corresponding Chinese file
        chin_rel_path = eng_rel_path
        chin_file = docs_zh_dir / chin_rel_path

        if chin_file.exists():
            chin_hash = calculate_hash(chin_file)
            status = "ok"
            manifest["stats"]["mapped"] += 1
        else:
            chin_hash = None
            status = "missing_chinese"
            manifest["stats"]["missing_chinese"] += 1

        manifest["files"][eng_rel_path] = {
            "english_hash": eng_hash,
            "chinese_path": chin_rel_path,
            "chinese_hash": chin_hash,
            "status": status,
        }

    # Check for new English files (added since translation)
    # Files that don't have a Chinese counterpart are flagged
    manifest["stats"]["new_english"] = manifest["stats"]["missing_chinese"]

    return manifest


def compare_with_previous(
    current_manifest: Dict, previous_manifest: Dict
) -> Dict[str, List[str]]:
    """
    Compare current manifest with previous version to detect changes.

    Returns:
        {
            "modified": ["path1", "path2"],
            "removed": ["path1"],
            "new": ["path1"]
        }
    """
    changes = {
        "modified": [],
        "removed": [],
        "new": [],
    }

    if not previous_manifest or "files" not in previous_manifest:
        return changes

    current_files = current_manifest["files"]
    previous_files = previous_manifest["files"]

    # Find modified and removed files
    for path, prev_data in previous_files.items():
        if path not in current_files:
            changes["removed"].append(path)
        elif prev_data["english_hash"] != current_files[path]["english_hash"]:
            changes["modified"].append(path)

    # Find new files
    for path in current_files:
        if path not in previous_files:
            changes["new"].append(path)

    return changes


def load_previous_manifest(manifest_path: Path) -> Dict:
    """Load previous manifest if it exists."""
    try:
        if manifest_path.exists():
            with open(manifest_path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load previous manifest: {e}")
    return {}


def main():
    """Generate and save hash manifest."""

    # Paths
    repo_root = Path(__file__).parent
    docs_dir = repo_root / "docs"
    docs_zh_dir = repo_root / "docs_zh"
    manifest_path = repo_root / "docs_sync_manifest.json"

    # Validate directories exist
    if not docs_dir.exists():
        print(f"Error: {docs_dir} not found")
        return 1

    if not docs_zh_dir.exists():
        print(f"Error: {docs_zh_dir} not found")
        return 1

    print("Generating hash manifest...")
    print(f"  English docs: {docs_dir}")
    print(f"  Chinese docs: {docs_zh_dir}")

    # Generate manifest
    current_manifest = map_files(docs_dir, docs_zh_dir)

    # Load previous manifest for comparison
    previous_manifest = load_previous_manifest(manifest_path)

    # Detect changes
    changes = compare_with_previous(current_manifest, previous_manifest)

    # Save manifest
    with open(manifest_path, "w") as f:
        json.dump(current_manifest, f, indent=2)

    print(f"\n✓ Manifest saved to: {manifest_path}")

    # Print summary
    stats = current_manifest["stats"]
    print(f"\nSummary:")
    print(f"  Total English files:    {stats['total_english_files']}")
    print(f"  Total Chinese files:    {stats['total_chinese_files']}")
    print(f"  Mapped (with Chinese):  {stats['mapped']}")
    print(f"  Missing Chinese:        {stats['missing_chinese']}")

    if changes["modified"]:
        print(f"\nModified English files ({len(changes['modified'])}):")
        for path in changes["modified"][:10]:
            print(f"  - {path}")
        if len(changes["modified"]) > 10:
            print(f"  ... and {len(changes['modified']) - 10} more")

    if changes["new"]:
        print(f"\nNew English files ({len(changes['new'])}):")
        for path in changes["new"][:10]:
            print(f"  + {path}")
        if len(changes["new"]) > 10:
            print(f"  ... and {len(changes['new']) - 10} more")

    if changes["removed"]:
        print(f"\nRemoved English files ({len(changes['removed'])}):")
        for path in changes["removed"][:10]:
            print(f"  - {path}")

    print("\nHow to use this manifest:")
    print("  1. When English files are modified, their hash will change")
    print("  2. Compare hashes to detect modified files needing translation update")
    print("  3. New files will have status 'missing_chinese'")
    print("  4. Run this script periodically to update the manifest")

    return 0


if __name__ == "__main__":
    exit(main())
