from flask import current_app

from app.extensions import db, hashing


class UserModel(db.Model):
    """The user model"""

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(64))     # length of SHA-256 hash value

    items = db.relationship('ItemModel')

    def __init__(self, username, password):
        self.username = username
        self.password = hashing.hash_value(password, current_app.config['HASHING_SALT'])

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
