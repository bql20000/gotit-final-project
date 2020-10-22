import jwt
import datetime
from marshmallow import Schema, fields, post_load, validate

from app.database import db


class UserModel(db.Model):
    """
        Docs ...
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, idx):
        return cls.query.filter_by(id=idx).first()

    def encode_jwt(self, user_id):
        """
        Generates JWT
        :param: user_id
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_jwt(token):
        """
        Decodes JWT
        :param token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(max=32))
    password = fields.Str(required=True, validate=validate.Length(max=32))

    @post_load
    def make_user(self, data, **kwargs):
        return UserModel(**data)


user_schema = UserSchema()
