from marshmallow import fields, Schema
from marshmallow.validate import Length

from main.schemas.validators import FirstCharNotNum


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True,
                      validate=[Length(min=1, max=32), FirstCharNotNum()])
    created = fields.Str()
    updated = fields.Str()
