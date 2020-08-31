import os
import tempfile

import pytest

from emapp import create_app
from emapp.event import init_events


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test.
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config.
    app = create_app({
        "API_KEY": "test",
        "PREDEFINED_EVENTS": [
            {
                'name': 'foo',
                'location': 'x',
                'start_time': '2020-08-30 18:00:00',  # utc
                'end_time': '2020-08-30 20:00:00',  # utc
            },
            {
                'name': 'bar',
                'location': 'y',
                'start_time': '2020-08-30 19:00:00',  # utc
                'end_time': '2020-09-01 19:00:00',  # utc
            },
        ],
        "DATABASE": db_path})

    # create the database and load test data.
    with app.app_context():
        init_events()

    yield app

    # close and remove the temporary database.
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
