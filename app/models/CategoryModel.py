from marshmallow import fields, Schema, validate, post_load

from app.extensions import db


class CategoryModel(db.Model):
    """The category model"""

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, idx):
        return cls.query.filter_by(id=idx).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1, max=80))

    @post_load
    def make_category(self, data, **kwargs):
        return CategoryModel(**data)


category_schema = CategorySchema()
