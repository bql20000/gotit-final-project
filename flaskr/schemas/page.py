from marshmallow import Schema, fields, validate


class PageSchema(Schema):
    page_number = fields.Int(validate=validate.Range(min=1))
    items_per_page = fields.Int(validate=validate.Range(min=1))
