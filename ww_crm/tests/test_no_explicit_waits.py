"""
Tests to ensure we don't have unnecessary explicit waits in our test code.

Playwright provides excellent built-in auto-waiting for most interactions:
- Elements are automatically waited for before interacting
- Clicks, navigation, and form submissions have intelligent waiting behavior
- Page state changes are properly awaited without explicit timeouts

By relying on Playwright's built-in mechanisms instead of explicit waits, our tests benefit from:
1. Increased reliability - tests adapt to varying application response times
2. Improved maintainability - less code to maintain with fewer magic numbers
3. Better performance - no arbitrary waiting that slows down tests
4. More readable code - focus on intentions rather than implementation details

This test ensures we maintain these benefits by checking for explicit wait patterns.
"""

import os
import re
import pytest
from glob import glob

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


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


def get_e2e_test_files():
    """Get all E2E test files.

    Returns:
        List of all E2E test files
    """
    # Get the project root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Find all Python files in the e2e directory
    pattern = os.path.join(root_dir, "ww_crm", "tests", "e2e", "**", "*.py")
    return glob(pattern, recursive=True)


def test_no_explicit_waits_in_e2e_tests():
    """Test that we don't have explicit waits in our E2E tests."""
    test_files = get_e2e_test_files()
    assert test_files, "No E2E test files found"

    errors = []

    for file_path in test_files:
        with open(file_path, "r") as f:
            file_content = f.read()

        # Get relative path for more readable output
        rel_path = os.path.relpath(file_path)

        # Check for explicit waits
        for pattern, description in WAIT_PATTERNS:
            # Find all matches
            matches = re.finditer(pattern, file_content)

            for match in matches:
                # Check if this is an allowed exception
                line_start = file_content.rfind("\n", 0, match.start()) + 1
                line_end = file_content.find("\n", match.start())
                line = file_content[line_start:line_end]

                # Skip if the line has an allowed exception
                if any(re.search(allowed, line) for allowed in ALLOWED_PATTERNS):
                    continue

                # Get line number (count newlines before match)
                line_number = file_content.count("\n", 0, match.start()) + 1

                # Add error
                errors.append(f"{rel_path}:{line_number} - {description}: {line.strip()}")

    # If there are errors, display them and fail the test
    if errors:
        error_message = "\nExplicit waits found:\n" + "\n".join(f"  {error}" for error in errors)
        error_message += "\n\nPlaywright has built-in auto-waiting, so explicit waits should be avoided."
        error_message += "\nIf a wait is truly necessary, add a '# ALLOW_WAIT: <reason>' comment."
        pytest.fail(error_message)
