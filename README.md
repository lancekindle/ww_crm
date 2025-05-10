# Window Wash CRM

A simple customer relationship management system for window washing businesses.

## Project Overview

This CRM application is designed with simplicity and maintainability in mind. It provides essential tools for small window washing businesses to manage customers, schedule jobs, and generate invoices.

## Features

- **Customer Management**: Add, edit, and track customer information
- **Invoice Management**: Create and track invoices for services
- **Mobile-Friendly UI**: Designed to work on mobile devices via a WebView

## Technology Stack

- **Backend**: Flask with SQLAlchemy
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript via WebView
- **Mobile Packaging**: Kivy (planned)

## Development Setup

1. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install the package in development mode:
   ```
   pip install -e .
   ```

3. Install development dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the Window Wash CRM application:

```
python main.py
```

This will start the Flask server on http://localhost:5000

Access the following endpoints:
- Home: http://localhost:5000/
- Customers: http://localhost:5000/customers
- Invoices: http://localhost:5000/invoices

## Running Tests

This project uses pytest for testing. The test suite includes unit tests, integration tests, and UI tests.

### Running All Tests

```
python run_tests.py
```

### Running Specific Test Categories

```
python run_tests.py models    # Run only model tests
python run_tests.py routes    # Run only route tests
python run_tests.py ui        # Run only UI tests
python run_tests.py utils     # Run only utility tests
```

### Test Structure

- `tests/conftest.py`: Test fixtures and configuration
- `tests/test_models.py`: Tests for database models
- `tests/test_routes.py`: Tests for API routes
- `tests/test_ui.py`: Playwright tests for the UI
- `tests/test_utils.py`: Tests for utility functions

## License

GPL3
