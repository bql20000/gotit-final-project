import logging

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.orm.exc import NoResultFound

from app.models.user import UserModel
from app.schemas.user import user_schema
from app.security import encode_jwt


def register():
    """A new user sends username & password to register."""
    data = request.get_json()
    try:
        # validate data
        user_schema.load(data)

        # check if username exists
        if UserModel.query.filter_by(username=data.get('username')).first():
            raise ValidationError('Username existed, please choose another username.')

        # save user's data & response a successful message
        user = UserModel(**data)
        user.save_to_db()
        return jsonify(message='User registers successfully.'), 201
    except ValidationError as e:
        logging.exception('Invalid request data to register.')
        return jsonify(e.messages), 400
    except:
        logging.exception('Unknown error while registering.')
        return jsonify(message='Unknown error while registering'), 500


def login():
    """User sends username & password to login.
    :return: successful message & JWT
    """
    data = request.get_json()
    try:
        # validate data
        user_schema.load(data)

        # find users from database --> throws NoResultFound exception
        user = UserModel.query.filter_by(
            username=data.get('username'),
            password=data.get('password')
        ).one()

        # generate jwt & response to client
        jwt_token = encode_jwt(user.id)
        return jsonify(message='Successfully logged in.',
                       jwt_token=jwt_token.decode()
                       ), 200
    except (NoResultFound, ValidationError) as e:
        logging.exception(e)
        response = {'message': 'Wrong username or password.',
                    'username': [],
                    'password': []
                    }
        if e.messages.get('username'):
            response['username'] = e.messages.get('username')
        if e.messages.get('password'):
            response['password'] = e.messages.get('password')

        return jsonify(response), 400
    except:
        logging.exception('Unknown error while logging in.')
        return jsonify({'message': 'Unknown error while logging in.'}), 500
