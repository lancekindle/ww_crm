"""
Invoice-related routes for the Window Wash CRM application.
"""
from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, abort
from ww_crm.db import db
from ww_crm.models import Invoice, Customer

# Create blueprint for invoice routes
bp = Blueprint('invoices', __name__, url_prefix='/invoices')


@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
def list_invoices():
    """Return a list of all invoices."""
    invoices = Invoice.query.all()

    if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
        # Return JSON if requested
        return jsonify([{
            'id': i.id,
            'customer_id': i.customer_id,
            'customer_name': i.customer.name,
            'service_date': i.service_date.isoformat(),
            'issue_date': i.issue_date.isoformat(),
            'due_date': i.due_date.isoformat() if i.due_date else None,
            'amount': i.amount,
            'status': i.status,
            'service_description': i.service_description
        } for i in invoices])

    # Return HTML
    return render_template('invoices/list.html', invoices=invoices)


@bp.route('/create', methods=['GET', 'POST'])
def create_invoice():
    """Create a new invoice."""
    if request.method == 'POST':
        if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
            # Handle JSON data
            data = request.get_json()

            # Check if customer exists
            customer_id = data.get('customer_id')
            customer = db.session.get(Customer, customer_id)
            if customer is None:
                abort(404)

            # Parse dates
            service_date = None
            if data.get('service_date'):
                service_date = datetime.fromisoformat(data.get('service_date'))

            due_date = None
            if data.get('due_date'):
                due_date = datetime.fromisoformat(data.get('due_date'))

            # Create invoice
            invoice = Invoice(
                customer_id=customer_id,
                service_date=service_date,
                due_date=due_date,
                amount=data.get('amount'),
                status=data.get('status', 'draft'),
                service_description=data.get('service_description')
            )

            db.session.add(invoice)
            db.session.commit()

            # Return JSON response
            result = {
                'id': invoice.id,
                'customer_id': invoice.customer_id,
                'service_date': invoice.service_date.isoformat(),
                'issue_date': invoice.issue_date.isoformat(),
                'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
                'amount': invoice.amount,
                'status': invoice.status,
                'service_description': invoice.service_description
            }
            return jsonify(result), 201
        else:
            # Handle form data
            customer_id = request.form.get('customer_id')
            customer = db.session.get(Customer, customer_id)
            if customer is None:
                abort(404)

            # Parse dates
            service_date = None
            if request.form.get('service_date'):
                service_date = datetime.strptime(request.form.get('service_date'), '%Y-%m-%d')

            due_date = None
            if request.form.get('due_date'):
                due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%d')

            # Create invoice
            invoice = Invoice(
                customer_id=customer_id,
                service_date=service_date,
                due_date=due_date,
                amount=float(request.form.get('amount')),
                status=request.form.get('status', 'draft'),
                service_description=request.form.get('service_description')
            )

            db.session.add(invoice)
            db.session.commit()

            # Redirect to invoice list
            return render_template('invoices/list.html'), 201

    # Get customers for dropdown
    customers = Customer.query.all()

    # Return the create form for GET requests
    return render_template('invoices/create.html', customers=customers)


@bp.route('/<int:invoice_id>', methods=['GET'])
def view_invoice(invoice_id):
    """View a specific invoice."""
    invoice = db.session.get(Invoice, invoice_id)
    if invoice is None:
        abort(404)

    if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
        # Return JSON if requested
        result = {
            'id': invoice.id,
            'customer_id': invoice.customer_id,
            'customer_name': invoice.customer.name,
            'service_date': invoice.service_date.isoformat(),
            'issue_date': invoice.issue_date.isoformat(),
            'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
            'amount': invoice.amount,
            'status': invoice.status,
            'service_description': invoice.service_description
        }
        return jsonify(result)

    # Return HTML view
    return render_template('invoices/view.html', invoice=invoice)


@bp.route('/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """Update a specific invoice."""
    invoice = db.session.get(Invoice, invoice_id)
    if invoice is None:
        abort(404)

    if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
        data = request.get_json()

        # Update invoice fields
        if 'customer_id' in data:
            # Verify customer exists
            customer = db.session.get(Customer, data['customer_id'])
            if customer is None:
                abort(404)
            invoice.customer_id = data['customer_id']

        # Update dates if provided
        if 'service_date' in data:
            invoice.service_date = datetime.fromisoformat(data['service_date'])

        if 'due_date' in data:
            invoice.due_date = datetime.fromisoformat(data['due_date'])

        # Update other fields
        if 'amount' in data:
            invoice.amount = data['amount']

        if 'status' in data:
            invoice.status = data['status']

        if 'service_description' in data:
            invoice.service_description = data['service_description']

        db.session.commit()

        # Return updated invoice
        result = {
            'id': invoice.id,
            'customer_id': invoice.customer_id,
            'service_date': invoice.service_date.isoformat(),
            'issue_date': invoice.issue_date.isoformat(),
            'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
            'amount': invoice.amount,
            'status': invoice.status,
            'service_description': invoice.service_description
        }
        return jsonify(result)

    # Handle form data (not implemented in this example)
    abort(415)


@bp.route('/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """Delete a specific invoice."""
    invoice = db.session.get(Invoice, invoice_id)
    if invoice is None:
        abort(404)

    db.session.delete(invoice)
    db.session.commit()

    # Return 204 No Content
    return '', 204
