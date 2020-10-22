from flask import request, jsonify
from marshmallow import ValidationError

from app.models.UserModel import UserModel, user_schema
from app.database import db


def register():
    """
        Docs ...
    """
    data = request.get_json()
    if UserModel.find_by_username(data['username']):
        return jsonify({'message': 'Username existed, please choose another username.'}), 400
    try:
        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()
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

        jwt_token = UserModel.encode_jwt(user.id)
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
                'jwt_token': jwt_token
            }
            return jsonify(response), 200

    except Exception as e:
        response = {
            'status': 'fail',
            'message': 'Wrong username or password.'
        }
        return jsonify(response), 400

