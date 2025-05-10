#!/usr/bin/env python3
"""
Test runner script for the Window Wash CRM.
"""
import sys
import os
import pytest


def run_tests():
    """Run the test suite with specified configurations."""
    # Add the project root directory to the Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    # Default pytest arguments
    args = [
        '-xvs',  # x: stop on first failure, v: verbose, s: show print statements
        '--tb=native',  # Use Python's traceback format
    ]

    # Add specific test categories if provided as command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'models':
            args.append('tests/test_models.py')
        elif sys.argv[1] == 'routes':
            args.append('tests/test_routes.py')
        elif sys.argv[1] == 'ui':
            args.append('tests/test_ui.py')
        elif sys.argv[1] == 'utils':
            args.append('tests/test_utils.py')
        else:
            args.append(sys.argv[1])  # Allow specifying a test file or pattern

    # Run tests with configured arguments
    return pytest.main(args)


if __name__ == '__main__':
    sys.exit(run_tests())
