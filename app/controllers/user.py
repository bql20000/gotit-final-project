import logging

from flask import request, jsonify
from marshmallow import ValidationError

from app.models.UserModel import UserModel, user_schema
from app.security import encode_jwt


def register():
    """
        Docs ...
    """
    data = request.get_json()
    try:
        user = user_schema.load(data)
        if UserModel.find_by_username(data.get('username')):
            return jsonify({'message': 'Username existed, please choose another username.'}), 400

        user.save_to_db()
        return jsonify({'message': 'User registers successfully!'}), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


def login():
    data = request.get_json()
    try:
        user = UserModel.query.filter_by(
            username=data.get('username'),
            password=data.get('password')
        ).one()

        jwt_token = encode_jwt(user.id)
        if isinstance(jwt_token, Exception):
            response = {
                'status': 'fail',
                'message': 'Server error.'
            }
            return jsonify(response), 500
        else:
            response = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'jwt_token': jwt_token.decode()
            }
            return jsonify(response), 200
    except Exception as e:
        logging.exception("Exception")
        response = {
            'status': 'fail',
            'message': 'Wrong username or password. Please try again.'
        }
        return jsonify(response), 400

