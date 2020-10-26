import jwt
from flask import current_app

from app.models.UserModel import UserModel
from tests.functional_tests.test_user import login_demo, register_demo


def test_initialization(init_client, init_db):
    new_user = UserModel('bill', '1234')
    new_user.save_to_db()
    user = UserModel.find_by_username('bill')
    assert user.username == 'bill'
    assert user.password == '1234'


def test_jwt_encoding(init_client, init_db):
    register_demo(init_client, 'long', '1234')
    user = UserModel.find_by_username('long')
    resp = login_demo(init_client, 'long', '1234')
    assert user.id == jwt.decode(resp.get_json().get('jwt_token'),
                                 current_app.config.get('SECRET_KEY')).get('sub')