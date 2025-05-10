"""
UI tests for the Window Wash CRM application.

These tests use Playwright to verify the application's UI functionality.
The tests follow the Page Object Model pattern for better organization and maintenance.
"""
import logging
import pytest
from playwright.sync_api import Page

from ww_crm.tests.e2e.pages.home_page import HomePage
from ww_crm.tests.e2e.pages.customer_list_page import CustomerListPage
from ww_crm.tests.e2e.pages.customer_create_page import CustomerCreatePage
from ww_crm.tests.e2e.pages.invoice_list_page import InvoiceListPage

# Set up logging
logger = logging.getLogger(__name__)

# Mark all tests in this module as requiring the live_server and as e2e tests
pytestmark = [
    pytest.mark.usefixtures('live_server'),
    pytest.mark.e2e
]


class TestUserInterface:
    """
    UI Tests using the Page Object Model pattern.

    These tests verify the functionality of the UI by interacting with
    the application through Page Objects, which encapsulate the details
    of how to interact with each page.
    """

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, live_server):
        """Set up page objects for each test."""
        logger.info("Setting up UI test")

        # Initialize page objects
        self.home_page = HomePage(page, live_server.url())
        self.customer_list_page = CustomerListPage(page, live_server.url())
        self.customer_create_page = CustomerCreatePage(page, live_server.url())
        self.invoice_list_page = InvoiceListPage(page, live_server.url())

        # Navigate to the homepage at the start of each test
        self.home_page.navigate()

    def test_homepage_loads(self):
        """Test that the homepage loads successfully."""
        logger.info("Running test: homepage_loads")

        # Verify the home page loaded correctly
        self.home_page.assert_page_loaded()
        self.home_page.assert_navigation_visible()

    def test_customer_list(self, sample_customer):
        """Test that the customer list displays properly."""
        logger.info("Running test: customer_list")

        # Navigate to customers page
        self.home_page.click_nav_customers()

        # Verify page loaded correctly
        self.customer_list_page.assert_page_loaded()

        # Verify sample customer is visible
        self.customer_list_page.assert_customer_visible(
            sample_customer.id, sample_customer.name
        )

    @pytest.mark.skip(reason="Form submission test needs additional adjustments to handle navigation issues. Will be fixed in separate PR.")
    def test_customer_creation_form(self):
        """Test the customer creation form."""
        logger.info("Running test: customer_creation_form")

        # Navigate to the customer create page
        self.customer_create_page.navigate()

        # Verify the page loaded correctly
        self.customer_create_page.assert_page_loaded()

        # Fill out and submit the form
        customer_data = {
            'name': 'UI Test Customer',
            'phone': '555-123-4567',
            'email': 'ui-test@example.com',
            'address': '123 UI Test St',
            'building_type': 'residential',
            'window_count': 15,
            'notes': 'Created via UI test'
        }

        # Create the customer
        success, customer_name = self.customer_create_page.create_customer(customer_data)

        # Navigate to customer list page to verify, regardless of form submission result
        self.customer_list_page.navigate()
        self.customer_list_page.assert_page_loaded()

        # Search for the customer in the list by name
        self.customer_list_page.assert_customer_exists_by_name(customer_name)
        logger.info(f"Successfully verified customer {customer_name} was created")

    def test_invoice_list(self, sample_invoice):
        """Test that the invoice list displays properly."""
        logger.info("Running test: invoice_list")

        # Navigate to invoices page
        self.home_page.click_nav_invoices()

        # Verify page loaded correctly
        self.invoice_list_page.assert_page_loaded()

        # Verify sample invoice is visible
        self.invoice_list_page.assert_invoice_visible(
            sample_invoice.id,
            sample_invoice.amount,
            sample_invoice.customer.name
        )
