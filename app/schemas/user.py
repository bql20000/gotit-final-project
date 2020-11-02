from marshmallow import Schema, fields, validate



class UserSchema(Schema):
    username = fields.Str(required=True,
                          validate=[validate.Length(min=4, max=32),
                                    validate.Regexp(r'[a-zA-Z0-9_\-]*$',
                                                    error='Username must not contain '
                                                    'special characters (except _ and -).')]
                          )
    password = fields.Str(required=True, validate=validate.Length(min=4, max=32))
    created = fields.Str()
    updated = fields.Str()
