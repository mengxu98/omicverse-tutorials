#!/usr/bin/env python3
"""
Check synchronization status between English and Chinese documentation.

Compares current file hashes with the manifest to detect:
1. Modified English files needing translation update
2. New English files needing Chinese translation
3. Removed English files (optional cleanup)

Usage:
    python3 check_sync_status.py                    # Show all status
    python3 check_sync_status.py --modified         # Show only modified
    python3 check_sync_status.py --new              # Show only new files
    python3 check_sync_status.py --priority         # Priority: new > modified
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import sys
import argparse


def calculate_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return ""


def load_manifest(manifest_path: Path) -> Dict:
    """Load the hash manifest."""
    try:
        with open(manifest_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading manifest: {e}")
        return {}


def is_important_file(path: str) -> bool:
    """Check if file is important for translation (exclude auto-generated)."""
    # Exclude auto-generated and build files
    excluded_dirs = {"_build", ".ipynb_checkpoints", "api/reference"}
    path_parts = Path(path).parts
    return not any(part in excluded_dirs for part in path_parts)


def check_sync_status(
    manifest_path: Path, docs_dir: Path, important_only: bool = False
) -> Dict[str, List[str]]:
    """
    Check which files need translation updates.

    Args:
        important_only: If True, exclude auto-generated files like _build/

    Returns:
        {
            "modified": ["path1", "path2"],    # English changed, Chinese outdated
            "new": ["path1"],                   # No Chinese version exists
            "removed": ["path1"],               # English file was deleted
            "updated_chinese": ["path1"]        # Chinese updated matching English
        }
    """
    manifest = load_manifest(manifest_path)
    status = {
        "modified": [],
        "new": [],
        "removed": [],
        "updated_chinese": [],
    }

    if not manifest or "files" not in manifest:
        return status

    for rel_path, file_info in manifest["files"].items():
        # Skip auto-generated files if important_only is True
        if important_only and not is_important_file(rel_path):
            continue

        file_path = docs_dir / rel_path

        # Check if file still exists
        if not file_path.exists():
            status["removed"].append(rel_path)
            continue

        # Calculate current hash
        current_hash = calculate_hash(file_path)
        stored_hash = file_info.get("english_hash")

        # Check if English file was modified
        if current_hash != stored_hash:
            status["modified"].append(rel_path)
        elif file_info["status"] == "missing_chinese":
            status["new"].append(rel_path)
        else:
            status["updated_chinese"].append(rel_path)

    return status


def print_status_report(status: Dict[str, List[str]], docs_dir: Path):
    """Print a formatted status report."""

    print("\n" + "=" * 70)
    print("DOCUMENTATION SYNCHRONIZATION STATUS")
    print("=" * 70)

    # Modified files
    if status["modified"]:
        print(f"\n📝 MODIFIED English files ({len(status['modified'])}):")
        print("   (Chinese versions are now outdated)")
        for path in sorted(status["modified"])[:20]:
            print(f"   • {path}")
        if len(status["modified"]) > 20:
            print(f"   ... and {len(status['modified']) - 20} more")

    # New files
    if status["new"]:
        print(f"\n✨ NEW English files ({len(status['new'])}):")
        print("   (No Chinese translation yet)")
        for path in sorted(status["new"])[:20]:
            print(f"   + {path}")
        if len(status["new"]) > 20:
            print(f"   ... and {len(status['new']) - 20} more")

    # Removed files
    if status["removed"]:
        print(f"\n🗑️  REMOVED English files ({len(status['removed'])}):")
        print("   (Consider removing Chinese versions)")
        for path in sorted(status["removed"])[:10]:
            print(f"   - {path}")
        if len(status["removed"]) > 10:
            print(f"   ... and {len(status['removed']) - 10} more")

    # Synced files (if requested)
    if status["updated_chinese"]:
        synced_count = len(status["updated_chinese"])
        print(f"\n✅ SYNCED files in Chinese ({synced_count})")

    # Summary
    total_to_translate = len(status["modified"]) + len(status["new"])
    print(f"\n{'-' * 70}")
    print(f"PRIORITY: {total_to_translate} files need translation work")
    if status["modified"]:
        print(f"  - {len(status['modified'])} modified files need update")
    if status["new"]:
        print(f"  - {len(status['new'])} new files need translation")
    print("=" * 70 + "\n")


def print_priority_list(status: Dict[str, List[str]]):
    """Print files in priority order (new first, then modified)."""

    print("\n" + "=" * 70)
    print("TRANSLATION PRIORITY LIST")
    print("=" * 70)

    # New files first (highest priority)
    if status["new"]:
        print(f"\n🔴 PRIORITY 1: New files ({len(status['new'])})")
        for path in sorted(status["new"]):
            print(f"   {path}")

    # Then modified files
    if status["modified"]:
        print(f"\n🟡 PRIORITY 2: Modified files ({len(status['modified'])})")
        for path in sorted(status["modified"]):
            print(f"   {path}")

    print(f"\n{'-' * 70}")
    print(f"Total: {len(status['new']) + len(status['modified'])} files")
    print("=" * 70 + "\n")


def export_to_file(status: Dict[str, List[str]], output_path: Path):
    """Export sync status to a file for tracking."""

    with open(output_path, "w") as f:
        f.write("# Documentation Synchronization Status\n\n")

        if status["new"]:
            f.write(f"## New Files ({len(status['new'])})\n\n")
            for path in sorted(status["new"]):
                f.write(f"- [ ] `{path}`\n")
            f.write("\n")

        if status["modified"]:
            f.write(f"## Modified Files ({len(status['modified'])})\n\n")
            for path in sorted(status["modified"]):
                f.write(f"- [ ] `{path}`\n")
            f.write("\n")

        if status["removed"]:
            f.write(f"## Removed Files ({len(status['removed'])})\n\n")
            for path in sorted(status["removed"]):
                f.write(f"- [ ] `{path}`\n")
            f.write("\n")

    print(f"✓ Status exported to: {output_path}")


def main():
    """Main function."""

    parser = argparse.ArgumentParser(
        description="Check documentation synchronization status"
    )
    parser.add_argument(
        "--modified", action="store_true", help="Show only modified files"
    )
    parser.add_argument(
        "--new", action="store_true", help="Show only new files"
    )
    parser.add_argument(
        "--removed", action="store_true", help="Show only removed files"
    )
    parser.add_argument(
        "--priority", action="store_true", help="Show priority list (new > modified)"
    )
    parser.add_argument(
        "--export",
        type=str,
        help="Export status to markdown file",
    )

    args = parser.parse_args()

    repo_root = Path(__file__).parent
    manifest_path = repo_root / "docs_sync_manifest.json"
    docs_dir = repo_root / "docs"

    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}")
        print("Run: python3 generate_hash_manifest.py")
        return 1

    # Check status (exclude auto-generated files by default)
    status = check_sync_status(manifest_path, docs_dir, important_only=True)

    # Filter based on arguments
    if args.modified:
        print("\nModified files:")
        for path in sorted(status["modified"]):
            print(f"  {path}")
    elif args.new:
        print("\nNew files:")
        for path in sorted(status["new"]):
            print(f"  {path}")
    elif args.removed:
        print("\nRemoved files:")
        for path in sorted(status["removed"]):
            print(f"  {path}")
    elif args.priority:
        print_priority_list(status)
    else:
        print_status_report(status, docs_dir)

    # Export if requested
    if args.export:
        export_to_file(status, Path(args.export))

    return 0


if __name__ == "__main__":
    exit(main())
