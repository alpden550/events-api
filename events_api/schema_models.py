from marshmallow import Schema, fields


class EventSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String()
    date = fields.Date()
    time = fields.Time()
    event_type = fields.String()
    category = fields.String()
    address = fields.String()
    seats = fields.Integer()
    location = fields.String()


class LocationSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    location_type = fields.String()
    events = fields.Nested('EventSchema', many=True)
