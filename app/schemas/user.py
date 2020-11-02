from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=4, max=32))
    password = fields.Str(required=True, validate=validate.Length(min=4, max=32))
    created = fields.Str()
    updated = fields.Str()
