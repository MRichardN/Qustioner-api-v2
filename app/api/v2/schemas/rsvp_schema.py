from marshmallow import Schema, fields
from app.api.v2.util.validate import required


class RsvpSchema(Schema):
    """Schema for Rsvp """

    id = fields.Integer(required=False)
    response = fields.Str(required=True, validate=(required))
    meetup_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    createdOn = fields.DateTime(dump_only=True)
