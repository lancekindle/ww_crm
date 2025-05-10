"""
Customer list page object for UI testing.
"""
import logging
from playwright.sync_api import Page
from .base_page import NavigablePage
from .selectors import CustomerPageSelectors

logger = logging.getLogger(__name__)


class CustomerListPage(NavigablePage):
    """
    Page object for the customer list page.

    This class follows the Single Responsibility Principle by focusing
    only on customer list page specific interactions and verifications.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize the customer list page object.

        Args:
            page: The Playwright page object
            base_url: The base URL of the application
        """
        super().__init__(page, base_url)

    def navigate(self):
        """Navigate to the customer list page."""
        logger.info("Navigating to customer list page")
        self.navigate_to("/customers")

    def assert_page_loaded(self):
        """Assert that the customer list page is loaded correctly."""
        logger.debug("Verifying customer list page loaded")
        self.assert_url("/customers")

        # Assert customer heading or any other reliable element is present
        try:
            self.assert_element_visible(
                CustomerPageSelectors.LIST_HEADING,
                "Customers heading"
            )
        except AssertionError:
            # Fall back to checking if the customers table is visible
            logger.warning("Could not find customers heading, checking for customer table instead")
            self.assert_element_visible(
                CustomerPageSelectors.LIST_TABLE,
                "Customers table"
            )

    def click_add_customer(self):
        """Click the Add Customer button."""
        logger.info("Clicking Add Customer button")
        self.assert_element_visible(
            CustomerPageSelectors.BTN_ADD_CUSTOMER,
            "Add Customer button"
        )
        self.click_element(
            CustomerPageSelectors.BTN_ADD_CUSTOMER,
            "Add Customer button"
        )

    def assert_customer_table_visible(self):
        """Assert that the customers table is visible."""
        logger.debug("Verifying customer table is visible")
        self.assert_element_visible(
            CustomerPageSelectors.LIST_TABLE,
            "Customers table"
        )

    def assert_customer_visible(self, customer_id, expected_name=None):
        """
        Assert that a customer is visible in the table.

        Args:
            customer_id: The ID of the customer
            expected_name: The expected name of the customer (optional)
        """
        logger.debug(f"Verifying customer {customer_id} is visible")
        self.assert_customer_table_visible()

        customer_row_selector = CustomerPageSelectors.customer_row(customer_id)
        self.assert_element_visible(customer_row_selector, f"Customer row {customer_id}")

        if expected_name:
            customer_name_selector = CustomerPageSelectors.customer_name_cell(customer_id)
            self.assert_element_contains_text(
                customer_name_selector,
                expected_name,
                f"Customer name for ID {customer_id}"
            )

    def assert_customer_exists_by_name(self, name):
        """
        Assert that a customer with the given name exists in the table.

        Args:
            name: The name of the customer to check for
        """
        logger.debug(f"Verifying customer with name '{name}' exists")
        self.assert_customer_table_visible()
        self.assert_element_contains_text(
            CustomerPageSelectors.LIST_TABLE,
            name,
            f"Customer with name '{name}'"
        )

    def click_view_customer(self, customer_id):
        """
        Click the View button for a specific customer.

        Args:
            customer_id: The ID of the customer
        """
        logger.info(f"Clicking view button for customer {customer_id}")
        selector = CustomerPageSelectors.btn_view_customer(customer_id)
        self.click_element(selector, f"View button for customer {customer_id}")

    def click_delete_customer(self, customer_id):
        """
        Click the Delete button for a specific customer.

        Args:
            customer_id: The ID of the customer
        """
        logger.info(f"Clicking delete button for customer {customer_id}")
        selector = CustomerPageSelectors.btn_delete_customer(customer_id)
        self.click_element(selector, f"Delete button for customer {customer_id}")
