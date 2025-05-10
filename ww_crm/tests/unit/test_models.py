import pytest
from datetime import datetime, timedelta
from ww_crm.models import Customer, Invoice

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


def test_customer_model(db):
    """Test that a customer can be created and retrieved."""
    # Create a customer
    customer = Customer(
        name='John Doe',
        phone='555-123-4567',
        email='john@example.com',
        address='456 Main St, Anytown',
        building_type='residential',
        window_count=8,
        notes='First time customer'
    )
    db.session.add(customer)
    db.session.commit()

    # Retrieve the customer from the database
    retrieved = Customer.query.filter_by(name='John Doe').first()

    # Verify customer attributes
    assert retrieved.id is not None
    assert retrieved.name == 'John Doe'
    assert retrieved.phone == '555-123-4567'
    assert retrieved.email == 'john@example.com'
    assert retrieved.address == '456 Main St, Anytown'
    assert retrieved.building_type == 'residential'
    assert retrieved.window_count == 8
    assert retrieved.notes == 'First time customer'
    assert isinstance(retrieved.created_at, datetime)


def test_invoice_model(db, sample_customer):
    """Test that an invoice can be created and retrieved."""
    # Setup dates
    today = datetime.utcnow()
    service_date = today - timedelta(days=2)
    due_date = today + timedelta(days=30)

    # Create an invoice
    invoice = Invoice(
        customer_id=sample_customer.id,
        service_date=service_date,
        issue_date=today,
        due_date=due_date,
        amount=120.50,
        status='sent',
        service_description='Window cleaning - 8 windows'
    )
    db.session.add(invoice)
    db.session.commit()

    # Retrieve the invoice from the database
    retrieved = Invoice.query.filter_by(amount=120.50).first()

    # Verify invoice attributes
    assert retrieved.id is not None
    assert retrieved.customer_id == sample_customer.id
    assert retrieved.amount == 120.50
    assert retrieved.status == 'sent'
    assert retrieved.service_description == 'Window cleaning - 8 windows'

    # Test relationship
    assert retrieved.customer.name == sample_customer.name


def test_customer_invoice_relationship(db, sample_customer, sample_invoice):
    """Test the relationship between customers and invoices."""
    # Verify that the invoice is linked to the customer
    assert sample_invoice in sample_customer.invoices

    # Verify that creating a new invoice for a customer updates the relationship
    new_invoice = Invoice(
        customer_id=sample_customer.id,
        service_date=datetime.utcnow(),
        amount=75.25,
        status='draft',
        service_description='Follow-up service'
    )
    db.session.add(new_invoice)
    db.session.commit()

    # Refresh sample_customer from the database
    db.session.refresh(sample_customer)

    # Check invoice count
    assert len(sample_customer.invoices) == 2

    # Verify new invoice is in customer's invoices
    assert any(inv.amount == 75.25 for inv in sample_customer.invoices)
