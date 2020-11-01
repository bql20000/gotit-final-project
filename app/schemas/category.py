from marshmallow import fields, Schema, validate


class CategorySchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=validate.Length(min=1, max=32))

