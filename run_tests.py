#!/usr/bin/env python3
"""
Test runner script for the Window Wash CRM.

This script can be used to run the test suite with different configurations,
including support for test parallelization.
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

    # By default, enable parallelization with 4 processes
    # Skip parallel execution if PYTEST_DISABLE_PARALLEL is set
    if not os.environ.get('PYTEST_DISABLE_PARALLEL'):
        args.append('--maxprocesses=4')

    # Handle specific test categories if provided as command line arguments
    if len(sys.argv) > 1:
        category = sys.argv[1].lower()

        if category == 'models':
            args.append('ww_crm/tests/unit/test_models.py')
        elif category == 'routes':
            args.append('ww_crm/tests/integration/test_routes.py')
        elif category == 'ui':
            args.append('ww_crm/tests/e2e/test_ui.py')
        elif category == 'utils':
            args.append('ww_crm/tests/test_utils.py')
        elif category == 'unit':
            args.append('-m unit')  # Run only unit tests
        elif category == 'integration':
            args.append('-m integration')  # Run only integration tests
        elif category == 'e2e':
            args.append('-m e2e')  # Run only end-to-end tests
        elif category == 'parallel':
            # Ensure we use parallelization
            if '--maxprocesses=4' not in args:
                args.append('--maxprocesses=4')
        elif category == 'sequential':
            # Disable parallelization
            if '--maxprocesses=4' in args:
                args.remove('--maxprocesses=4')
        else:
            args.append(sys.argv[1])  # Allow specifying a test file or pattern

    # Run tests with configured arguments
    return pytest.main(args)


if __name__ == '__main__':
    sys.exit(run_tests())
