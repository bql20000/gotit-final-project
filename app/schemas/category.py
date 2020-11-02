from marshmallow import fields, Schema
from marshmallow.validate import Length
from app.schemas.validators import FirstCharNotNum


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=[Length(min=1, max=32), FirstCharNotNum()])
    created = fields.Str()
    updated = fields.Str()
