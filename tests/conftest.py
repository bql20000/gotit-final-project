import pytest

from app import create_app
from app.extensions import db
from app.models.UserModel import UserModel


@pytest.fixture
def init_client():
    # initialize an app from application factory
    app = create_app('testing')

    # Establish an application context & a test client
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def init_db():
    # create database & its tables
    print("WHYYY:", db.get_app())
    db.create_all()

    # create sample users
    user1 = UserModel('long', '1234')
    user2 = UserModel('thinh', '1234')
    user1.save_to_db()
    user2.save_to_db()

    print("HUHUHUHUH:", db.get_app())

    yield db

    # tear down the database
    db.drop_all()