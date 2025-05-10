import os
import tempfile
import pytest
from ww_crm.app import app as flask_app
from ww_crm.db import db as _db
from ww_crm.models import Customer, Invoice


@pytest.fixture(scope='session')
def app():
    """Create a Flask app configured for testing."""
    # Configure app for testing
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'DEBUG': False
    })

    # Set up the test database
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    # Create the database and application context
    with flask_app.app_context():
        _db.create_all()
        yield flask_app

    # Cleanup after tests
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='function')
def db(app):
    """
    Create a fresh database for each test.
    This is a function-scoped fixture, so it's destroyed after each test.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture(scope='function')
def sample_customer(db):
    """Create a sample customer for testing."""
    customer = Customer(
        name='Test Customer',
        phone='123-456-7890',
        email='test@example.com',
        address='123 Test St, Test City',
        building_type='residential',
        window_count=10,
        notes='Test notes'
    )
    db.session.add(customer)
    db.session.commit()
    return customer


@pytest.fixture(scope='function')
def sample_invoice(db, sample_customer):
    """Create a sample invoice for testing."""
    from datetime import datetime, timedelta

    today = datetime.utcnow()
    due_date = today + timedelta(days=30)

    invoice = Invoice(
        customer_id=sample_customer.id,
        service_date=today,
        issue_date=today,
        due_date=due_date,
        amount=150.00,
        status='draft',
        service_description='Test window cleaning service'
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice
