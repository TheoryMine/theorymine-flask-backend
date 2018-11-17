import pytest

from app import create_app
from app.db import get_db, truncate_db
from app.get_stripe import get_stripe


@pytest.fixture
def app():
    app = create_app("testing")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    with app.app_context():
        db = get_db()
        truncate_db()
        yield db

@pytest.fixture
def stripe(app):
    with app.app_context():
        stripe = get_stripe()
        yield stripe
