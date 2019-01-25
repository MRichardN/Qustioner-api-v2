from marshmallow import Schema, fields
#from ..util.validate import required
from app.api.v2.util.validate import required

class QuestionSchema(Schema):
    """ Schema for Questions """

    id = fields.Int(dump_only=True)
    title = fields.Str(required=False, validate=(required))
    body = fields.Str(required=True, validate=(required))
    meetup_id = fields.Int(required=True)
    user_id = fields.Int(dump_only=True)
    votes = fields.Int(dump_only=True)
    createdOn = fields.DateTime(dump_only=True)
