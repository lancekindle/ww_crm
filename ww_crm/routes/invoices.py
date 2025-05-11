"""
Invoice-related routes for the Window Wash CRM application.
"""

from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, abort
from ww_crm.db import db
from ww_crm.models import Invoice, Customer

# Create blueprint for invoice routes
bp = Blueprint("invoices", __name__, url_prefix="/invoices")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def list_invoices():
    """Return a list of all invoices."""
    invoices = Invoice.query.all()

    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        # Return JSON if requested
        results = [i.to_dict() for i in invoices]
        # Add customer names for API responses
        for i, invoice in enumerate(invoices):
            results[i]["customer_name"] = invoice.customer.name
        return jsonify(results)

    # Return HTML
    return render_template("invoices/list.html", invoices=invoices)


@bp.route("/create", methods=["GET", "POST"])
def create_invoice():
    """Create a new invoice."""
    if request.method == "POST":
        # Get data from either JSON or form
        is_json = request.headers.get("Accept") == "application/json" or request.content_type == "application/json"
        data = request.get_json() if is_json else request.form

        # Check if customer exists
        customer_id = data.get("customer_id")
        customer = db.session.get(Customer, customer_id)
        if customer is None:
            abort(404)

        # Create invoice from data
        invoice = Invoice.from_dict(data, is_form=not is_json)
        db.session.add(invoice)
        db.session.commit()

        # Return appropriate response based on request type
        if is_json:
            return jsonify(invoice.to_dict()), 201
        else:
            return render_template("invoices/list.html"), 201

    # Get customers for dropdown and return the create form for GET requests
    customers = Customer.query.all()
    return render_template("invoices/create.html", customers=customers)


@bp.route("/<int:invoice_id>", methods=["GET"])
def view_invoice(invoice_id):
    """View a specific invoice."""
    invoice = db.session.get(Invoice, invoice_id)
    if invoice is None:
        abort(404)

    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        # Return JSON if requested
        result = invoice.to_dict()
        # Add customer name for API response
        result["customer_name"] = invoice.customer.name
        return jsonify(result)

    # Return HTML view
    return render_template("invoices/view.html", invoice=invoice)


@bp.route("/<int:invoice_id>", methods=["PUT"])
def update_invoice(invoice_id):
    """Update a specific invoice."""
    invoice = db.session.get(Invoice, invoice_id)
    if invoice is None:
        abort(404)

    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        data = request.get_json()

        # Check if customer exists if customer_id is provided
        if "customer_id" in data:
            customer = db.session.get(Customer, data["customer_id"])
            if customer is None:
                abort(404)
            invoice.customer_id = data["customer_id"]

        # Update each field explicitly
        if "amount" in data:
            invoice.amount = data["amount"]

        if "status" in data:
            invoice.status = data["status"]

        if "service_description" in data:
            invoice.service_description = data["service_description"]

        # Handle dates specifically due to format conversion
        if "service_date" in data:
            invoice.service_date = datetime.fromisoformat(data["service_date"])

        if "due_date" in data:
            invoice.due_date = datetime.fromisoformat(data["due_date"])

        db.session.commit()

        # Return updated invoice
        return jsonify(invoice.to_dict())

    # Handle form data (not implemented in this example)
    abort(415)


@bp.route("/<int:invoice_id>", methods=["DELETE"])
def delete_invoice(invoice_id):
    """Delete a specific invoice."""
    invoice = db.session.get(Invoice, invoice_id)
    if invoice is None:
        abort(404)

    db.session.delete(invoice)
    db.session.commit()

    # Return 204 No Content
    return "", 204
