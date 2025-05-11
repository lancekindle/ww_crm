"""
Selector registry for UI testing.

This module centralizes all CSS selectors used in page objects,
making them easier to maintain and update when the UI changes.
"""


class NavigationSelectors:
    """Selectors for navigation elements common across pages."""

    MAIN_NAV = "#main-nav"
    NAV_HOME = "#nav-home"
    NAV_CUSTOMERS = "#nav-customers"
    NAV_INVOICES = "#nav-invoices"
    MAIN_CONTENT = "#main-content"


class HomePageSelectors:
    """Selectors for the home page."""

    WELCOME_HEADING = "#welcome-heading"
    WELCOME_MESSAGE = "#welcome-message"


class CustomerPageSelectors:
    """Selectors for customer-related pages."""

    # List page
    LIST_HEADING = "#customers-heading"
    LIST_TABLE = "#customers-table"
    BTN_ADD_CUSTOMER = "#btn-add-customer"

    # Create page
    CREATE_HEADING = "#create-customer-heading"
    CUSTOMER_FORM = "#customer-form"
    NAME_INPUT = "#name"
    PHONE_INPUT = "#phone"
    EMAIL_INPUT = "#email"
    ADDRESS_INPUT = "#address"
    BUILDING_TYPE_SELECT = "#building_type"
    WINDOW_COUNT_INPUT = "#window_count"
    NOTES_INPUT = "#notes"
    BTN_SAVE_CUSTOMER = "#btn-save-customer"
    BTN_CANCEL = "#btn-cancel"

    @staticmethod
    def customer_row(customer_id):
        """Generate selector for a customer row by ID."""
        return f"#customer-{customer_id}"

    @staticmethod
    def customer_name_cell(customer_id):
        """Generate selector for a customer name cell by ID."""
        return f"#customer-{customer_id} .customer-name"

    @staticmethod
    def btn_view_customer(customer_id):
        """Generate selector for a view customer button by ID."""
        return f"#btn-view-customer-{customer_id}"

    @staticmethod
    def btn_delete_customer(customer_id):
        """Generate selector for a delete customer button by ID."""
        return f"#btn-delete-customer-{customer_id}"


class InvoicePageSelectors:
    """Selectors for invoice-related pages."""

    # List page
    INVOICES_HEADING = "#invoices-heading"
    INVOICES_TABLE = "#invoices-table"
    BTN_ADD_INVOICE = "#btn-add-invoice"

    @staticmethod
    def invoice_row(invoice_id):
        """Generate selector for an invoice row by ID."""
        return f"#invoice-{invoice_id}"

    @staticmethod
    def invoice_customer_cell(invoice_id):
        """Generate selector for an invoice customer cell by ID."""
        return f"#invoice-{invoice_id} .invoice-customer"

    @staticmethod
    def invoice_amount_cell(invoice_id):
        """Generate selector for an invoice amount cell by ID."""
        return f"#invoice-{invoice_id} .invoice-amount"

    @staticmethod
    def btn_view_invoice(invoice_id):
        """Generate selector for a view invoice button by ID."""
        return f"#btn-view-invoice-{invoice_id}"

    @staticmethod
    def btn_delete_invoice(invoice_id):
        """Generate selector for a delete invoice button by ID."""
        return f"#btn-delete-invoice-{invoice_id}"
