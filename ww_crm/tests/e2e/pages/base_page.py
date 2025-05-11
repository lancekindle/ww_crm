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

    def submit_form(
        self,
        form_selector: str,
        submit_button_selector: str = None,
        expected_redirect: str = None,
        timeout: int = 10000,
    ):
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
            logger.info(f"DEBUG: Inside submit_form method. Form: {form_selector}, Button: {submit_button_selector}")
            form = self.page.locator(form_selector)

            # Make sure form exists
            if form.count() == 0:
                logger.error(f"DEBUG: Form not found: {form_selector}")
                return False

            logger.info(f"DEBUG: Form found. Count: {form.count()}")

            # Log the form method and action
            form_method = form.evaluate("form => form.method")
            form_action = form.evaluate("form => form.action")
            logger.info(f"DEBUG: Form method: {form_method}, Form action: {form_action}")

            # Use context manager to watch for navigation
            if expected_redirect:
                expected_url = f"{self.base_url}{expected_redirect}"
                logger.debug(f"DEBUG: Expecting navigation to: {expected_url}")
                logger.debug(f"DEBUG: Current URL before submit: {self.page.url}")

                # Try a more robust approach by using JavaScript to submit the form
                try:
                    # Set longer timeout for navigation
                    with self.page.expect_navigation(timeout=timeout) as navigation_info:
                        if submit_button_selector:
                            # Try multiple approaches to handle the submit button
                            try:
                                logger.info(f"DEBUG: Attempting to click submit button: {submit_button_selector}")
                                submit_button = self.page.locator(submit_button_selector)

                                if submit_button.count() > 0:
                                    logger.info(f"DEBUG: Submit button found. Count: {submit_button.count()}")

                                    # First try clicking it directly
                                    logger.info(f"DEBUG: Clicking submit button via Playwright click")
                                    submit_button.click(timeout=5000)
                                else:
                                    logger.warning(f"DEBUG: Submit button not found: {submit_button_selector}")
                                    # If button not found, try form submission directly
                                    logger.info(f"DEBUG: Using JavaScript to submit form")
                                    form.evaluate("form => { console.log('Submitting form via JS'); form.submit(); }")
                            except Exception as e:
                                logger.warning(
                                    f"DEBUG: Failed to click submit button: {str(e)}. Trying JavaScript form submission."
                                )
                                # Different approach with more logging
                                js_result = self.page.evaluate(
                                    f"""() => {{
                                    const form = document.querySelector('{form_selector}');
                                    if (!form) {{ return "Form not found"; }}
                                    console.log('Form found in JS, submitting...');
                                    form.submit();
                                    return "Form submitted via JS";
                                }}"""
                                )
                                logger.info(f"DEBUG: JavaScript submit result: {js_result}")
                        else:
                            logger.info(f"DEBUG: No submit button provided, submitting form via JavaScript")
                            form.evaluate("form => form.submit()")

                    # After form submission, check navigation
                    logger.info(f"DEBUG: Navigation attempt completed")
                    if navigation_info.value:
                        actual_url = navigation_info.value.url
                        logger.info(f"DEBUG: Navigated to: {actual_url}")

                        if actual_url == expected_url:
                            logger.info(f"DEBUG: Successfully navigated to expected URL: {expected_url}")
                            return True
                        else:
                            logger.warning(
                                f"DEBUG: Navigation occurred but to wrong URL. Expected: {expected_url}, Got: {actual_url}"
                            )
                    else:
                        logger.warning(f"DEBUG: No navigation occurred")

                except Exception as navigation_error:
                    logger.error(f"DEBUG: Navigation error: {str(navigation_error)}")

                # Check current URL in case navigation happened but we missed it
                actual_url = self.page.url
                logger.info(f"DEBUG: Current URL after submit attempt: {actual_url}")

                if actual_url == expected_url:
                    logger.info(f"DEBUG: URL matches expected - we're on the right page: {expected_url}")
                    return True
                else:
                    logger.warning(f"DEBUG: URLs don't match. Expected: {expected_url}, Got: {actual_url}")

                    # Check for form validation errors with various possible selectors
                    error_selectors = [
                        ".error-message",
                        ".field-error",
                        ".validation-error",
                        ".alert",
                        ".form-error",
                        "#error-message",
                    ]

                    for selector in error_selectors:
                        validation_errors = self.page.locator(selector).all()
                        if validation_errors:
                            logger.warning(f"DEBUG: Found {len(validation_errors)} errors with selector '{selector}':")
                            for error in validation_errors:
                                logger.warning(f"DEBUG: - {error.text_content()}")

                    # Check HTML response for clues
                    try:
                        page_html = self.page.content()
                        if "error" in page_html.lower():
                            logger.warning("DEBUG: Found 'error' in page HTML content")
                    except Exception as e:
                        logger.error(f"DEBUG: Error checking page content: {str(e)}")

                    return False
            else:
                # No navigation expectation, just submit the form
                logger.info("DEBUG: No expected redirect, just submitting form")
                if submit_button_selector:
                    try:
                        self.click_element(submit_button_selector, "Form submit button")
                        logger.info("DEBUG: Clicked submit button without navigation expectation")
                    except Exception as e:
                        logger.warning(f"DEBUG: Failed to click submit button: {e}. Trying direct form submission.")
                        result = form.evaluate("form => { form.submit(); return 'Submitted'; }")
                        logger.info(f"DEBUG: Form submission result: {result}")
                else:
                    result = form.evaluate("form => { form.submit(); return 'Submitted'; }")
                    logger.info(f"DEBUG: Direct form submission result: {result}")
                return True

        except Exception as e:
            logger.error(f"DEBUG: Form submission failed with exception: {str(e)}")
            return False

    def fill_form_fields(self, field_data: dict):
        """
        Fill multiple form fields at once.

        Args:
            field_data: Dictionary mapping CSS selectors to values
        """
        logger.info(f"DEBUG: Starting to fill {len(field_data)} form fields")

        for selector, value in field_data.items():
            try:
                logger.info(f"DEBUG: Filling field {selector} with value: {value}")

                # Check if the element exists before attempting to fill
                element = self.page.locator(selector)
                if element.count() == 0:
                    logger.error(f"DEBUG: Element {selector} not found - cannot fill")
                    continue

                # Log element details
                tag_name = element.evaluate("el => el.tagName.toLowerCase()")
                element_type = element.get_attribute("type") if tag_name == "input" else tag_name
                logger.info(
                    f"DEBUG: Element {selector} is a {tag_name}{' of type ' + element_type if element_type and tag_name == 'input' else ''}"
                )

                # Handle different element types
                if isinstance(value, bool):
                    if value:
                        logger.info(f"DEBUG: Checking checkbox {selector}")
                        self.page.check(selector)
                    else:
                        logger.info(f"DEBUG: Unchecking checkbox {selector}")
                        self.page.uncheck(selector)
                elif self.is_select_element(selector):
                    logger.info(f"DEBUG: Selecting option {value} from dropdown {selector}")
                    # Check if option exists in the select
                    options = element.evaluate("el => Array.from(el.options).map(o => o.value)")
                    logger.info(f"DEBUG: Available options for {selector}: {options}")

                    if str(value) in options:
                        self.select_option(selector, str(value))
                    else:
                        logger.error(f"DEBUG: Option value '{value}' not found in select element options")
                else:
                    logger.info(f"DEBUG: Filling input {selector} with text: {value}")
                    self.fill_input(selector, str(value))

                # Verify the value was set correctly
                try:
                    actual_value = None
                    if tag_name == "select":
                        actual_value = element.evaluate("el => el.value")
                    elif tag_name == "input" and element_type == "checkbox":
                        actual_value = element.is_checked()
                    else:
                        actual_value = element.input_value()

                    logger.info(f"DEBUG: After filling, field {selector} has value: {actual_value}")

                    if str(actual_value) != str(value) and not (isinstance(value, bool) and actual_value == value):
                        logger.warning(
                            f"DEBUG: Field value mismatch for {selector}. Expected: {value}, Actual: {actual_value}"
                        )
                except Exception as verify_error:
                    logger.error(f"DEBUG: Error verifying field value: {str(verify_error)}")

            except Exception as e:
                logger.error(f"DEBUG: Error filling field {selector}: {str(e)}")

        logger.info("DEBUG: Finished filling form fields")

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

    def submit_form_with_retry(
        self,
        form_selector: str,
        submit_button_selector: str = None,
        expected_redirect: str = None,
        max_retries: int = 3,
    ):
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
        logger.info(
            f"DEBUG: Starting form submission with retry. Form: {form_selector}, Button: {submit_button_selector}"
        )

        # Log the form's action attribute to debug
        try:
            form_action = self.page.locator(form_selector).evaluate("form => form.action")
            logger.info(f"DEBUG: Form action URL: {form_action}")
        except Exception as e:
            logger.error(f"DEBUG: Could not get form action: {str(e)}")

        # Log submit button details
        if submit_button_selector:
            try:
                button_exists = self.page.locator(submit_button_selector).count() > 0
                logger.info(f"DEBUG: Submit button exists: {button_exists}")
                if button_exists:
                    button_text = self.page.locator(submit_button_selector).text_content()
                    logger.info(f"DEBUG: Submit button text: {button_text}")
            except Exception as e:
                logger.error(f"DEBUG: Error checking submit button: {str(e)}")

        for attempt in range(max_retries):
            logger.info(f"DEBUG: Form submission attempt {attempt + 1} of {max_retries}")

            # Log the form content before submission
            try:
                form_html = self.page.locator(form_selector).evaluate("form => form.outerHTML")
                logger.info(f"DEBUG: Form HTML before submission:\n{form_html}")

                # Log form field values
                form_fields = self.page.locator(
                    f"{form_selector} input, {form_selector} select, {form_selector} textarea"
                ).all()
                logger.info(f"DEBUG: Found {len(form_fields)} form fields")
                for field in form_fields:
                    try:
                        field_name = field.get_attribute("name")
                        field_id = field.get_attribute("id")
                        field_type = field.get_attribute("type")

                        value = None
                        if field_type == "checkbox" or field_type == "radio":
                            value = field.is_checked()
                        else:
                            value = field.input_value()

                        logger.info(f"DEBUG: Field {field_name} (id: {field_id}, type: {field_type}): '{value}'")
                    except Exception as e:
                        logger.error(f"DEBUG: Error getting field info: {str(e)}")
            except Exception as e:
                logger.error(f"DEBUG: Error logging form content: {str(e)}")

            success = self.submit_form(form_selector, submit_button_selector, expected_redirect)

            if success:
                logger.info("DEBUG: Form submission successful!")
                return True

            # If we're supposed to be redirected but we're not, let's check the current page
            if expected_redirect and attempt < max_retries - 1:
                logger.info(f"DEBUG: Retry attempt {attempt + 1}: Current URL: {self.page.url}")
                expected_url = f"{self.base_url}{expected_redirect}"
                logger.info(f"DEBUG: Expected URL: {expected_url}")

                # Check page content for clues about failure
                try:
                    logger.info("DEBUG: Page content after failed submission:")
                    page_content = self.page.content()
                    logger.info(f"DEBUG: Page title: {self.page.title()}")

                    # Look for various types of error messages
                    selectors = [
                        ".error-message",
                        ".field-error",
                        ".validation-error",
                        ".alert",
                        "#error-message",
                        ".form-error",
                    ]

                    for selector in selectors:
                        error_elements = self.page.locator(selector).all()
                        if error_elements:
                            logger.warning(f"DEBUG: Found {len(error_elements)} errors with selector '{selector}':")
                            for error in error_elements:
                                logger.warning(f"DEBUG: - {error.text_content()}")
                except Exception as e:
                    logger.error(f"DEBUG: Error checking page content: {str(e)}")

        logger.error("DEBUG: All form submission attempts failed")
        return False
