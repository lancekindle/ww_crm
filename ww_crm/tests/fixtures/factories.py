"""
Test data factories for Window Wash CRM.

This module provides factory classes for generating test data
instances of models that can be used in tests.
"""

import factory
import factory.fuzzy
from datetime import datetime, timedelta
from ww_crm.models import Customer, Invoice
from ww_crm.db import db


class CustomerFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Customer model instances for testing."""

    class Meta:
        model = Customer
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    # Basic information
    name = factory.Sequence(lambda n: f"Test Customer {n}")
    phone = factory.Sequence(lambda n: f"555-{n:03d}-{n+1000:04d}")
    email = factory.LazyAttribute(lambda obj: f'{obj.name.lower().replace(" ", ".")}@example.com')
    address = factory.Sequence(lambda n: f"{n+100} Test Street, Test City, 12345")

    # Additional fields
    building_type = factory.fuzzy.FuzzyChoice(["residential", "commercial"])
    window_count = factory.fuzzy.FuzzyInteger(5, 50)
    notes = factory.Faker("paragraph")
    created_at = factory.LazyFunction(datetime.utcnow)


class InvoiceFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating Invoice model instances for testing."""

    class Meta:
        model = Invoice
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    # Link to customer
    customer = factory.SubFactory(CustomerFactory)

    # Dates
    service_date = factory.LazyFunction(datetime.utcnow)
    issue_date = factory.LazyFunction(datetime.utcnow)
    due_date = factory.LazyAttribute(lambda obj: obj.issue_date + timedelta(days=30))

    # Invoice details
    amount = factory.fuzzy.FuzzyFloat(50, 500)
    status = factory.fuzzy.FuzzyChoice(["draft", "sent", "paid"])
    service_description = factory.fuzzy.FuzzyChoice(
        [
            "Regular window cleaning",
            "Deep cleaning service",
            "Interior and exterior windows",
            "Commercial window washing",
            "Residential full service",
        ]
    )
