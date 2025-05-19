"""
Service layer for customer-related business logic.
"""

from flask import abort
from ww_crm.db import db
from ww_crm.models import Customer


class CustomerService:
    """Service class for handling customer-related operations."""
    
    @staticmethod
    def get_all_customers():
        """
        Get all customers from the database.
        
        Returns:
            list: List of Customer objects
        """
        return Customer.query.all()
    
    @staticmethod
    def get_customer_by_id(customer_id):
        """
        Get a specific customer by ID.
        
        Args:
            customer_id (int): The ID of the customer to retrieve
            
        Returns:
            Customer: The customer object if found
            
        Raises:
            404: If the customer is not found
        """
        customer = db.session.get(Customer, customer_id)
        if customer is None:
            abort(404)
        return customer
    
    @staticmethod
    def create_customer(data, is_form=False):
        """
        Create a new customer.
        
        Args:
            data (dict): Dictionary containing customer data
            is_form (bool): Whether data is from a form
            
        Returns:
            Customer: The newly created customer
        """
        customer = Customer.from_dict(data, is_form)
        db.session.add(customer)
        db.session.commit()
        return customer
    
    @staticmethod
    def update_customer(customer_id, data):
        """
        Update an existing customer.
        
        Args:
            customer_id (int): The ID of the customer to update
            data (dict): Dictionary containing updated customer data
            
        Returns:
            Customer: The updated customer
            
        Raises:
            404: If the customer is not found
        """
        customer = CustomerService.get_customer_by_id(customer_id)
        
        # Update customer fields
        customer.name = data.get("name", customer.name)
        customer.phone = data.get("phone", customer.phone)
        customer.email = data.get("email", customer.email)
        customer.address = data.get("address", customer.address)
        customer.service_units = data.get("service_units", customer.service_units)
        customer.notes = data.get("notes", customer.notes)
        
        db.session.commit()
        return customer
    
    @staticmethod
    def delete_customer(customer_id):
        """
        Delete a customer.
        
        Args:
            customer_id (int): The ID of the customer to delete
            
        Raises:
            404: If the customer is not found
        """
        customer = CustomerService.get_customer_by_id(customer_id)
        db.session.delete(customer)
        db.session.commit()