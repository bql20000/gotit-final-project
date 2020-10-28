from marshmallow import Schema, fields, validate


class PageSchema(Schema):
    page_number = fields.Integer(validate=validate.Range(min=1))
    items_per_page = fields.Integer(validate=validate.Range(min=1))


