from marshmallow import Schema, fields
from marshmallow.validate import Length

from app.schemas.validators import CategoryExists, FirstCharNotNum


class ItemSchema(Schema):
    id = fields.Integer()
    name = fields.Str(required=True, validate=[Length(min=1, max=32), FirstCharNotNum()])
    description = fields.Str(required=True, validate=Length(max=255))
    category_id = fields.Integer(required=True, validate=CategoryExists())
    user_id = fields.Integer()
    created = fields.Str()
    updated = fields.Str()


