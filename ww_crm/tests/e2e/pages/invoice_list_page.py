"""
Invoice list page object for UI testing.
"""
import logging
from playwright.sync_api import Page
from .base_page import NavigablePage
from .selectors import InvoicePageSelectors

logger = logging.getLogger(__name__)


class InvoiceListPage(NavigablePage):
    """
    Page object for the invoice list page.

    This class follows the Single Responsibility Principle by focusing
    only on invoice list page specific interactions and verifications.
    """

    def __init__(self, page: Page, base_url: str):
        """
        Initialize the invoice list page object.

        Args:
            page: The Playwright page object
            base_url: The base URL of the application
        """
        super().__init__(page, base_url)

    def navigate(self):
        """Navigate to the invoice list page."""
        logger.info("Navigating to invoice list page")
        self.navigate_to("/invoices")

    def assert_page_loaded(self):
        """Assert that the invoice list page is loaded correctly."""
        logger.debug("Verifying invoice list page loaded")
        self.assert_url("/invoices")
        self.assert_element_visible(
            InvoicePageSelectors.INVOICES_HEADING,
            "Invoices heading"
        )
        self.assert_element_visible(
            InvoicePageSelectors.INVOICES_TABLE,
            "Invoices table"
        )

    def click_add_invoice(self):
        """Click the Add Invoice button."""
        logger.info("Clicking Add Invoice button")
        self.click_element(
            InvoicePageSelectors.BTN_ADD_INVOICE,
            "Add Invoice button"
        )

    def assert_invoice_visible(self, invoice_id, expected_amount=None, expected_customer_name=None):
        """
        Assert that an invoice is visible in the table.

        Args:
            invoice_id: The ID of the invoice
            expected_amount: The expected amount of the invoice (optional)
            expected_customer_name: The expected customer name (optional)
        """
        logger.debug(f"Verifying invoice {invoice_id} is visible")
        invoice_row_selector = InvoicePageSelectors.invoice_row(invoice_id)
        self.assert_element_visible(invoice_row_selector, f"Invoice row {invoice_id}")

        if expected_amount:
            amount_text = f"${expected_amount:.2f}"
            amount_selector = InvoicePageSelectors.invoice_amount_cell(invoice_id)
            self.assert_element_contains_text(
                amount_selector,
                amount_text,
                f"Invoice amount for ID {invoice_id}"
            )

        if expected_customer_name:
            customer_selector = InvoicePageSelectors.invoice_customer_cell(invoice_id)
            self.assert_element_contains_text(
                customer_selector,
                expected_customer_name,
                f"Invoice customer name for ID {invoice_id}"
            )

    def click_view_invoice(self, invoice_id):
        """
        Click the View button for a specific invoice.

        Args:
            invoice_id: The ID of the invoice
        """
        logger.info(f"Clicking view button for invoice {invoice_id}")
        selector = InvoicePageSelectors.btn_view_invoice(invoice_id)
        self.click_element(selector, f"View button for invoice {invoice_id}")

    def click_delete_invoice(self, invoice_id):
        """
        Click the Delete button for a specific invoice.

        Args:
            invoice_id: The ID of the invoice
        """
        logger.info(f"Clicking delete button for invoice {invoice_id}")
        selector = InvoicePageSelectors.btn_delete_invoice(invoice_id)
        self.click_element(selector, f"Delete button for invoice {invoice_id}")

        # Since this triggers a confirmation dialog, we should wait a bit
        logger.debug("Waiting for confirmation dialog")
        self.page.wait_for_timeout(500)  # Short delay for dialog to appear
