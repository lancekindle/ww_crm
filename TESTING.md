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
python run_tests.py visual      # Run visual regression tests

# Run tests by category
python run_tests.py unit        # Run all unit tests
python run_tests.py integration # Run all integration tests
python run_tests.py e2e         # Run all end-to-end tests

# Run tests with verbose output
python run_tests.py --verbose
python run_tests.py -v

# Run tests in parallel mode
python run_tests.py --parallel
python run_tests.py --parallel --workers=4  # Specify number of workers

# Stop on first test failure
python run_tests.py --stop

# Combine options
python run_tests.py --parallel --verbose unit  # Run unit tests in parallel with verbose output

# Special commands
python run_tests.py --check-waits  # Check for explicit waits in UI tests
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

# Run tests with verbose output
pytest -v
```

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

### Parallel Test Execution

The test suite supports parallel test execution to significantly improve test performance:

- Parallel execution is enabled with the `--parallel` flag
- Worker count can be customized with `--workers=N` (default is 2)
- Uses `pytest-xdist` under the hood for distributing tests
- Each worker gets isolated resources (database, server ports) to prevent conflicts
- Particularly beneficial for E2E tests which are traditionally slow

To run tests in parallel mode:
```bash
python run_tests.py --parallel
python run_tests.py --parallel --workers=4 e2e  # Run E2E tests with 4 workers
```

### Visual Regression Testing

The test suite includes visual regression testing capabilities:
- Captures screenshots of key UI states
- Compares screenshots against baseline images
- Highlights visual differences between runs
- Organized in `ww_crm/tests/e2e/screenshots/`

To run visual tests:
```bash
python run_tests.py visual
```

### Future Improvements

1. **Advanced Reporting**:
   - Implement detailed test reports with metrics and trends
   - Add visualization of test coverage and performance

2. **CI/CD Integration**:
   - Set up automated test runs on code changes
   - Implement test result reporting

3. **Load Testing**:
   - Add tools to measure application performance under load
   - Create benchmarks for key operations

4. **API Testing**:
   - Expand testing for API endpoints
   - Add contract testing for API interfaces
