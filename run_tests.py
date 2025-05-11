#!/usr/bin/env python3
"""
Test runner script for the Window Wash CRM.

This script can be used to run the test suite with different configurations and supports
both serial and parallel test execution modes.

Examples:
    # Run all tests serially
    python run_tests.py

    # Run specific test category
    python run_tests.py models

    # Run tests in parallel
    python run_tests.py --parallel

    # Run specific tests in parallel with 4 workers
    python run_tests.py --parallel --workers=4 e2e
"""
import sys
import os
import pytest
import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Run Window Wash CRM tests')

    # Test selection options
    parser.add_argument('category', nargs='?', default=None,
                        help='Test category to run (models, routes, ui, utils, unit, integration, e2e, visual)')

    # Execution options
    parser.add_argument('--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('--workers', type=int, default=2, help='Number of parallel workers (default: 2)')
    parser.add_argument('--stop', action='store_true', help='Stop on first failure')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    # Special commands
    parser.add_argument('--check-waits', action='store_true', help='Check for explicit waits in UI tests')

    return parser.parse_args()


def run_tests():
    """Run the test suite with specified configurations."""
    # Add the project root directory to the Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)

    # Parse command line arguments
    args = parse_args()

    # Handle special commands
    if args.check_waits:
        from ww_crm.tools.check_explicit_waits import main as check_waits
        return check_waits()

    # Build pytest arguments
    pytest_args = []

    # Configure output verbosity
    if args.verbose:
        pytest_args.append('-v')

    # Always show print statements
    pytest_args.append('-s')

    # Stop on first failure if requested
    if args.stop:
        pytest_args.append('-x')

    # Use Python's native traceback format
    pytest_args.append('--tb=native')

    # Configure parallel execution if requested
    if args.parallel:
        pytest_args.extend([
            '-n', str(args.workers),
            '--conftest=ww_crm/tests/conftest_parallel.py'
        ])

    # Handle specific test categories
    if args.category:
        category = args.category.lower()

        if category == 'models':
            pytest_args.append('ww_crm/tests/unit/test_models.py')
        elif category == 'routes':
            pytest_args.append('ww_crm/tests/integration/test_routes.py')
        elif category == 'ui':
            pytest_args.append('ww_crm/tests/e2e/test_ui.py')
        elif category == 'utils':
            pytest_args.append('ww_crm/tests/test_utils.py')
        elif category == 'visual':
            pytest_args.append('ww_crm/tests/e2e/test_visual.py')
        elif category == 'unit':
            pytest_args.append('-m unit')  # Run only unit tests
        elif category == 'integration':
            pytest_args.append('-m integration')  # Run only integration tests
        elif category == 'e2e':
            pytest_args.append('-m e2e')  # Run only end-to-end tests
        else:
            # Allow specifying a test file or pattern
            pytest_args.append(category)

    # Print command being run
    print(f"Running: pytest {' '.join(pytest_args)}")

    # Run tests with configured arguments
    return pytest.main(pytest_args)


if __name__ == '__main__':
    sys.exit(run_tests())
