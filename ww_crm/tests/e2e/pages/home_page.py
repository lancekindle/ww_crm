"""
Home page object for UI testing.
"""

from playwright.sync_api import Page
from .base_page import NavigablePage
from .selectors import HomePageSelectors


class HomePage(NavigablePage):
    """
    Page object for the home page.

    This class follows the Single Responsibility Principle by focusing
    only on home page specific interactions and verifications.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize the home page object.

        Args:
            page: The Playwright page object
            base_url: The base URL of the application
        """
        super().__init__(page, base_url)

    def navigate(self):
        """Navigate to the home page."""
        self.navigate_to("/")

    def assert_page_loaded(self):
        """Assert that the home page is loaded correctly."""
        # Check page title
        expect_title = "Home - Window Wash CRM"
        actual_title = self.page.title()
        assert actual_title == expect_title, f"Expected title '{expect_title}', got '{actual_title}'"

        # Check content elements
        self.assert_element_visible(HomePageSelectors.WELCOME_HEADING, "Welcome heading")
        self.assert_element_visible(HomePageSelectors.WELCOME_MESSAGE, "Welcome message")
