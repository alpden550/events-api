from marshmallow import Schema, fields


class LocationSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    location_type = fields.String()
