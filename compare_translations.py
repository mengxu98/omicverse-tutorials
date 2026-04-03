#!/usr/bin/env python3
"""
Compare translation hashes between English and Chinese versions of a specific file.

Usage:
    python3 compare_translations.py docs/Installation_guild.md
    python3 compare_translations.py --file docs/Installation_guild.md
    python3 compare_translations.py --check-all  # Verify all hashes
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Tuple
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
        print(f"Error: Could not read {file_path}: {e}")
        return ""


def load_manifest(manifest_path: Path) -> dict:
    """Load the hash manifest."""
    try:
        with open(manifest_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading manifest: {e}")
        return {}


def compare_file(
    repo_root: Path, manifest: dict, rel_path: str
) -> Tuple[bool, str]:
    """
    Compare English and Chinese versions of a file.

    Returns:
        (is_synced, message)
    """

    if rel_path not in manifest.get("files", {}):
        return False, f"❓ File '{rel_path}' not in manifest"

    file_info = manifest["files"][rel_path]
    eng_file = repo_root / "docs" / rel_path
    chin_file = repo_root / "docs_zh" / rel_path

    # Check English file
    if not eng_file.exists():
        return False, f"❌ English file not found: {rel_path}"

    eng_hash = calculate_hash(eng_file)
    stored_eng_hash = file_info.get("english_hash")

    if eng_hash != stored_eng_hash:
        return False, f"⚠️  English file was modified (hash mismatch)"

    # Check Chinese file
    if not chin_file.exists():
        return (
            False,
            f"❌ Chinese file not found: {file_info.get('chinese_path')}",
        )

    chin_hash = calculate_hash(chin_file)
    stored_chin_hash = file_info.get("chinese_hash")

    if chin_hash != stored_chin_hash:
        return False, f"⚠️  Chinese file was modified (hash mismatch)"

    # All synced
    return True, "✅ Synced: Both English and Chinese are up to date"


def verify_all_hashes(repo_root: Path, manifest: dict) -> dict:
    """Verify all file hashes in manifest match actual files."""

    results = {
        "total": 0,
        "valid": 0,
        "invalid_english": [],
        "invalid_chinese": [],
        "missing_english": [],
        "missing_chinese": [],
    }

    tracked_extensions = {".md", ".ipynb", ".py", ".rst"}

    for rel_path, file_info in manifest.get("files", {}).items():
        # Skip untracked file types and auto-generated files
        if Path(rel_path).suffix not in tracked_extensions:
            continue
        if "_build" in rel_path or ".ipynb_checkpoints" in rel_path:
            continue

        results["total"] += 1

        eng_file = repo_root / "docs" / rel_path
        chin_file = repo_root / "docs_zh" / rel_path

        # Check English file
        if not eng_file.exists():
            results["missing_english"].append(rel_path)
            continue

        eng_hash = calculate_hash(eng_file)
        if eng_hash != file_info.get("english_hash"):
            results["invalid_english"].append(rel_path)
            continue

        # Check Chinese file if it should exist
        if file_info.get("status") == "ok":
            if not chin_file.exists():
                results["missing_chinese"].append(rel_path)
                continue

            chin_hash = calculate_hash(chin_file)
            if chin_hash != file_info.get("chinese_hash"):
                results["invalid_chinese"].append(rel_path)
                continue

        results["valid"] += 1

    return results


def print_verification_report(results: dict):
    """Print verification results."""

    print("\n" + "=" * 70)
    print("HASH VERIFICATION REPORT")
    print("=" * 70)

    print(f"\nFiles verified: {results['valid']}/{results['total']}")

    if results["invalid_english"]:
        print(f"\n❌ INVALID English hashes ({len(results['invalid_english'])}):")
        print("   Files have been modified since last manifest generation")
        for path in sorted(results["invalid_english"])[:10]:
            print(f"   • {path}")
        if len(results["invalid_english"]) > 10:
            print(f"   ... and {len(results['invalid_english']) - 10} more")

    if results["invalid_chinese"]:
        print(f"\n❌ INVALID Chinese hashes ({len(results['invalid_chinese'])}):")
        print("   Files have been modified since last manifest generation")
        for path in sorted(results["invalid_chinese"])[:10]:
            print(f"   • {path}")
        if len(results["invalid_chinese"]) > 10:
            print(f"   ... and {len(results['invalid_chinese']) - 10} more")

    if results["missing_english"]:
        print(f"\n❌ MISSING English files ({len(results['missing_english'])}):")
        for path in sorted(results["missing_english"])[:10]:
            print(f"   - {path}")

    if results["missing_chinese"]:
        print(f"\n❌ MISSING Chinese files ({len(results['missing_chinese'])}):")
        for path in sorted(results["missing_chinese"])[:10]:
            print(f"   - {path}")

    if (
        not results["invalid_english"]
        and not results["invalid_chinese"]
        and not results["missing_english"]
        and not results["missing_chinese"]
    ):
        print("\n✅ All verified files are in sync!")

    print("=" * 70 + "\n")


def main():
    """Main function."""

    parser = argparse.ArgumentParser(description="Compare translation synchronization")
    parser.add_argument(
        "file", nargs="?", help="Relative path to file in docs/ to check"
    )
    parser.add_argument(
        "--file", dest="file_arg", help="Alternative way to specify file path"
    )
    parser.add_argument(
        "--check-all",
        action="store_true",
        help="Verify all manifest hashes",
    )

    args = parser.parse_args()

    repo_root = Path(__file__).parent
    manifest_path = repo_root / "docs_sync_manifest.json"

    if not manifest_path.exists():
        print(f"Error: Manifest not found at {manifest_path}")
        print("Run: python3 generate_hash_manifest.py")
        return 1

    manifest = load_manifest(manifest_path)

    # Check all hashes
    if args.check_all:
        results = verify_all_hashes(repo_root, manifest)
        print_verification_report(results)
        return 0

    # Compare specific file
    file_path = args.file or args.file_arg
    if not file_path:
        print("Usage:")
        print("  python3 compare_translations.py docs/Installation_guild.md")
        print("  python3 compare_translations.py --check-all")
        return 1

    # Remove leading docs/ if present
    if file_path.startswith("docs/"):
        file_path = file_path[5:]
    elif file_path.startswith("./docs/"):
        file_path = file_path[7:]

    is_synced, message = compare_file(repo_root, manifest, file_path)

    print(f"\n{message}\n")

    if not is_synced:
        if "modified" in message.lower():
            print("To sync, translate or update the Chinese version and then run:")
            print("  python3 generate_hash_manifest.py")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
