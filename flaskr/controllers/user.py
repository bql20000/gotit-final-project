from flask import jsonify, current_app
from werkzeug.exceptions import BadRequest

from flaskr import app
from flaskr.models.user import UserModel
from flaskr.schemas.user import UserSchema
from flaskr.security import encode_jwt
from flaskr.extensions import hashing
from flaskr.helpers import load_request_data


@app.route('/register', methods=['POST'])
@load_request_data(UserSchema)
def register(data):
    """A new user sends username & password to register."""

    # check if username exists
    if UserModel.query.filter_by(username=data['username']).first():
        raise BadRequest('Username existed.')

    # save user's data & response a successful message
    user = UserModel(**data)
    user.save_to_db()
    return jsonify(UserSchema(exclude=('password',)).dump(user)), 201


@app.route('/login', methods=['POST'])
@load_request_data(UserSchema)
def login(data):
    """User sends username & password to login.
    :return: successful message & JWT
    """

    # find users from database
    user = UserModel.query.filter_by(
        username=data['username'],
        password=hashing.hash_value(data['password'], current_app.config['HASHING_SALT'])
    ).first()

    if user is None:
        raise BadRequest('Wrong username or password.')

    # generate jwt & response to client
    jwt_token = encode_jwt(user.id)
    return jsonify(jwt_token=jwt_token.decode()), 200
