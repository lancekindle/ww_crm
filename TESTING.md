# Testing Guide for Window Wash CRM

This document provides a comprehensive guide to the testing infrastructure for the Window Wash CRM application.

## Test Structure

The test suite is organized into three main categories:

- **Unit Tests**: Test individual components in isolation (models, functions)
- **Integration Tests**: Test interactions between components (routes, database operations)
- **End-to-End (E2E) Tests**: Test the application from a user's perspective (UI tests)

### Directory Structure

```
ww_crm/tests/
├── conftest.py              # Shared test fixtures and configuration
├── test_utils.py            # Utility test helpers
├── test_imports.py          # Import verification tests
├── e2e/                     # End-to-end tests
│   ├── pages/               # Page Object Model components
│   │   ├── base_page.py     # Base classes for page objects
│   │   ├── home_page.py     # Home page interactions
│   │   ├── customer_*       # Customer-related page objects
│   │   ├── invoice_*        # Invoice-related page objects
│   │   └── selectors.py     # Centralized CSS selectors
│   └── test_ui.py           # UI test cases
├── integration/             # Integration tests
│   ├── test_routes.py       # API and view route tests
│   └── test_data_seeding.py # Database seeding tests
└── unit/                    # Unit tests
    └── test_models.py       # Database model tests
```

## Running Tests

### Using the Test Runner Script

The project includes a dedicated test runner script that provides various options for running tests:

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py models      # Run model tests
python run_tests.py routes      # Run route tests
python run_tests.py ui          # Run UI tests
python run_tests.py utils       # Run utility tests

# Run tests by category
python run_tests.py unit        # Run all unit tests
python run_tests.py integration # Run all integration tests
python run_tests.py e2e         # Run all end-to-end tests

# Control parallelization
python run_tests.py parallel    # Force parallel testing
python run_tests.py sequential  # Disable parallel testing
```

### Using pytest Directly

You can also use pytest directly with additional options:

```bash
# Run all tests
pytest

# Run tests with specific markers
pytest -m unit
pytest -m integration
pytest -m e2e

# Run tests in parallel with specified number of processes
pytest --maxprocesses=4

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
```

## Test Parallelization

The test suite supports parallel test execution to speed up the testing process. This is implemented using the pytest-xdist plugin.

### How It Works

- By default, tests run with 4 parallel processes
- The number of processes can be adjusted in the `pyproject.toml` file or via command-line arguments
- Test categories are designed to be run in isolation to prevent conflicts
- Fixture scoping ensures proper resource management

### Controlling Parallelization

You can control parallelization using these methods:

1. Environment variable: `PYTEST_DISABLE_PARALLEL=1 python run_tests.py`
2. Command flag: `python run_tests.py sequential`
3. Direct pytest option: `pytest --maxprocesses=1`

## Test Types and Fixtures

### Unit Tests

Unit tests focus on testing individual components in isolation. They use the following fixtures:

- `db`: A fresh database instance for each test
- Mocks for various dependencies to ensure isolation

### Integration Tests

Integration tests verify the interactions between components. Key fixtures include:

- `app`: The Flask application configured for testing
- `client`: A Flask test client for making HTTP requests
- `db`: A database instance with proper transaction handling
- `sample_customer`, `sample_invoice`: Pre-created sample data

### End-to-End (E2E) Tests

E2E tests validate the application from a user's perspective using Playwright for browser automation. They rely on:

- `live_server`: A running instance of the application
- `page`: A Playwright browser page
- Page Object Model classes to organize UI interactions

## Page Object Model (POM)

The E2E tests use the Page Object Model pattern to organize UI interactions and improve test maintainability.

### Key Components

1. **Base Classes**:
   - `BasePage`: Common page operations and assertions
   - `NavigablePage`: Navigation capabilities
   - `FormPage`: Form handling capabilities

2. **Page-Specific Classes**:
   - Each page of the application has a dedicated class
   - Methods model user interactions (click, fill forms, etc.)
   - Assertions verify page state

3. **Selector Registry**:
   - Centralized in `selectors.py`
   - Organized by page and element type
   - Makes selectors easier to maintain

### Benefits of POM

- **Improved Readability**: Test code clearly describes user actions
- **Better Maintainability**: UI changes only require updates in one place
- **Reusability**: Page objects can be used across multiple tests
- **Abstraction**: Complex UI interactions are simplified

## Test Data Management

The test suite includes a robust data generation and management system:

### Factories

The test suite uses the Factory pattern to generate test data:

- `CustomerFactory`: Creates customer records with sensible defaults
- `InvoiceFactory`: Creates invoice records with associated customers

### Benefits of Factories

- **Deterministic Testing**: Tests use consistent, predictable data
- **Focused Tests**: Only specify the attributes relevant to the test
- **Reduced Duplication**: Avoid repeating test data creation code
- **Relationship Handling**: Automatically create required related records

## Test Documentation

Each test file and test function includes detailed docstrings explaining:

1. The purpose of the test
2. What is being tested
3. Expected outcomes
4. Any special considerations

## Continuous Improvement

The test suite is designed to evolve with the application. The testing strategy follows these principles:

1. **Comprehensive Coverage**: Aim for high coverage of both code and functionality
2. **Fast Feedback**: Tests are optimized for speed to support rapid development
3. **Maintainability**: Test code is treated with the same care as production code
4. **Documentation**: Keep testing documentation updated with changes

## Recent Improvements

### Phase 4 Improvements

1. **Fixed SQLAlchemy Deprecation Warnings**:
   - Updated all uses of `query.get()` to `db.session.get()` with proper error handling
   - This addresses SQLAlchemy 2.0 compatibility

2. **Implemented Test Parallelization**:
   - Added pytest-xdist support for parallel test execution
   - Configured test categories to run in parallel safely
   - Added controls to enable/disable parallelization

3. **Added Comprehensive Documentation**:
   - Created detailed testing documentation (this file)
   - Improved docstrings and comments throughout test code
   - Added examples for common testing patterns

### Future Improvements

1. **Additional UI Test Coverage**:
   - Complete the form submission test implementation
   - Add tests for edge cases and error handling

2. **CI/CD Integration**:
   - Set up automated test runs on code changes
   - Implement test result reporting

3. **Performance Monitoring**:
   - Add metrics to track test execution time
   - Optimize slow tests to improve developer experience
