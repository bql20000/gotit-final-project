from marshmallow import fields, Schema
from marshmallow.validate import Length, Regexp

from app.schemas.validators import FirstCharNotNum


class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True,
                      validate=[Length(min=1, max=32),
                                FirstCharNotNum(),
                                Regexp(r'[a-zA-Z0-9_]*$',
                                       error='Category name must not contain '
                                             'special characters (except _).')
                                ]
                      )
    created = fields.Str()
    updated = fields.Str()
