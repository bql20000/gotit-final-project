import logging
from marshmallow import Schema, fields, post_load, validate

from app.extensions import db


class ItemModel(db.Model):
    """
        Docs ...
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    cat_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # category = db.relationship('CategoryModel')
    # user = db.relationship('UserModel')

    def __init__(self, title, description, cat_id, user_id):
        self.title = title
        self.description = description
        self.cat_id = cat_id
        self.user_id = user_id

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, idx):
        return cls.query.filter_by(id=idx).first()


class ItemSchema(Schema):
    id = fields.Integer()
    title = fields.Str(required=True, validate=validate.Length(max=80))
    description = fields.Str(validate=validate.Length(max=255))
    cat_id = fields.Integer(required=True)

    # todo: add cat_id & user_id? - no need
    # todo: add validation for cat_id existence

    @post_load
    def make_item(self, data, **kwargs):
        return ItemModel(**data)  # todo: check???


item_schema = ItemSchema()
