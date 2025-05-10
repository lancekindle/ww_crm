from datetime import datetime
from ww_crm.db import db


class Customer(db.Model):
    """
    Customer model representing a window washing client.

    Attributes:
        id: Unique identifier for the customer
        name: Customer's name (required)
        phone: Customer's phone number
        email: Customer's email address
        address: Customer's physical address
        building_type: Type of building (residential, commercial)
        window_count: Number of windows at the customer's location
        notes: Additional notes about the customer
        created_at: When the customer record was created
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    window_count = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        """String representation of the Customer object."""
        return f"<Customer {self.id}: {self.name}>"


class Invoice(db.Model):
    """
    Invoice model representing a billing record for window washing services.

    Attributes:
        id: Unique identifier for the invoice
        customer_id: Foreign key to the customer this invoice belongs to
        service_date: When the service was/will be performed
        issue_date: When the invoice was created
        due_date: When payment is due
        amount: The total amount due
        status: Current status of the invoice (draft, sent, paid)
        service_description: Description of the services performed
    """
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    service_date = db.Column(db.DateTime, default=datetime.utcnow)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, sent, paid
    service_description = db.Column(db.Text)

    # Relationship
    customer = db.relationship('Customer', backref='invoices')

    def __repr__(self):
        """String representation of the Invoice object."""
        return f"<Invoice {self.id}: ${self.amount:.2f} - {self.status}>"
