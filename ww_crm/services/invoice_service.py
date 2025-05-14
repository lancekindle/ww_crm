"""
Service layer for invoice-related business logic.
"""

from flask import abort
from ww_crm.db import db
from ww_crm.models import Invoice, Customer
from ww_crm.services.customer_service import CustomerService


class InvoiceService:
    """Service class for handling invoice-related operations."""
    
    @staticmethod
    def get_all_invoices():
        """
        Get all invoices from the database.
        
        Returns:
            list: List of Invoice objects
        """
        return Invoice.query.all()
    
    @staticmethod
    def get_invoice_by_id(invoice_id):
        """
        Get a specific invoice by ID.
        
        Args:
            invoice_id (int): The ID of the invoice to retrieve
            
        Returns:
            Invoice: The invoice object if found
            
        Raises:
            404: If the invoice is not found
        """
        invoice = db.session.get(Invoice, invoice_id)
        if invoice is None:
            abort(404)
        return invoice
    
    @staticmethod
    def get_customer_invoices(customer_id):
        """
        Get all invoices for a specific customer.
        
        Args:
            customer_id (int): The ID of the customer
            
        Returns:
            list: List of Invoice objects for the customer
            
        Raises:
            404: If the customer is not found
        """
        # Verify the customer exists
        CustomerService.get_customer_by_id(customer_id)
        
        # Return the customer's invoices
        return Invoice.query.filter_by(customer_id=customer_id).all()
    
    @staticmethod
    def create_invoice(data, is_form=False):
        """
        Create a new invoice.
        
        Args:
            data (dict): Dictionary containing invoice data
            is_form (bool): Whether data is from a form
            
        Returns:
            Invoice: The newly created invoice
            
        Raises:
            404: If the customer is not found
        """
        # Verify the customer exists
        customer_id = data.get("customer_id")
        CustomerService.get_customer_by_id(customer_id)
        
        # Create invoice
        invoice = Invoice.from_dict(data, is_form)
        db.session.add(invoice)
        db.session.commit()
        return invoice
    
    @staticmethod
    def update_invoice(invoice_id, data):
        """
        Update an existing invoice.
        
        Args:
            invoice_id (int): The ID of the invoice to update
            data (dict): Dictionary containing updated invoice data
            
        Returns:
            Invoice: The updated invoice
            
        Raises:
            404: If the invoice or customer is not found
        """
        invoice = InvoiceService.get_invoice_by_id(invoice_id)
        
        # Check if customer exists if customer_id is provided
        if "customer_id" in data:
            CustomerService.get_customer_by_id(data["customer_id"])
            invoice.customer_id = data["customer_id"]
        
        # Update each field if provided
        if "amount" in data:
            invoice.amount = data["amount"]
        
        if "status" in data:
            invoice.status = data["status"]
        
        if "service_description" in data:
            invoice.service_description = data["service_description"]
        
        # Handle dates specifically due to format conversion
        if "service_date" in data:
            # Assume date is already in the right format from validation
            invoice.service_date = data["service_date"]
        
        if "due_date" in data:
            # Assume date is already in the right format from validation
            invoice.due_date = data["due_date"]
        
        db.session.commit()
        return invoice
    
    @staticmethod
    def delete_invoice(invoice_id):
        """
        Delete an invoice.
        
        Args:
            invoice_id (int): The ID of the invoice to delete
            
        Raises:
            404: If the invoice is not found
        """
        invoice = InvoiceService.get_invoice_by_id(invoice_id)
        db.session.delete(invoice)
        db.session.commit()