"""
Database utilities for testing.

This module provides functions for seeding the database with test data,
cleaning up test data, and other database-related test utilities.
"""

from typing import Dict, List, Union, Optional
from ww_crm.models import Customer, Invoice
from ww_crm.db import db
from .factories import CustomerFactory, InvoiceFactory


def seed_test_data(
    num_customers: int = 5, invoices_per_customer: int = 2, session: Optional[object] = None
) -> Dict[str, List[Union[Customer, Invoice]]]:
    """
    Seed the database with test customers and invoices.

    Args:
        num_customers: Number of customer records to create
        invoices_per_customer: Number of invoices to create per customer
        session: SQLAlchemy session to use (defaults to db.session)

    Returns:
        Dictionary containing lists of created customers and invoices
    """
    if session is None:
        session = db.session

    # Create customers
    customers = CustomerFactory.create_batch(size=num_customers)

    # Create invoices for each customer
    invoices = []
    for customer in customers:
        customer_invoices = InvoiceFactory.create_batch(size=invoices_per_customer, customer=customer)
        invoices.extend(customer_invoices)

    # Return all created objects
    return {"customers": customers, "invoices": invoices}


def clear_test_data(session: Optional[object] = None) -> None:
    """
    Clear all test data from the database.

    Args:
        session: SQLAlchemy session to use (defaults to db.session)
    """
    if session is None:
        session = db.session

    # Delete all invoices first (due to foreign key constraints)
    session.query(Invoice).delete()

    # Then delete all customers
    session.query(Customer).delete()

    # Commit the transaction
    session.commit()


def count_records(model_class: object, session: Optional[object] = None) -> int:
    """
    Count the number of records for a given model.

    Args:
        model_class: SQLAlchemy model class to count
        session: SQLAlchemy session to use (defaults to db.session)

    Returns:
        Integer count of records
    """
    if session is None:
        session = db.session

    return session.query(model_class).count()
