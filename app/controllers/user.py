import logging

from flask import request, jsonify
from marshmallow import ValidationError

from app.models.UserModel import UserModel, user_schema
from app.security import encode_jwt


def register():
    """A new user sends username & password to register."""
    data = request.get_json()
    try:
        # validate data
        user = user_schema.load(data)

        # check if username exists
        if UserModel.find_by_username(data.get('username')):
            return jsonify({'message': 'Username existed, please choose another username.'}), 400

        # save user's data & response a successful message
        user.save_to_db()
        return jsonify({'message': 'User registers successfully!'}), 201
    except ValidationError as e:
        logging.exception("Invalid request data to register.")
        return jsonify(e.messages), 400
    except Exception as e:
        logging.exception("Unknown error while registering.")
        return jsonify({'message': 'Unknown error while registering.'}), 500


def login():
    """User sends username & password to login.
    :return: successful message & JWT
    """
    data = request.get_json()
    try:
        # find users from database
        user = UserModel.query.filter_by(
            username=data.get('username'),
            password=data.get('password')
        ).one()

        # generate jwt & response to client
        jwt_token = encode_jwt(user.id)
        if isinstance(jwt_token, Exception):
            return jsonify({'message': 'Server error.'}), 500
        else:
            response = {
                'message': 'Successfully logged in.',
                'jwt_token': jwt_token.decode()
            }
            return jsonify(response), 200
    except Exception as e:
        logging.exception("Wrong username or password")
        return jsonify({'message': 'Wrong username or password.'}), 400

