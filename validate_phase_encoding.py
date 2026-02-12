#!/usr/bin/env python3
"""
validate_phase_encoding.py
Author: [Your Name]

Sanity-check and optionally fix the 'PhaseEncodingDirection' field
in BIDS DWI JSON sidecars.

Usage:
    python validate_phase_encoding.py /path/to/bids_root [--fix]

Checks every JSON under sub-*/dwi/ or sub-*/ses-*/dwi/ for the following:
  - 'PhaseEncodingDirection' exists
  - Value is one of: 'i', 'i-', 'j', 'j-', 'k', 'k-'

If --fix is passed, it will infer from 'dir' key or folder name
(e.g., PA → 'j-', AP → 'j') and patch the JSON in place.
"""

import json
import sys
import argparse
from pathlib import Path

VALID_DIRECTIONS = {"i", "i-", "j", "j-", "k", "k-"}


def infer_direction_from_dir(meta, path):
    """Guess PhaseEncodingDirection from 'dir' key or filename context."""
    name = (meta.get("dir") or path.name).upper()
    if "PA" in name:
        return "j-"
    if "AP" in name:
        return "j"
    if "RL" in name:
        return "i"
    if "LR" in name:
        return "i-"
    if "SI" in name:
        return "k"
    if "IS" in name:
        return "k-"
    return None


def validate_json(json_path, fix=False):
    """Check a single JSON file and optionally fix it."""
    try:
        text = json_path.read_text()
        meta = json.loads(text)
    except Exception as e:
        print(f"✗ {json_path}: Invalid JSON ({e})")
        return False

    ped = meta.get("PhaseEncodingDirection")

    if ped in VALID_DIRECTIONS:
        print(f"✓ {json_path}: PhaseEncodingDirection = {ped}")
        return True

    # Invalid or missing
    print(f"  {json_path}: invalid or missing PhaseEncodingDirection ({ped})")
    if fix:
        guess = infer_direction_from_dir(meta, json_path)
        if guess:
            meta["PhaseEncodingDirection"] = guess
            json_path.write_text(json.dumps(meta, indent=2))
            print(f"  → Fixed: set PhaseEncodingDirection = '{guess}'")
            return True
        else:
            print("  → Could not infer direction.")
    return False


def main():
    parser = argparse.ArgumentParser(description="Validate and fix PhaseEncodingDirection in DWI JSONs.")
    parser.add_argument("bids_root", help="Path to BIDS dataset root")
    parser.add_argument("--fix", action="store_true", help="Auto-fix missing fields when possible")
    args = parser.parse_args()

    bids_root = Path(args.bids_root)

    #  Recursive search for both sessioned and non-sessioned layouts
    json_files = list(bids_root.rglob("sub-*/**/dwi/*.json"))
    if not json_files:
        print(f"No DWI JSONs found under {bids_root} (searched recursively).")
        sys.exit(1)

    print(f"Checking {len(json_files)} DWI JSON files under {bids_root}")
    n_valid = 0

    for js in json_files:
        if validate_json(js, fix=args.fix):
            n_valid += 1

    print(f"\nSummary: {n_valid}/{len(json_files)} valid PhaseEncodingDirection fields.")
    if args.fix:
        print("All missing or invalid fields were updated when possible.")


if __name__ == "__main__":
    main()
