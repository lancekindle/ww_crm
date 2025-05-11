"""
UI tests for the Window Wash CRM application.

These tests use Playwright to verify the application's UI functionality.
The tests follow the Page Object Model pattern for better organization and maintenance.
"""
import logging
import pytest
from pytest import param
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

# Test data for parameterized tests
CUSTOMER_TEST_DATA = [
    param({
        'name': 'Residential Customer',
        'phone': '555-111-2222',
        'email': 'residential@example.com',
        'address': '123 Home St',
        'building_type': 'residential',
        'window_count': 10,
        'notes': 'Regular residential customer with few windows'
    }, id='residential_small'),
    param({
        'name': 'Residential Large',
        'phone': '555-222-3333',
        'email': 'large.home@example.com',
        'address': '456 Mansion Ave',
        'building_type': 'residential',
        'window_count': 30,
        'notes': 'Large residential with many windows'
    }, id='residential_large'),
    param({
        'name': 'Commercial Building',
        'phone': '555-333-4444',
        'email': 'commercial@example.com',
        'address': '789 Business Blvd',
        'building_type': 'commercial',
        'window_count': 50,
        'notes': 'Office building with many windows'
    }, id='commercial')
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
