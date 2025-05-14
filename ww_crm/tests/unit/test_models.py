import pytest
from datetime import datetime, timedelta
from ww_crm.models import Customer, Invoice
from ww_crm.utils.constants import InvoiceStatus, BuildingType

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit


def test_customer_model(db):
    """Test that a customer can be created and retrieved."""
    # Create a customer
    customer = Customer(
        name="John Doe",
        phone="555-123-4567",
        email="john@example.com",
        address="456 Main St, Anytown",
        building_type="residential",
        service_units=8,
        notes="First time customer",
    )
    db.session.add(customer)
    db.session.commit()

    # Retrieve the customer from the database
    retrieved = Customer.query.filter_by(name="John Doe").first()

    # Verify customer attributes
    assert retrieved.id is not None
    assert retrieved.name == "John Doe"
    assert retrieved.phone == "555-123-4567"
    assert retrieved.email == "john@example.com"
    assert retrieved.address == "456 Main St, Anytown"
    assert retrieved.building_type == "residential"
    assert retrieved.service_units == 8
    assert retrieved.notes == "First time customer"
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
        status="sent",
        service_description="Window cleaning - 8 windows",
    )
    db.session.add(invoice)
    db.session.commit()

    # Retrieve the invoice from the database
    retrieved = Invoice.query.filter_by(amount=120.50).first()

    # Verify invoice attributes
    assert retrieved.id is not None
    assert retrieved.customer_id == sample_customer.id
    assert retrieved.amount == 120.50
    assert retrieved.status == "sent"
    assert retrieved.service_description == "Window cleaning - 8 windows"

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
        status="draft",
        service_description="Follow-up service",
    )
    db.session.add(new_invoice)
    db.session.commit()

    # Refresh sample_customer from the database
    db.session.refresh(sample_customer)

    # Check invoice count
    assert len(sample_customer.invoices) == 2

    # Verify new invoice is in customer's invoices
    assert any(inv.amount == 75.25 for inv in sample_customer.invoices)


def test_customer_last_invoice_fields(db):
    """Test the denormalized last_invoice fields on the Customer model."""
    # Create a customer
    customer = Customer(
        name="Jane Smith",
        phone="555-987-6543",
        building_type=BuildingType.RESIDENTIAL
    )
    db.session.add(customer)
    db.session.commit()
    
    # Create an initial invoice
    first_invoice = Invoice(
        customer_id=customer.id,
        service_date=datetime.utcnow() - timedelta(days=30),
        amount=100.00,
        status=InvoiceStatus.PAID,
        service_description="Initial service",
    )
    db.session.add(first_invoice)
    db.session.commit()
    
    # Manually update the last invoice fields (normally done by service layer)
    customer.last_invoice_date = first_invoice.service_date
    customer.last_invoice_amount = first_invoice.amount
    customer.last_invoice_description = first_invoice.service_description
    customer.last_invoice_id = first_invoice.id
    db.session.commit()
    
    # Verify fields are set
    assert customer.last_invoice_date == first_invoice.service_date
    assert customer.last_invoice_amount == 100.00
    assert customer.last_invoice_description == "Initial service"
    assert customer.last_invoice_id == first_invoice.id
    
    # Create a newer invoice
    second_invoice = Invoice(
        customer_id=customer.id,
        service_date=datetime.utcnow() - timedelta(days=10),
        amount=150.00,
        status=InvoiceStatus.SENT,
        service_description="Follow-up service",
    )
    db.session.add(second_invoice)
    db.session.commit()
    
    # Update the last invoice fields again
    customer.last_invoice_date = second_invoice.service_date
    customer.last_invoice_amount = second_invoice.amount
    customer.last_invoice_description = second_invoice.service_description
    customer.last_invoice_id = second_invoice.id
    db.session.commit()
    
    # Verify fields are updated
    assert customer.last_invoice_amount == 150.00
    assert customer.last_invoice_description == "Follow-up service"
    assert customer.last_invoice_id == second_invoice.id
    
    # Verify to_dict includes the last_invoice fields
    customer_dict = customer.to_dict()
    assert customer_dict["last_invoice_amount"] == 150.00
    assert customer_dict["last_invoice_description"] == "Follow-up service"
    assert customer_dict["last_invoice_id"] == second_invoice.id


def test_invoice_from_dict_method():
    """Test the from_dict method for creating an Invoice from dictionary data."""
    # Test with JSON data
    json_data = {
        'customer_id': 1,
        'service_date': '2024-05-01T12:00:00',
        'due_date': '2024-06-01T12:00:00',
        'amount': 150.75,
        'status': 'draft',
        'service_description': 'Test service'
    }

    invoice = Invoice.from_dict(json_data, is_form=False)

    assert invoice.customer_id == 1
    assert invoice.service_date.isoformat() == '2024-05-01T12:00:00'
    assert invoice.due_date.isoformat() == '2024-06-01T12:00:00'
    assert invoice.amount == 150.75
    assert invoice.status == 'draft'
    assert invoice.service_description == 'Test service'

    # Test with form data
    form_data = {
        'customer_id': 2,
        'service_date': '2024-05-15',
        'due_date': '2024-06-15',
        'amount': '200.50',
        'status': 'sent',
        'service_description': 'Another test service'
    }

    invoice = Invoice.from_dict(form_data, is_form=True)

    assert invoice.customer_id == 2
    assert invoice.service_date.strftime('%Y-%m-%d') == '2024-05-15'
    assert invoice.due_date.strftime('%Y-%m-%d') == '2024-06-15'
    assert invoice.amount == 200.50
    assert invoice.status == 'sent'
    assert invoice.service_description == 'Another test service'


def test_invoice_to_dict_method(db, sample_invoice):
    """Test the to_dict method for converting an Invoice to a dictionary."""
    invoice_dict = sample_invoice.to_dict()

    assert invoice_dict['id'] == sample_invoice.id
    assert invoice_dict['customer_id'] == sample_invoice.customer_id
    assert invoice_dict['service_date'] == sample_invoice.service_date.isoformat()
    assert invoice_dict['issue_date'] == sample_invoice.issue_date.isoformat()
    assert invoice_dict['due_date'] == sample_invoice.due_date.isoformat() if sample_invoice.due_date else None
    assert invoice_dict['amount'] == sample_invoice.amount
    assert invoice_dict['status'] == sample_invoice.status
    assert invoice_dict['service_description'] == sample_invoice.service_description
