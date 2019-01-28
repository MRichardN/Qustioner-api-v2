from marshmallow import Schema, fields

# local import
#from ..util.validate import required, email, password
from app.api.v2.util.validate import required, email, password


class UserSchema(Schema):
    """  Class for user schema """

    id = fields.Int(dump_only=True)
    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    phoneNumber = fields.Str(required=False, validate=(required))
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, load_only=True, validate=(password))
    registeredOn = fields.DateTime(dump_only=True)
    questionsAsked = fields.Int(dump_only=True)
    questionsCommented = fields.Int(dump_only=True)
    
