"""
Base page object pattern implementation.

This module provides the foundation for the Page Object Model pattern,
following SOLID principles to create maintainable and extensible test code.
"""
import logging
from playwright.sync_api import Page, expect
from .selectors import NavigationSelectors

# Set up logging
logger = logging.getLogger(__name__)


class BasePage:
    """
    Base page class that provides common functionality for all page objects.

    This class follows the Single Responsibility Principle by focusing only
    on common page interactions and assertions.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize the base page object.

        Args:
            page: The Playwright page object
            base_url: The base URL of the application
        """
        self.page = page
        self.base_url = base_url

    def navigate_to(self, path: str = ""):
        """
        Navigate to a specific path in the application.

        Args:
            path: The path to navigate to relative to the base URL
        """
        url = f"{self.base_url}{path}"
        logger.info(f"Navigating to: {url}")
        self.page.goto(url)

    def assert_url(self, expected_path: str):
        """
        Assert that the current URL matches the expected path.

        Args:
            expected_path: The expected path (without the base URL)
        """
        expected_url = f"{self.base_url}{expected_path}"
        logger.debug(f"Asserting URL is: {expected_url}")
        expect(self.page).to_have_url(expected_url)

    def assert_element_visible(self, selector: str, description: str = None):
        """
        Assert that an element is visible with improved error messaging.

        Args:
            selector: The CSS selector for the element
            description: Optional human-readable description of the element
        """
        desc = description or selector
        logger.debug(f"Checking visibility of element: {desc}")
        try:
            expect(self.page.locator(selector)).to_be_visible()
        except Exception as e:
            logger.error(f"Element not visible: {desc} (selector: {selector})")
            raise AssertionError(f"Expected element '{desc}' to be visible") from e

    def assert_element_contains_text(self, selector: str, expected_text: str, description: str = None):
        """
        Assert that an element contains the expected text with improved error messaging.

        Args:
            selector: The CSS selector for the element
            expected_text: The expected text
            description: Optional human-readable description of the element
        """
        desc = description or selector
        logger.debug(f"Checking text content of element: {desc}")
        try:
            expect(self.page.locator(selector)).to_contain_text(expected_text)
        except Exception as e:
            logger.error(f"Element text mismatch: {desc} (selector: {selector})")
            logger.error(f"Expected to contain: '{expected_text}', got: '{self.page.locator(selector).text_content()}'")
            raise AssertionError(f"Expected element '{desc}' to contain text '{expected_text}'") from e

    def click_element(self, selector: str, description: str = None):
        """
        Click an element with improved error handling.

        Args:
            selector: The CSS selector for the element
            description: Optional human-readable description of the element
        """
        desc = description or selector
        logger.debug(f"Clicking element: {desc}")
        try:
            self.page.locator(selector).click()
        except Exception as e:
            logger.error(f"Failed to click element: {desc} (selector: {selector})")
            raise AssertionError(f"Failed to click element '{desc}'") from e

    def fill_input(self, selector: str, value: str, description: str = None):
        """
        Fill an input field with improved error handling.

        Args:
            selector: The CSS selector for the input
            value: The value to fill
            description: Optional human-readable description of the input
        """
        desc = description or selector
        logger.debug(f"Filling input {desc} with value: {value}")
        try:
            self.page.fill(selector, str(value))
        except Exception as e:
            logger.error(f"Failed to fill input: {desc} (selector: {selector})")
            raise AssertionError(f"Failed to fill input '{desc}'") from e

    def select_option(self, selector: str, value: str, description: str = None):
        """
        Select an option from a dropdown with improved error handling.

        Args:
            selector: The CSS selector for the select element
            value: The value to select
            description: Optional human-readable description of the dropdown
        """
        desc = description or selector
        logger.debug(f"Selecting option {value} from {desc}")
        try:
            self.page.select_option(selector, value)
        except Exception as e:
            logger.error(f"Failed to select option: {value} from {desc} (selector: {selector})")
            raise AssertionError(f"Failed to select option '{value}' from '{desc}'") from e


class NavigablePage(BasePage):
    """
    Extension of BasePage that adds navigation capabilities.

    This class follows the Open/Closed Principle by extending BasePage
    without modifying it, and the Interface Segregation Principle by
    keeping navigation capabilities separate.
    """

    def click_nav_home(self):
        """Click the Home navigation link."""
        self.click_element(NavigationSelectors.NAV_HOME, "Home navigation link")

    def click_nav_customers(self):
        """Click the Customers navigation link."""
        self.click_element(NavigationSelectors.NAV_CUSTOMERS, "Customers navigation link")

    def click_nav_invoices(self):
        """Click the Invoices navigation link."""
        self.click_element(NavigationSelectors.NAV_INVOICES, "Invoices navigation link")

    def assert_navigation_visible(self):
        """Assert that the main navigation is visible."""
        self.assert_element_visible(NavigationSelectors.MAIN_NAV, "Main navigation")
        self.assert_element_visible(NavigationSelectors.NAV_HOME, "Home navigation link")
        self.assert_element_visible(NavigationSelectors.NAV_CUSTOMERS, "Customers navigation link")
        self.assert_element_visible(NavigationSelectors.NAV_INVOICES, "Invoices navigation link")


