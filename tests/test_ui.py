import pytest
from playwright.sync_api import Page, expect
import multiprocessing
import time
import os
import sys
from window_wash_crm.app import app

# Global server process
server_process = None


def setup_module():
    """Start the Flask server for UI testing."""
    global server_process

    # Start Flask in a separate process
    server_process = multiprocessing.Process(
        target=lambda: app.run(port=5000, debug=False)
    )
    server_process.start()

    # Give the server a moment to start
    time.sleep(2)


def teardown_module():
    """Tear down the Flask server after testing."""
    global server_process
    if server_process:
        server_process.terminate()
        server_process.join()


# Skip UI tests if running in CI environment
run_ui_tests = not os.environ.get('CI', False)
skip_ui_tests = pytest.mark.skipif(
    not run_ui_tests,
    reason="UI tests are disabled in CI environment"
)


@skip_ui_tests
class TestUserInterface:
    """Tests for the UI/frontend components."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Set up the page for each test."""
        # Navigate to the homepage
        page.goto("http://localhost:5000")

    def test_homepage_loads(self, page: Page):
        """Test that the homepage loads successfully."""
        # Check that we have a title
        expect(page).to_have_title("Window Wash CRM")

        # Check that the main navigation is present
        nav = page.locator("nav")
        expect(nav).to_be_visible()

        # Check for customer and invoice links
        expect(page.locator("text=Customers")).to_be_visible()
        expect(page.locator("text=Invoices")).to_be_visible()

    def test_customer_list(self, page: Page, sample_customer):
        """Test that the customer list displays properly."""
        # Navigate to customers page
        page.click("text=Customers")

        # Check that we're on the customer list page
        expect(page).to_have_url("http://localhost:5000/customers")

        # Check for our sample customer
        expect(page.locator(f"text={sample_customer.name}")).to_be_visible()

    def test_customer_creation_form(self, page: Page):
        """Test the customer creation form."""
        # Navigate to customers page
        page.click("text=Customers")

        # Click on "Add Customer"
        page.click("text=Add Customer")

        # Check that the form is shown
        form = page.locator("form")
        expect(form).to_be_visible()

        # Fill and submit the form
        page.fill("input[name=name]", "UI Test Customer")
        page.fill("input[name=phone]", "555-123-4567")
        page.fill("input[name=email]", "ui-test@example.com")
        page.fill("input[name=address]", "123 UI Test St")
        page.select_option("select[name=building_type]", "residential")
        page.fill("input[name=window_count]", "15")
        page.fill("textarea[name=notes]", "Created via UI test")

        page.click("button[type=submit]")

        # Check that we're redirected back to the customer list
        expect(page).to_have_url("http://localhost:5000/customers")

        # Check that our new customer is in the list
        expect(page.locator("text=UI Test Customer")).to_be_visible()

    def test_invoice_list(self, page: Page, sample_invoice):
        """Test that the invoice list displays properly."""
        # Navigate to invoices page
        page.click("text=Invoices")

        # Check that we're on the invoice list page
        expect(page).to_have_url("http://localhost:5000/invoices")

        # Check for our sample invoice
        customer_name = sample_invoice.customer.name
        expect(page.locator(f"text={customer_name}")).to_be_visible()

        # Format the amount with dollar sign and check
        amount_text = f"${sample_invoice.amount:.2f}"
        expect(page.locator(f"text={amount_text}")).to_be_visible()
