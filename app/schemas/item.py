from marshmallow import Schema, fields, validate, ValidationError

from app.models.category import CategoryModel


def validate_category_id(idx):
    """Check if a category with id = idx exists."""
    category = CategoryModel.query.filter_by(id=idx).first()
    if category is None:
        raise ValidationError(f'Category with id {idx} not found.')


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True, validate=validate.Length(min=1, max=32))
    description = fields.Str(required=True, validate=validate.Length(max=255))
    category_id = fields.Integer(required=True, validate=validate_category_id)
    user_id = fields.Integer()

