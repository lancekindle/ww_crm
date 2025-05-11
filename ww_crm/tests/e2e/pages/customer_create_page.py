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
        self.assert_element_visible(CustomerPageSelectors.CREATE_HEADING, "Create Customer heading")
        self.assert_element_visible(CustomerPageSelectors.CUSTOMER_FORM, "Customer form")

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
            "name": CustomerPageSelectors.NAME_INPUT,
            "phone": CustomerPageSelectors.PHONE_INPUT,
            "email": CustomerPageSelectors.EMAIL_INPUT,
            "address": CustomerPageSelectors.ADDRESS_INPUT,
            "building_type": CustomerPageSelectors.BUILDING_TYPE_SELECT,
            "window_count": CustomerPageSelectors.WINDOW_COUNT_INPUT,
            "notes": CustomerPageSelectors.NOTES_INPUT,
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
        self.click_element(CustomerPageSelectors.BTN_SAVE_CUSTOMER, "Save Customer button")

    def click_cancel_button(self):
        """Click the Cancel button."""
        logger.info("Clicking Cancel button")
        self.click_element(CustomerPageSelectors.BTN_CANCEL, "Cancel button")

    def create_customer(self, customer_data):
        """
        Create a new customer by filling the form and clicking save.
        Uses improved form submission with retry logic.

        Args:
            customer_data: Dictionary containing customer data

        Returns:
            tuple: (success, customer_name) - Whether the submission succeeded and the customer name
        """
        logger.info(f"DEBUG: Creating new customer: {customer_data.get('name', 'Unknown')}")
        logger.info(f"DEBUG: Customer data: {customer_data}")

        # Ensure we're on the create page
        current_url = self.page.url
        create_url = f"{self.base_url}/customers/create"
        if not current_url.startswith(create_url):
            logger.info(f"DEBUG: Not on create page. Current URL: {current_url}, Expected: {create_url}")
            self.navigate()
            logger.info(f"DEBUG: Navigated to create page: {self.page.url}")

        # Fill the form with extra logging
        logger.info("DEBUG: Starting to fill customer form")
        filled_fields = self.fill_customer_form(customer_data)
        logger.info(f"DEBUG: Filled {len(filled_fields)} form fields")

        # Try a more direct approach to submit the form to avoid JavaScript hanging
        logger.info("DEBUG: Attempting to submit customer form - direct approach")
        success = False

        try:
            # First, try just clicking the submit button directly
            button = self.page.locator(CustomerPageSelectors.BTN_SAVE_CUSTOMER)

            if button.count() > 0:
                logger.info("DEBUG: Submit button found, clicking it directly")

                # Set up navigation expectation
                expected_url = f"{self.base_url}/customers"

                try:
                    with self.page.expect_navigation(timeout=5000) as nav_info:
                        button.click(timeout=3000)

                    # Check if navigation succeeded
                    if nav_info.value and nav_info.value.url == expected_url:
                        logger.info(f"DEBUG: Successfully navigated to: {expected_url}")
                        success = True
                    else:
                        current_url = self.page.url

                        # Double check we got to the right place
                        if current_url == expected_url:
                            logger.info(f"DEBUG: Current URL matches expected: {expected_url}")
                            success = True
                        else:
                            logger.warning(
                                f"DEBUG: Navigation didn't match. Expected: {expected_url}, Got: {current_url}"
                            )
                except Exception as nav_error:
                    logger.error(f"DEBUG: Navigation error: {str(nav_error)}")

                    # Check if we're on the right page anyway
                    if self.page.url == expected_url:
                        logger.info(f"DEBUG: Despite error, we're on the expected URL: {expected_url}")
                        success = True
            else:
                logger.warning("DEBUG: Submit button not found")
        except Exception as e:
            logger.error(f"DEBUG: Error during direct form submission: {str(e)}")

        # If direct approach failed, try a fallback method
        if not success:
            logger.info("DEBUG: Direct approach failed, trying fallback method")
            try:
                # Use a simple JavaScript form submission approach
                form_selector = CustomerPageSelectors.CUSTOMER_FORM
                expected_url = f"{self.base_url}/customers"

                # Try with a minimal JavaScript approach less likely to hang
                try:
                    with self.page.expect_navigation(timeout=5000) as nav_info:
                        # Use a very simple JavaScript submission
                        self.page.evaluate(
                            f"""() => {{
                            const form = document.querySelector('{form_selector}');
                            if (form) form.submit();
                        }}"""
                        )

                    # Check navigation results
                    if nav_info.value and nav_info.value.url == expected_url:
                        logger.info(f"DEBUG: Fallback method navigated to: {expected_url}")
                        success = True
                    else:
                        # Double check current URL
                        if self.page.url == expected_url:
                            logger.info(f"DEBUG: Fallback succeeded! Current URL: {self.page.url}")
                            success = True
                except Exception as js_error:
                    logger.error(f"DEBUG: Fallback JavaScript error: {str(js_error)}")

                    # Check URL anyway
                    if self.page.url == expected_url:
                        logger.info(f"DEBUG: Despite error, fallback succeeded. Current URL: {self.page.url}")
                        success = True
            except Exception as fallback_error:
                logger.error(f"DEBUG: Fallback method failed: {str(fallback_error)}")

        if success:
            logger.info(f"DEBUG: Customer creation succeeded for {customer_data.get('name', 'Unknown')}")
        else:
            logger.error(f"DEBUG: Customer creation failed for {customer_data.get('name', 'Unknown')}")

            # Check if we're still on the create page or somewhere else
            current_url = self.page.url
            logger.info(f"DEBUG: After failed submission, current URL: {current_url}")

            # Check page title for more context
            page_title = self.page.title()
            logger.info(f"DEBUG: Current page title: {page_title}")

            # Check for any visible error messages on the page
            try:
                error_messages = self.page.locator(".error-message, .alert, .validation-error").all()
                if error_messages:
                    logger.error("DEBUG: Found error messages on page:")
                    for msg in error_messages:
                        logger.error(f"DEBUG: Error: {msg.text_content()}")
            except Exception as e:
                logger.error(f"DEBUG: Error checking for error messages: {str(e)}")

        return success, customer_data.get("name", "Unknown")
