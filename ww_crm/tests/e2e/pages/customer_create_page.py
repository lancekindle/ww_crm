"""
Customer create page object for UI testing.
"""
import logging
from playwright.sync_api import Page
from .base_page import NavigablePage, FormPage
from .selectors import CustomerPageSelectors

logger = logging.getLogger(__name__)


class CustomerCreatePage(NavigablePage, FormPage):
    """
    Page object for the customer creation page.

    This class follows the Single Responsibility Principle by focusing
    only on customer creation related interactions, and the Liskov
    Substitution Principle by properly inheriting from both NavigablePage
    and FormPage without breaking their contracts.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize the customer creation page object.

        Args:
            page: The Playwright page object
            base_url: The base URL of the application
        """
        super().__init__(page, base_url)

    def navigate(self):
        """Navigate to the customer creation page."""
        logger.info("Navigating to customer creation page")
        self.navigate_to("/customers/create")

    def assert_page_loaded(self):
        """Assert that the customer creation page is loaded correctly."""
        logger.debug("Verifying customer creation page loaded")
        self.assert_url("/customers/create")
        self.assert_element_visible(
            CustomerPageSelectors.CREATE_HEADING,
            "Create Customer heading"
        )
        self.assert_element_visible(
            CustomerPageSelectors.CUSTOMER_FORM,
            "Customer form"
        )

    def fill_customer_form(self, customer_data):
        """
        Fill the customer creation form with the provided data.

        Args:
            customer_data: Dictionary containing customer data with keys:
                          name, phone, email, address, building_type, window_count, notes

        Returns:
            Dictionary of field selectors and values that were filled
        """
        logger.info("Filling customer form")
        field_mapping = {
            'name': CustomerPageSelectors.NAME_INPUT,
            'phone': CustomerPageSelectors.PHONE_INPUT,
            'email': CustomerPageSelectors.EMAIL_INPUT,
            'address': CustomerPageSelectors.ADDRESS_INPUT,
            'building_type': CustomerPageSelectors.BUILDING_TYPE_SELECT,
            'window_count': CustomerPageSelectors.WINDOW_COUNT_INPUT,
            'notes': CustomerPageSelectors.NOTES_INPUT
        }

        # Create a dictionary of field selectors and values
        fields_to_fill = {}
        for field_name, selector in field_mapping.items():
            if field_name in customer_data:
                fields_to_fill[selector] = customer_data[field_name]
                logger.debug(f"Will fill {field_name} with: {customer_data[field_name]}")

        # Fill the form fields
        self.fill_form_fields(fields_to_fill)
        return fields_to_fill

    def click_save_button(self):
        """Click the Save Customer button."""
        logger.info("Clicking Save Customer button")
        self.click_element(
            CustomerPageSelectors.BTN_SAVE_CUSTOMER,
            "Save Customer button"
        )

    def click_cancel_button(self):
        """Click the Cancel button."""
        logger.info("Clicking Cancel button")
        self.click_element(
            CustomerPageSelectors.BTN_CANCEL,
            "Cancel button"
        )

    def create_customer(self, customer_data):
        """
        Create a new customer by filling the form and clicking save.
        Uses improved form submission with retry logic.

        Args:
            customer_data: Dictionary containing customer data

        Returns:
            tuple: (success, customer_name) - Whether the submission succeeded and the customer name
        """
        logger.info(f"Creating new customer: {customer_data.get('name', 'Unknown')}")

        # Fill the form
        self.fill_customer_form(customer_data)

        # Submit the form with retry logic
        success = self.submit_form_with_retry(
            CustomerPageSelectors.CUSTOMER_FORM,
            CustomerPageSelectors.BTN_SAVE_CUSTOMER,
            "/customers",
            max_retries=3
        )

        logger.info(f"Customer creation {'succeeded' if success else 'failed'}")
        return success, customer_data.get('name', 'Unknown')
