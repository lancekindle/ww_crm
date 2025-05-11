"""
Pytest configuration for parallel test execution.

This module extends the standard pytest configuration to support parallel test execution
using pytest-xdist. It provides specialized fixtures that ensure test isolation when
running tests concurrently.

Usage:
    pytest -xvs -n 4 --conftest=ww_crm/tests/conftest_parallel.py

This will run tests with 4 parallel workers using this configuration file.
"""
import os
import pytest
import tempfile
import shutil
from pathlib import Path

from ww_crm.tests.conftest import *  # Import all fixtures from standard conftest


def pytest_configure(config):
    """Register custom markers with pytest."""
    config.addinivalue_line("markers", "parallel: mark test as suitable for parallel execution")
    config.addinivalue_line("markers", "serial: mark test as requiring serial execution (cannot be run in parallel)")


@pytest.fixture(scope="session")
def worker_id(request):
    """Return the worker ID for xdist."""
    if hasattr(request.config, 'workerinput'):
        return request.config.workerinput['workerid']
    return "main"


@pytest.fixture(scope="session")
def tmp_path_factory_per_worker(tmp_path_factory, worker_id):
    """Create a temporary directory specifically for this worker."""
    root_tmp_dir = tmp_path_factory.getbasetemp()
    worker_tmp_dir = root_tmp_dir / worker_id
    worker_tmp_dir.mkdir(exist_ok=True)
    return worker_tmp_dir


@pytest.fixture(scope="session")
def base_temp_dir(worker_id):
    """Return a unique temporary directory for the worker."""
    temp_dir = Path(tempfile.mkdtemp(prefix=f"wwcrm_parallel_tests_{worker_id}_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def parallel_db_path(base_temp_dir, worker_id):
    """Create a unique database path for the worker to ensure test isolation."""
    return base_temp_dir / f"test_db_{worker_id}.sqlite"


@pytest.fixture(scope="session")
def parallel_app_config(parallel_db_path):
    """Create app configuration for parallel testing."""
    return {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{parallel_db_path}',
        'SERVER_NAME': f'localhost.localdomain',
        'PREFERRED_URL_SCHEME': 'http',
        'WTF_CSRF_ENABLED': False,
    }


@pytest.fixture(scope="function")
def app(parallel_app_config):
    """Create a Flask application instance for testing.

    This fixture overrides the standard 'app' fixture to use the parallel configuration.
    """
    from ww_crm import create_app, db

    app = create_app(parallel_app_config)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def live_server(app, worker_id):
    """Run the app in a live server for browser tests.

    This fixture overrides the standard 'live_server' fixture to use a different
    port for each worker to avoid port conflicts when running in parallel.
    """
    import multiprocessing
    from werkzeug.serving import make_server

    # Extract worker number for port assignment
    try:
        worker_num = int(''.join(filter(str.isdigit, worker_id)))
    except ValueError:
        worker_num = 0

    # Assign a unique port based on worker ID
    port = 5000 + worker_num

    # Create server with the unique port
    server = make_server('localhost', port, app)
    server_thread = multiprocessing.Process(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    yield f"http://localhost:{port}"

    server_thread.terminate()
    server_thread.join()


def pytest_collection_modifyitems(items):
    """Mark tests that can't be run in parallel."""
    # Mark tests that require exclusive access to shared resources
    for item in items:
        # Some tests may require exclusive database access or other shared resources
        if "serial" in item.keywords:
            item.add_marker(pytest.mark.xdist_group("serial"))

        # E2E tests usually need to be run serially for browser stability
        if "visual" in item.keywords and "parallel" not in item.keywords:
            item.add_marker(pytest.mark.xdist_group("visual"))
