import pytest

from app.extensions import db
from app.controllers.user import *
from app.controllers.category import *
from app.controllers.item import *    # an application has been created from this
from tests.helpers import create_db_samples


@pytest.fixture(scope='session')
def init_client():
    # Establish an application context & a test client
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='session')
def init_db():
    # create database & its tables
    db.session.commit()
    db.drop_all()
    db.create_all()
    create_db_samples()
    yield db
