from marshmallow import Schema, fields
#from ..util.validate import date_checker, required
from app.api.v2.util.validate import date_checker, required, tag


class MeetupSchema(Schema):
    """ Schema for Meetups """

    id = fields.Int(dump_only=True)
    topic = fields.Str(required=True, validate=(required))
    description = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    happeningOn = fields.Str(required=True, validate=(required, date_checker))
    createdOn = fields.DateTime(dump_only=True)
<<<<<<< HEAD
    tags = fields.List(fields.Str(), required=True, validate=(tag))
=======
    usersAttending = fields.Int(dump_only=True)
    tags = fields.List(fields.Str(),required=True, validate=(tag))
>>>>>>> 3d5bb255d63bf2cd9f014ada570d278871c9fa91
    attendees = fields.Int(dump_only=True)
    
