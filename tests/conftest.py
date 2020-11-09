import pytest

from main.extensions import db
from main import app
from tests.helpers import create_db_samples


def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_db_samples()


@pytest.fixture
def client():
    reset_db()
    return app.test_client()
