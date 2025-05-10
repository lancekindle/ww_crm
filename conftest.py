"""
Project-level pytest configuration for Flask testing.
This file sets up Flask-specific configuration for pytest-flask plugin.
"""
import pytest
from ww_crm.app import app as flask_app


@pytest.fixture
def app():
    """Flask application fixture for pytest-flask."""
    return flask_app
