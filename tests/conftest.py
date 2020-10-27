import pytest

from app import create_app
from app.extensions import db


@pytest.fixture(scope='function')
def init_client():
    # initialize an app from application factory
    app = create_app()

    # Establish an application context & a test client
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='function')
def init_db():
    # create database & its tables
    db.session.commit()
    db.drop_all()
    db.create_all()
    yield db
