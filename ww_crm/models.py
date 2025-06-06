from datetime import datetime
from ww_crm.db import db
from ww_crm.utils.constants import InvoiceStatus


class Customer(db.Model):
    """
    Customer model representing a service business client.

    Attributes:
        id: Unique identifier for the customer
        name: Customer's name (required)
        phone: Customer's phone number
        email: Customer's email address
        address: Customer's physical address
        service_units: Number of service units (e.g., windows, fixtures)
        notes: Additional notes about the customer
        created_at: When the customer record was created
        last_invoice_date: Date of the most recent invoice
        last_invoice_amount: Amount of the most recent invoice
        last_invoice_description: Description of the most recent invoice
        last_invoice_id: ID of the most recent invoice
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    service_units = db.Column(db.Integer)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Denormalized fields for easier querying
    last_invoice_date = db.Column(db.DateTime)
    last_invoice_amount = db.Column(db.Float)
    last_invoice_description = db.Column(db.Text)
    last_invoice_id = db.Column(db.Integer)

    def __repr__(self):
        """String representation of the Customer object."""
        return f"<Customer {self.id}: {self.name}>"
        
    def to_dict(self):
        """
        Convert customer to dictionary for API responses.
        
        Returns:
            Dictionary of customer data
        """
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "service_units": self.service_units,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_invoice_date": self.last_invoice_date.isoformat() if self.last_invoice_date else None,
            "last_invoice_amount": self.last_invoice_amount,
            "last_invoice_description": self.last_invoice_description,
            "last_invoice_id": self.last_invoice_id,
        }
        
    @classmethod
    def from_dict(cls, data, is_form=False):
        """
        Create a customer instance from a dictionary (JSON or form data).
        
        Args:
            data: Dictionary containing customer data
            is_form: Whether the data is from a form
            
        Returns:
            Customer instance (not yet added to session)
        """
        # Handle service_units type conversion for form data
        service_units = data.get("service_units")
        if is_form and service_units is not None and service_units != "":
            service_units = int(service_units)
        
        # Create customer
        return cls(
            name=data.get("name"),
            phone=data.get("phone"),
            email=data.get("email"),
            address=data.get("address"),
            service_units=service_units,
            notes=data.get("notes")
        )


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
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    service_date = db.Column(db.DateTime, default=datetime.utcnow)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default=InvoiceStatus.DRAFT)
    service_description = db.Column(db.Text)

    # Relationship
    customer = db.relationship("Customer", backref="invoices")

    def __repr__(self):
        """String representation of the Invoice object."""
        return f"<Invoice {self.id}: ${self.amount:.2f} - {self.status}>"

    @classmethod
    def from_dict(cls, data, is_form=False):
        """
        Create an invoice instance from a dictionary (JSON or form data).

        Args:
            data: Dictionary containing invoice data
            is_form: Whether the data is from a form (affects date parsing)

        Returns:
            Invoice instance (not yet added to session)
        """
        # Parse dates based on the source format
        service_date = None
        if data.get("service_date"):
            if is_form:
                service_date = datetime.strptime(data.get("service_date"), "%Y-%m-%d")
            else:
                service_date = datetime.fromisoformat(data.get("service_date"))

        due_date = None
        if data.get("due_date"):
            if is_form:
                due_date = datetime.strptime(data.get("due_date"), "%Y-%m-%d")
            else:
                due_date = datetime.fromisoformat(data.get("due_date"))

        # Handle amount type conversion for form data
        amount = data.get("amount")
        if is_form and amount is not None:
            amount = float(amount)

        # Create invoice
        return cls(
            customer_id=data.get("customer_id"),
            service_date=service_date,
            due_date=due_date,
            amount=amount,
            status=data.get("status", InvoiceStatus.DRAFT),
            service_description=data.get("service_description"),
        )

    def to_dict(self):
        """
        Convert invoice to dictionary for API responses.

        Returns:
            Dictionary of invoice data
        """
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "service_date": self.service_date.isoformat(),
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "amount": self.amount,
            "status": self.status,
            "service_description": self.service_description,
        }
