from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(max=32))
    password = fields.Str(required=True, validate=validate.Length(max=32))


user_schema = UserSchema()
