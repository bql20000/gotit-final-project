import jwt
import logging
import datetime
from functools import wraps

from flask import jsonify, request, current_app


def encode_jwt(user_id):
    """
    Generates JWT
    :param: user_id
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1000),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        logging.exception("Exception")
        return e


def requires_auth(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        token = request.headers['AUTHORIZATION']
        if not token:
            return jsonify({'message': 'Please log in first.'}), 401
        try:
            jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token. Please log in again.'}), 401

    return decorated_func


def get_user_id_from_request():
    """Return the id of the user making the request."""
    token = request.headers['AUTHORIZATION']
    return jwt.decode(token, current_app.config.get('SECRET_KEY')).get('sub')

