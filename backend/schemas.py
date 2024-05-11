from marshmallow import Schema, fields


class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    firstName = fields.Str(required=True)
    lastName = fields.Str(required=True)
    email = fields.Str(required=True, )