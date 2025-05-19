"""
Customer-related routes for the Window Wash CRM application.
"""

from flask import Blueprint, request
from ww_crm.models import Customer
from ww_crm.services.customer_service import CustomerService
from ww_crm.services.invoice_service import InvoiceService
from ww_crm.services.business_config_service import BusinessConfigService
from ww_crm.utils.response import render_response, created_response, no_content_response

# Create blueprint for customer routes
bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def list_customers():
    """Return a list of all customers."""
    customers = CustomerService.get_all_customers()
    
    # Get business settings
    settings = BusinessConfigService.get_settings()
    
    # Prepare JSON data
    json_data = [customer.to_dict() for customer in customers]
    
    # Return appropriate response
    return render_response("customers/list.html", json_data, 
                          customers=customers, settings=settings)


@bp.route("/create", methods=["GET", "POST"])
def create_customer():
    """Create a new customer."""
    if request.method == "POST":
        # Get data from either JSON or form
        is_json = request.headers.get("Accept") == "application/json" or request.content_type == "application/json"
        data = request.get_json() if is_json else request.form
        
        # Create customer
        customer = CustomerService.create_customer(data, not is_json)
        
        # Return appropriate response
        return created_response(
            customer.to_dict(),
            redirect_endpoint="customers.list_customers" if not is_json else None
        )

    # Get business settings
    settings = BusinessConfigService.get_settings()
    
    # Return the create form for GET requests
    return render_response("customers/create.html", {}, 
                          settings=settings)


@bp.route("/<int:customer_id>", methods=["GET"])
def view_customer(customer_id):
    """View a specific customer."""
    # Get customer
    customer = CustomerService.get_customer_by_id(customer_id)
    
    # Get business settings
    settings = BusinessConfigService.get_settings()
    
    # Return appropriate response
    return render_response("customers/view.html", customer.to_dict(), 
                          customer=customer, settings=settings)


@bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Update a specific customer."""
    # Get data
    data = request.get_json()
    
    # Update customer
    customer = CustomerService.update_customer(customer_id, data)
    
    # Return updated customer
    return render_response(None, customer.to_dict())


@bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Delete a specific customer."""
    # Delete customer
    CustomerService.delete_customer(customer_id)
    
    # Return no content
    return no_content_response()


@bp.route("/<int:customer_id>/invoices", methods=["GET"])
def customer_invoices(customer_id):
    """Get all invoices for a specific customer."""
    # Get customer and invoices
    customer = CustomerService.get_customer_by_id(customer_id)
    invoices = InvoiceService.get_customer_invoices(customer_id)
    
    # Prepare JSON data
    json_data = [invoice.to_dict() for invoice in invoices]
    
    # Return appropriate response
    return render_response("customers/invoices.html", json_data, customer=customer)
