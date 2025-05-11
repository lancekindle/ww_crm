#!/usr/bin/env python3
"""
Tool to detect explicit waits in UI test files.

This script checks for unnecessary explicit wait calls in UI test files
to prevent reintroduction of timeouts that can make tests flaky and slow.

Usage:
    python -m ww_crm.tools.check_explicit_waits [path]

If no path is provided, it will check all UI test files in the project.

Exit codes:
    0: No explicit waits found
    1: Explicit waits found
"""
import os
import re
import sys
import argparse
from typing import List, Dict, Tuple


# Patterns to detect explicit waits
WAIT_PATTERNS = [
    (r"\.wait_for_selector\(", "Explicit wait_for_selector call"),
    (r"\.wait_for_timeout\(", "Arbitrary timeout"),
    (r"\.wait_for_url\(", "Explicit URL wait"),
    (r"\.wait_for_load_state\(", "Explicit load state wait"),
    (r"expect_navigation\(.*wait_until\s*=", "Custom navigation wait_until"),
    (r"page\.wait_for\(", "Generic wait_for call"),
]

# Patterns for allowed exceptions
ALLOWED_PATTERNS = [
    # Example of an allowed exception:
    r"# ALLOW_WAIT: .*",
]

# Directories to scan
TEST_DIRS = [
    "ww_crm/tests/e2e",
]

# File extensions to check
FILE_EXTENSIONS = [".py"]


def find_test_files(base_dir: str = None) -> List[str]:
    """Find all test files to check.

    Args:
        base_dir: Optional base directory to search

    Returns:
        List of file paths to check
    """
    if base_dir and os.path.isfile(base_dir):
        return [base_dir]

    files_to_check = []

    # Determine which directories to scan
    dirs_to_scan = [base_dir] if base_dir else TEST_DIRS

    for directory in dirs_to_scan:
        if not os.path.exists(directory):
            continue

        for root, _, files in os.walk(directory):
            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in FILE_EXTENSIONS:
                    files_to_check.append(os.path.join(root, file))

    return files_to_check


def check_file(file_path: str) -> Dict[int, List[Tuple[str, str]]]:
    """Check a file for explicit waits.

    Args:
        file_path: Path to the file to check

    Returns:
        Dictionary mapping line numbers to list of (matched text, description)
    """
    results = {}

    with open(file_path, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines, 1):
        # Check if line is allowed to have waits (has an exception comment)
        if any(re.search(pattern, line) for pattern in ALLOWED_PATTERNS):
            continue

        # Check each wait pattern
        for pattern, description in WAIT_PATTERNS:
            if re.search(pattern, line):
                if i not in results:
                    results[i] = []
                results[i].append((line.strip(), description))

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check for explicit waits in UI test files")
    parser.add_argument("path", nargs="?", help="Path to file or directory to check")
    args = parser.parse_args()

    files_to_check = find_test_files(args.path)
    if not files_to_check:
        print("No test files found to check")
        return 0

    found_waits = False

    for file_path in files_to_check:
        results = check_file(file_path)

        if results:
            found_waits = True
            print(f"\n⚠️  Explicit waits found in {file_path}:")

            for line_num, matches in sorted(results.items()):
                for match_text, description in matches:
                    print(f"    Line {line_num}: {description}")
                    print(f"        {match_text}")
                    print()

    if found_waits:
        print("\n❌ Some files contain explicit waits that may not be necessary.")
        print("    Playwright has built-in auto-waiting, so explicit waits should be avoided.")
        print("    If a wait is truly necessary, add a '# ALLOW_WAIT: <reason>' comment.")
        return 1
    else:
        print("\n✅ No explicit waits found! Your tests are using Playwright's auto-waiting correctly.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
