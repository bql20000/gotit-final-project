import typing

from marshmallow import Schema, fields, validate, ValidationError
from marshmallow.validate import Validator, Length, Regexp


class FirstChar(Validator):
    error = 'First character must not be a number.'

    def __call__(self, value) -> typing.Any:
        if value and '9' >= value[0] >= '0':
            raise ValidationError(FirstChar.error)
        return value


class UserSchema(Schema):
    username = fields.Str(required=True,
                          validate=[Length(min=4, max=32),
                                    Regexp(r'[a-zA-Z0-9_]*$',
                                           error='Username must not contain '
                                                 'special characters (except _).'),
                                    FirstChar()
                                    ]
                          )
    password = fields.Str(required=True, validate=validate.Length(min=4, max=32))
    created = fields.Str()
    updated = fields.Str()
