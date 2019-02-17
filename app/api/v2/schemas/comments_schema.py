from marshmallow import Schema, fields
#from ..util.validate import required
from app.api.v2.util.validate import required


class CommentSchema(Schema):
    """ Comments schema."""

    id = fields.Int(dump_only=True)
    createdOn = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)
    question_id = fields.Int(dump_only=True)
    body = fields.Str(required=True, validate=(required))
    
    