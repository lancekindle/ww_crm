import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime

# Mark all tests in this module as unit tests
pytestmark = pytest.mark.unit

# This module will be useful when we implement utility functions in the application


def mock_datetime_now(monkeypatch, mocked_date=None):
    """
    Helper function to mock datetime.now for predictable testing.

    Args:
        monkeypatch: The pytest monkeypatch fixture
        mocked_date: The datetime object to return, defaults to 2025-05-15
    """
    if mocked_date is None:
        mocked_date = datetime(2025, 5, 15, 12, 0, 0)

    class MockedDatetime(datetime):
        @classmethod
        def utcnow(cls):
            return mocked_date

        @classmethod
        def now(cls):
            return mocked_date

    monkeypatch.setattr('window_wash_crm.models.datetime', MockedDatetime)
    return mocked_date
