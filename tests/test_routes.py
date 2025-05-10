import json
import pytest
from flask import url_for


class TestCustomerRoutes:
    """Tests for customer-related routes."""

    def test_list_customers(self, client):
        """Test the customer listing route."""
        response = client.get('/customers')
        assert response.status_code == 200

    def test_create_customer(self, client):
        """Test the customer creation route."""
        data = {
            'name': 'New Customer',
            'phone': '555-987-6543',
            'email': 'new@example.com',
            'address': '789 New St, Newtown',
            'building_type': 'commercial',
            'window_count': 20,
            'notes': 'New customer notes'
        }

        response = client.post(
            '/customers/create',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 201
        assert b'New Customer' in response.data

    def test_view_customer(self, client, sample_customer):
        """Test viewing a specific customer."""
        response = client.get(f'/customers/{sample_customer.id}')
        assert response.status_code == 200
        assert sample_customer.name.encode() in response.data

    def test_update_customer(self, client, sample_customer):
        """Test updating a customer."""
        update_data = {
            'name': 'Updated Customer',
            'phone': sample_customer.phone,
            'email': sample_customer.email,
            'address': sample_customer.address,
            'building_type': sample_customer.building_type,
            'window_count': 15,  # Updated window count
            'notes': 'Updated notes'
        }

        response = client.put(
            f'/customers/{sample_customer.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert b'Updated Customer' in response.data
        assert b'Updated notes' in response.data

    def test_delete_customer(self, client, sample_customer):
        """Test deleting a customer."""
        response = client.delete(f'/customers/{sample_customer.id}')
        assert response.status_code == 204

        # Verify customer is gone
        verify_response = client.get(f'/customers/{sample_customer.id}')
        assert verify_response.status_code == 404


class TestInvoiceRoutes:
    """Tests for invoice-related routes."""

    def test_list_invoices(self, client):
        """Test listing all invoices."""
        response = client.get('/invoices')
        assert response.status_code == 200

    def test_create_invoice(self, client, sample_customer):
        """Test creating a new invoice."""
        data = {
            'customer_id': sample_customer.id,
            'service_date': '2025-05-10',
            'due_date': '2025-06-10',
            'amount': 180.75,
            'status': 'draft',
            'service_description': 'Standard window cleaning'
        }

        response = client.post(
            '/invoices/create',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 201
        assert b'Standard window cleaning' in response.data

    def test_view_invoice(self, client, sample_invoice):
        """Test viewing a specific invoice."""
        response = client.get(f'/invoices/{sample_invoice.id}')
        assert response.status_code == 200
        assert sample_invoice.service_description.encode() in response.data

    def test_update_invoice(self, client, sample_invoice):
        """Test updating an invoice."""
        update_data = {
            'customer_id': sample_invoice.customer_id,
            'service_date': sample_invoice.service_date.isoformat(),
            'due_date': sample_invoice.due_date.isoformat(),
            'amount': 195.50,  # Updated amount
            'status': 'sent',  # Updated status
            'service_description': 'Updated service description'
        }

        response = client.put(
            f'/invoices/{sample_invoice.id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert b'Updated service description' in response.data
        assert b'sent' in response.data

    def test_delete_invoice(self, client, sample_invoice):
        """Test deleting an invoice."""
        response = client.delete(f'/invoices/{sample_invoice.id}')
        assert response.status_code == 204

        # Verify invoice is gone
        verify_response = client.get(f'/invoices/{sample_invoice.id}')
        assert verify_response.status_code == 404

    def test_list_customer_invoices(self, client, sample_customer, sample_invoice):
        """Test listing invoices for a specific customer."""
        response = client.get(f'/customers/{sample_customer.id}/invoices')
        assert response.status_code == 200
        assert sample_invoice.service_description.encode() in response.data
