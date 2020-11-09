from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp

from main.schemas.validators import FirstCharNotNum


class UserSchema(Schema):
    username = fields.Str(required=True,
                          validate=[Length(min=4, max=32),
                                    Regexp(r'[a-zA-Z0-9_]*$',
                                           error='Username must not contain '
                                                 'special characters (except _).'),
                                    FirstCharNotNum()
                                    ]
                          )
    password = fields.Str(required=True, validate=Length(min=4, max=32))
    created = fields.Str()
    updated = fields.Str()
