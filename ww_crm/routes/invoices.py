"""
Invoice-related routes for the Window Wash CRM application.
"""

from flask import Blueprint, request
from ww_crm.models import Customer
from ww_crm.services.invoice_service import InvoiceService
from ww_crm.services.customer_service import CustomerService
from ww_crm.services.business_config_service import BusinessConfigService
from ww_crm.utils.response import render_response, created_response, no_content_response
from ww_crm.utils.constants import InvoiceStatus

# Create blueprint for invoice routes
bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def list_invoices():
    """Return a list of all invoices."""
    invoices = InvoiceService.get_all_invoices()

    # Prepare JSON data
    json_data = [invoice.to_dict() for invoice in invoices]
    
    # Add customer names for API responses
    for i, invoice in enumerate(invoices):
        json_data[i]["customer_name"] = invoice.customer.name
    
    # Return appropriate response
    return render_response("invoices/list.html", json_data, invoices=invoices)


@bp.route("/create", methods=["GET", "POST"])
def create_invoice():
    """Create a new invoice."""
    if request.method == "POST":
        # Get data from either JSON or form
        is_json = request.headers.get("Accept") == "application/json" or request.content_type == "application/json"
        data = request.get_json() if is_json else request.form

        # Create invoice
        invoice = InvoiceService.create_invoice(data, not is_json)
        
        # Prepare response data
        json_data = invoice.to_dict()
        json_data["customer_name"] = invoice.customer.name
        
        # Return appropriate response
        return created_response(
            json_data,
            template_name="invoices/list.html" if not is_json else None
        )

    # Get customers for dropdown and business settings
    customers = CustomerService.get_all_customers()
    settings = BusinessConfigService.get_settings()
    
    return render_response("invoices/create.html", {}, 
                          customers=customers, 
                          invoice_statuses=InvoiceStatus.ALL,
                          settings=settings)


@bp.route("/<int:invoice_id>", methods=["GET"])
def view_invoice(invoice_id):
    """View a specific invoice."""
    # Get invoice
    invoice = InvoiceService.get_invoice_by_id(invoice_id)
    
    # Get business settings and render SMS template
    settings = BusinessConfigService.get_settings()
    sms_text = BusinessConfigService.render_sms_template(invoice)
    
    # Prepare JSON data
    json_data = invoice.to_dict()
    json_data["customer_name"] = invoice.customer.name
    
    # Return appropriate response
    return render_response("invoices/view.html", json_data, 
                          invoice=invoice, 
                          settings=settings,
                          sms_text=sms_text)


@bp.route("/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    """Update a specific invoice."""
    # Get data
    data = request.get_json()
    
    # Handle dates if provided
    if "service_date" in data and isinstance(data["service_date"], str):
        from datetime import datetime
        data["service_date"] = datetime.fromisoformat(data["service_date"])
        
    if "due_date" in data and isinstance(data["due_date"], str):
        from datetime import datetime
        data["due_date"] = datetime.fromisoformat(data["due_date"])
    
    # Update invoice
    invoice = InvoiceService.update_invoice(invoice_id, data)
    
    # Prepare response data
    json_data = invoice.to_dict()
    json_data["customer_name"] = invoice.customer.name
    
    # Return updated invoice
    return render_response(None, json_data)


@bp.route("/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    """Delete a specific invoice."""
    # Delete invoice
    InvoiceService.delete_invoice(invoice_id)
    
    # Return no content
    return no_content_response()
