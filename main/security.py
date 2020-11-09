import datetime
from functools import wraps

import jwt
from flask import request, current_app
from werkzeug.exceptions import Unauthorized, BadRequest


def encode_jwt(user_id):
    """
    Generates JWT
    :param: user_id
    :return: string
    """
    payload = {
        'exp': (datetime.datetime.utcnow()
                + datetime.timedelta(seconds=current_app.config['JWT_EXPIRATION_PERIOD'])),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256').decode()


def requires_auth(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        auth_header = request.headers.get('AUTHORIZATION')
        if not auth_header:
            raise Unauthorized('Please log in first.')
        try:
            # exclude "Bearer " from "Bearer {access_token}"
            try:
                token_type, access_token = auth_header.split()
            except ValueError:
                raise BadRequest('Bad authorization header.')
            if token_type != 'Bearer':
                raise BadRequest(f'{token_type} token type not supported.')
            user_id = jwt.decode(access_token, current_app.config['SECRET_KEY'])['sub']
            return func(*args, user_id=user_id, **kwargs)
        except jwt.ExpiredSignatureError:
            raise Unauthorized('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise Unauthorized('Invalid token. Please log in again.')

    return decorated_func
