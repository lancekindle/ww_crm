"""
Customer-related routes for the Window Wash CRM application.
"""

from flask import Blueprint, jsonify, request, render_template, abort, redirect, url_for
from ww_crm.db import db
from ww_crm.models import Customer

# Create blueprint for customer routes
bp = Blueprint("customers", __name__, url_prefix="/customers")


@bp.route("/", methods=["GET"])
@bp.route("", methods=["GET"])
def list_customers():
    """Return a list of all customers."""
    customers = Customer.query.all()
    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        # Return JSON if requested
        return jsonify(
            [
                {
                    "id": c.id,
                    "name": c.name,
                    "phone": c.phone,
                    "email": c.email,
                    "address": c.address,
                    "building_type": c.building_type,
                    "window_count": c.window_count,
                    "notes": c.notes,
                }
                for c in customers
            ]
        )
    # Return HTML
    return render_template("customers/list.html", customers=customers)


@bp.route("/create", methods=["GET", "POST"])
def create_customer():
    """Create a new customer."""
    if request.method == "POST":
        if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
            # Handle JSON data
            data = request.get_json()
            customer = Customer(
                name=data.get("name"),
                phone=data.get("phone"),
                email=data.get("email"),
                address=data.get("address"),
                building_type=data.get("building_type"),
                window_count=data.get("window_count"),
                notes=data.get("notes"),
            )
            db.session.add(customer)
            db.session.commit()

            # Return JSON response
            result = {
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "email": customer.email,
                "address": customer.address,
                "building_type": customer.building_type,
                "window_count": customer.window_count,
                "notes": customer.notes,
            }
            return jsonify(result), 201
        else:
            # Handle form data
            customer = Customer(
                name=request.form.get("name"),
                phone=request.form.get("phone"),
                email=request.form.get("email"),
                address=request.form.get("address"),
                building_type=request.form.get("building_type"),
                window_count=request.form.get("window_count"),
                notes=request.form.get("notes"),
            )
            db.session.add(customer)
            db.session.commit()

            # Redirect to customer list
            return redirect(url_for("customers.list_customers"))

    # Return the create form for GET requests
    return render_template("customers/create.html")


@bp.route("/<int:customer_id>", methods=["GET"])
def view_customer(customer_id):
    """View a specific customer."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        abort(404)

    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        # Return JSON if requested
        result = {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "address": customer.address,
            "building_type": customer.building_type,
            "window_count": customer.window_count,
            "notes": customer.notes,
        }
        return jsonify(result)

    # Return HTML view
    return render_template("customers/view.html", customer=customer)


@bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    """Update a specific customer."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        abort(404)

    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        data = request.get_json()

        # Update customer fields
        customer.name = data.get("name", customer.name)
        customer.phone = data.get("phone", customer.phone)
        customer.email = data.get("email", customer.email)
        customer.address = data.get("address", customer.address)
        customer.building_type = data.get("building_type", customer.building_type)
        customer.window_count = data.get("window_count", customer.window_count)
        customer.notes = data.get("notes", customer.notes)

        db.session.commit()

        # Return updated customer
        result = {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "address": customer.address,
            "building_type": customer.building_type,
            "window_count": customer.window_count,
            "notes": customer.notes,
        }
        return jsonify(result)

    # Handle form data (not implemented in this example)
    abort(415)


@bp.route("/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    """Delete a specific customer."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        abort(404)

    db.session.delete(customer)
    db.session.commit()

    # Return 204 No Content
    return "", 204


@bp.route("/<int:customer_id>/invoices", methods=["GET"])
def customer_invoices(customer_id):
    """Get all invoices for a specific customer."""
    customer = db.session.get(Customer, customer_id)
    if customer is None:
        abort(404)

    if request.headers.get("Accept") == "application/json" or request.content_type == "application/json":
        # Return JSON if requested
        return jsonify(
            [
                {
                    "id": invoice.id,
                    "service_date": invoice.service_date.isoformat(),
                    "issue_date": invoice.issue_date.isoformat(),
                    "due_date": invoice.due_date.isoformat() if invoice.due_date else None,
                    "amount": invoice.amount,
                    "status": invoice.status,
                    "service_description": invoice.service_description,
                }
                for invoice in customer.invoices
            ]
        )

    # Return HTML view
    return render_template("customers/invoices.html", customer=customer)
