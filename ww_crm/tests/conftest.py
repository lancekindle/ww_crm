"""
Pytest configuration and fixtures for Window Wash CRM tests.
"""

import os
import tempfile
import pytest
from ww_crm.app import create_app
from ww_crm.db import db as _db
from ww_crm.models import Customer, Invoice
from ww_crm.tests.fixtures import CustomerFactory, InvoiceFactory, seed_test_data


# --------------------------------
# Application Fixtures
# --------------------------------


@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing using the application factory."""
    # Create a test configuration
    test_config = {"TESTING": True, "WTF_CSRF_ENABLED": False, "DEBUG": False}

    # Set up the test database
    db_fd, db_path = tempfile.mkstemp()
    test_config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

    # Create the app with test configuration
    flask_app = create_app(test_config)

    # Create the database and application context
    with flask_app.app_context():
        _db.create_all()
        yield flask_app

    # Cleanup after tests
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def db(app):
    """
    Create a fresh database for each test.
    This is a function-scoped fixture, so it's destroyed after each test.
    """
    with app.app_context():
        _db.drop_all()  # Drop all tables first
        _db.create_all()  # Recreate all tables
        yield _db
        _db.session.rollback()  # Ensure any failed transactions are rolled back
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app, db):
    """Create a test client for the Flask application."""
    return app.test_client()


# --------------------------------
# Test Data Fixtures
# --------------------------------


@pytest.fixture(scope="function")
def sample_customer(db):
    """Create a sample customer for testing using the factory."""
    return CustomerFactory()


@pytest.fixture(scope="function")
def sample_invoice(db, sample_customer):
    """Create a sample invoice for testing using the factory."""
    return InvoiceFactory(customer=sample_customer)


@pytest.fixture(scope="function")
def seeded_db(db):
    """
    Create a database seeded with a standard set of test data.

    Returns:
        A dictionary containing lists of created customers and invoices
    """
    return seed_test_data(num_customers=3, invoices_per_customer=2)


# --------------------------------
# UI Test Fixtures
# --------------------------------


@pytest.fixture(scope="function")
def selenium_browser():
    """
    Placeholder for a Selenium WebDriver instance.
    This would be used for browser automation tests.
    """
    # NOTE: This would be implemented when needed
    # For now it's just a placeholder to show structure
    pass