class FormPage(BasePage):
    """
    Extension of BasePage that adds form handling capabilities.

    This class follows the Single Responsibility Principle by focusing
    only on form interactions, and the Interface Segregation Principle
    by keeping form capabilities separate.
    """

    def submit_form(self, form_selector: str, submit_button_selector: str = None,
                   expected_redirect: str = None, timeout: int = 5000):
        """
        Submit a form and handle navigation expectations.

        Args:
            form_selector: The CSS selector for the form
            submit_button_selector: Optional selector for a submit button to click
            expected_redirect: Optional path where we expect to be redirected after submission
            timeout: How long to wait for navigation in milliseconds

        Returns:
            bool: True if submission and expected navigation succeeded
        """
        try:
            logger.info(f"Submitting form: {form_selector}")
            form = self.page.locator(form_selector)

            # Make sure form exists
            if form.count() == 0:
                logger.error(f"Form not found: {form_selector}")
                return False

            # Use context manager to watch for navigation
            if expected_redirect:
                expected_url = f"{self.base_url}{expected_redirect}"
                logger.debug(f"Expecting navigation to: {expected_url}")

                with self.page.expect_navigation(timeout=timeout) as navigation_info:
                    if submit_button_selector:
                        try:
                            # Try the click approach first
                            self.click_element(submit_button_selector, "Form submit button")
                        except Exception as e:
                            logger.warning(f"Failed to click submit button: {e}. Trying direct form submission.")
                            form.evaluate("form => form.submit()")
                    else:
                        form.evaluate("form => form.submit()")

                # Check if navigation succeeded
                if navigation_info.value and navigation_info.value.url == expected_url:
                    logger.info(f"Successfully navigated to: {expected_url}")
                    return True
                else:
                    actual_url = self.page.url
                    logger.warning(f"Navigation didn't match expectation. Expected: {expected_url}, Got: {actual_url}")

                    # Check for form validation errors
                    validation_errors = self.page.locator(".error-message, .field-error, .validation-error").all()
                    if validation_errors:
                        logger.warning("Form has validation errors:")
                        for error in validation_errors:
                            logger.warning(f"- {error.text_content()}")

                    return False
            else:
                # No navigation expectation, just submit the form
                if submit_button_selector:
                    try:
                        self.click_element(submit_button_selector, "Form submit button")
                    except Exception as e:
                        logger.warning(f"Failed to click submit button: {e}. Trying direct form submission.")
                        form.evaluate("form => form.submit()")
                else:
                    form.evaluate("form => form.submit()")
                return True

        except Exception as e:
            logger.error(f"Form submission failed: {str(e)}")
            return False

    def fill_form_fields(self, field_data: dict):
        """
        Fill multiple form fields at once.

        Args:
            field_data: Dictionary mapping CSS selectors to values
        """
        for selector, value in field_data.items():
            if isinstance(value, bool):
                if value:
                    self.page.check(selector)
                else:
                    self.page.uncheck(selector)
            elif self.is_select_element(selector):
                self.select_option(selector, str(value))
            else:
                self.fill_input(selector, str(value))

    def is_select_element(self, selector: str):
        """
        Check if the element is a select element.

        Args:
            selector: The CSS selector for the element

        Returns:
            bool: True if the element is a select element, False otherwise
        """
        try:
            # Get the tag name of the element
            tag_name = self.page.locator(selector).evaluate("el => el.tagName.toLowerCase()")
            return tag_name == "select"
        except Exception:
            # If there's an error, fall back to checking the selector name
            return "select" in selector.lower()

    def submit_form_with_retry(self, form_selector: str, submit_button_selector: str = None,
                              expected_redirect: str = None, max_retries: int = 3):
        """
        Submit a form with retry logic for flaky form submissions.

        Args:
            form_selector: The CSS selector for the form
            submit_button_selector: Optional selector for a submit button to click
            expected_redirect: Optional path where we expect to be redirected after submission
            max_retries: Maximum number of retry attempts

        Returns:
            bool: True if submission and expected navigation succeeded
        """
        for attempt in range(max_retries):
            logger.info(f"Form submission attempt {attempt + 1} of {max_retries}")
            success = self.submit_form(form_selector, submit_button_selector, expected_redirect)

            if success:
                return True

            # If we're supposed to be redirected but we're not, let's check the current page
            if expected_redirect and attempt < max_retries - 1:
                logger.info(f"Retry attempt {attempt + 1}: Current URL: {self.page.url}")

                # If page has errors, log them
                error_messages = self.page.locator(".error-message").all()
                if error_messages:
                    for error in error_messages:
                        logger.warning(f"Form error: {error.text_content()}")

                # Wait a bit before retry
                self.page.wait_for_timeout(1000)

        return False
