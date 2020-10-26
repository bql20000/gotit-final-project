from marshmallow import Schema, fields, post_load, validate, ValidationError

from app.extensions import db
from app.models.CategoryModel import CategoryModel


class ItemModel(db.Model):
    """The item model"""

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # items table has 2 foreign keys referencing users & categories table
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

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_to_db(self, data):
        self.query.filter_by(id=self.id).update(data)
        db.session.commit()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, idx):
        return cls.query.filter_by(id=idx).first()


def validate_cat_id(idx):
    """Check if a category with id = idx exists."""
    category = CategoryModel.find_by_id(idx)
    if category is None:
        raise ValidationError('Category not existed.')


class ItemSchema(Schema):
    id = fields.Integer()
    title = fields.Str(required=True, validate=validate.Length(max=80))
    description = fields.Str(required=True, validate=validate.Length(max=255))
    cat_id = fields.Integer(required=True, validate=validate_cat_id)
    user_id = fields.Integer()

    @post_load
    def make_item(self, data, **kwargs):
        return ItemModel(**data)


item_schema = ItemSchema()
