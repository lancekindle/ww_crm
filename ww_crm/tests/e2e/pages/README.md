# Page Object Model Implementation

This directory contains the Page Object Model (POM) implementation for the Window Wash CRM UI tests. The Page Object Model is a design pattern that creates an abstraction layer between test scripts and the UI, making tests more maintainable, reusable, and readable.

## Design Principles

The implementation follows SOLID principles:

1. **Single Responsibility Principle**: Each page object class focuses on one specific page or component.
2. **Open/Closed Principle**: Classes are open for extension but closed for modification, through inheritance and composition.
3. **Liskov Substitution Principle**: Derived classes can be used in place of their base classes without affecting behavior.
4. **Interface Segregation Principle**: Classes expose only the methods that clients need, with specialized interfaces (FormPage, NavigablePage).
5. **Dependency Inversion Principle**: High-level modules depend on abstractions, not concrete implementations.

## Architecture

The architecture consists of the following components:

### Selector Registry (`selectors.py`)

Centralizes all CSS selectors used in page objects, making them easier to maintain and update when the UI changes. This decouples selectors from page object implementation.

### Base Classes (`base_page.py`)

- **BasePage**: Core functionality common to all pages
- **NavigablePage**: Pages with navigation capabilities
- **FormPage**: Pages with form interaction capabilities

These follow a composition pattern allowing pages to inherit only the functionality they need.

### Page Objects

Individual page objects encapsulate the behavior and elements of specific pages:

- **HomePage**: Home page interactions
- **CustomerListPage**: Customer listing page interactions
- **CustomerCreatePage**: Customer creation form interactions
- **InvoiceListPage**: Invoice listing page interactions

## Benefits of This Approach

1. **Reduced Duplicated Code**: Common functionality is abstracted into base classes.
2. **Improved Readability**: Page objects use descriptive method names that express intent.
3. **Better Error Handling**: Consistent error messages and logging make debugging easier.
4. **Decoupled Selectors**: Centralized selectors make UI changes easier to manage.
5. **Reusable Components**: Base classes can be reused across different page objects.
6. **Clearer Responsibilities**: Each class has a clear, single responsibility.

## Usage Example

```python
def test_customer_list(self, sample_customer):
    """Test that the customer list displays properly."""
    # Navigate to customers page
    self.home_page.click_nav_customers()

    # Verify page loaded correctly
    self.customer_list_page.assert_page_loaded()

    # Verify sample customer is visible
    self.customer_list_page.assert_customer_visible(
        sample_customer.id, sample_customer.name
    )
```

## Future Improvements

1. **Fix Form Submission Test**: Investigation needed to resolve issues with the form submission test.
2. **Address SQLAlchemy Warnings**: Update code to use modern SQLAlchemy patterns.
3. **Add More Test Coverage**: Implement additional tests for edge cases.
4. **Implement Page Factory**: Consider adding a Page Factory pattern to manage page object creation.
