import pytest

from flaskr.extensions import db
from flaskr import app
from tests.helpers import create_db_samples


def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_db_samples()
        db.session.commit()


@pytest.fixture
def client():
    reset_db()
    return app.test_client()
