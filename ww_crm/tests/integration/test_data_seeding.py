"""
Tests for the data seeding functionality.

These tests demonstrate and verify the data seeding
capabilities for test data generation.
"""
import pytest
from ww_crm.models import Customer, Invoice
from ww_crm.tests.fixtures import CustomerFactory, InvoiceFactory, count_records

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


def test_customer_factory(db):
    """Test that the CustomerFactory creates valid Customer objects."""
    # Create a single customer with default values
    customer = CustomerFactory()

    # Verify customer was created and saved to the database
    assert customer.id is not None
    assert isinstance(customer, Customer)
    assert customer.name.startswith('Test Customer')
    assert '@example.com' in customer.email

    # Check record count in the database
    assert count_records(Customer) == 1


def test_invoice_factory(db):
    """Test that the InvoiceFactory creates valid Invoice objects with associations."""
    # Create an invoice which automatically creates a customer
    invoice = InvoiceFactory()

    # Verify invoice was created and saved
    assert invoice.id is not None
    assert isinstance(invoice, Invoice)

    # Verify customer relationship
    assert invoice.customer is not None
    assert invoice.customer.id is not None

    # Check record counts
    assert count_records(Customer) == 1
    assert count_records(Invoice) == 1


def test_invoice_with_specific_customer(db):
    """Test creating an invoice for a specific customer."""
    # Create a customer first
    customer = CustomerFactory(name="Special Customer")

    # Create invoices for this customer
    invoices = InvoiceFactory.create_batch(size=3, customer=customer)

    # Verify all invoices are linked to the same customer
    for invoice in invoices:
        assert invoice.customer.id == customer.id
        assert invoice.customer.name == "Special Customer"

    # Verify record counts
    assert count_records(Customer) == 1
    assert count_records(Invoice) == 3


def test_seeded_db_fixture(seeded_db):
    """Test that the seeded_db fixture properly seeds the database."""
    # Verify the returned data
    assert 'customers' in seeded_db
    assert 'invoices' in seeded_db

    # Check we have the expected number of records
    assert len(seeded_db['customers']) == 3
    assert len(seeded_db['invoices']) == 6

    # Verify record counts in the database match
    assert count_records(Customer) == 3
    assert count_records(Invoice) == 6

    # Verify relationships
    for invoice in seeded_db['invoices']:
        assert invoice.customer in seeded_db['customers']
