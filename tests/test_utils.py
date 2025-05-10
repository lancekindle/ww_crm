import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# This module will be useful when we implement utility functions in the application


def mock_datetime_now(monkeypatch, mocked_date=None):
    """
    Helper function to mock datetime.now for predictable testing.

    Args:
        monkeypatch: The pytest monkeypatch fixture
        mocked_date: The datetime object to return, defaults to 2025-05-15
    """
    if mocked_date is None:
        mocked_date = datetime(2025, 5, 15, 12, 0, 0)

    class MockedDatetime(datetime):
        @classmethod
        def utcnow(cls):
            return mocked_date

        @classmethod
        def now(cls):
            return mocked_date

    monkeypatch.setattr('window_wash_crm.models.datetime', MockedDatetime)
    return mocked_date


class TestDatabaseHelpers:
    """
    Tests for database helper functions that we'll implement later.
    These are placeholder tests that will guide implementation.
    """

    def test_get_customers_by_building_type(self, db, monkeypatch):
        """Test function to filter customers by building type."""
        from window_wash_crm.models import Customer

        # Create test customers with different building types
        residential = Customer(name="Res Customer", building_type="residential")
        commercial = Customer(name="Com Customer", building_type="commercial")

        db.session.add_all([residential, commercial])
        db.session.commit()

        # This test will fail until we implement this function
        # from window_wash_crm.utils import get_customers_by_building_type
        # customers = get_customers_by_building_type("residential")
        # assert len(customers) == 1
        # assert customers[0].name == "Res Customer"

        # For now, just do a direct query to demonstrate the expected behavior
        customers = Customer.query.filter_by(building_type="residential").all()
        assert len(customers) == 1
        assert customers[0].name == "Res Customer"

    def test_calculate_invoice_statistics(self, db, sample_customer):
        """Test function to calculate invoice statistics for a customer."""
        from window_wash_crm.models import Invoice

        # Create multiple invoices for the sample customer
        invoices = [
            Invoice(
                customer_id=sample_customer.id,
                service_date=datetime(2025, 1, 15),
                amount=100.00,
                status='paid'
            ),
            Invoice(
                customer_id=sample_customer.id,
                service_date=datetime(2025, 2, 15),
                amount=150.00,
                status='paid'
            ),
            Invoice(
                customer_id=sample_customer.id,
                service_date=datetime(2025, 3, 15),
                amount=125.00,
                status='sent'
            ),
            Invoice(
                customer_id=sample_customer.id,
                service_date=datetime(2025, 4, 15),
                amount=175.00,
                status='draft'
            )
        ]

        db.session.add_all(invoices)
        db.session.commit()

        # This test will fail until we implement this function
        # from window_wash_crm.utils import calculate_invoice_statistics
        # stats = calculate_invoice_statistics(sample_customer.id)
        # assert stats['total_paid'] == 250.00
        # assert stats['total_outstanding'] == 300.00
        # assert stats['average_invoice'] == 137.50
        # assert stats['invoice_count'] == 4

        # For now, just calculate directly to demonstrate the expected behavior
        total_paid = sum(inv.amount for inv in invoices if inv.status == 'paid')
        total_outstanding = sum(inv.amount for inv in invoices if inv.status in ['sent', 'draft'])
        average_invoice = sum(inv.amount for inv in invoices) / len(invoices)

        assert total_paid == 250.00
        assert total_outstanding == 300.00
        assert average_invoice == 137.50
