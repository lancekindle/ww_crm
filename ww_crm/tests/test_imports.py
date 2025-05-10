"""
Test to verify imports are working correctly.
"""
import pytest

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit

def test_import_factory():
    """Test that we can import the factory classes."""
    try:
        from ww_crm.tests.fixtures.factories import CustomerFactory, InvoiceFactory
        assert CustomerFactory is not None
        assert InvoiceFactory is not None
        print("Factory imports successful")
    except ImportError as e:
        assert False, f"Import failed: {e}"

def test_import_db_utils():
    """Test that we can import the database utilities."""
    try:
        from ww_crm.tests.fixtures.db_utils import seed_test_data, clear_test_data, count_records
        assert seed_test_data is not None
        assert clear_test_data is not None
        assert count_records is not None
        print("DB utils imports successful")
    except ImportError as e:
        assert False, f"Import failed: {e}"
