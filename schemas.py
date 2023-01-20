from marshmallow import Schema, fields


class UserSchemaForLogin(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    # token = fields.Str(dump_only=True)


class UserSchemaForSignup(UserSchemaForLogin):
    firstname = fields.Str(required=True)


class RecordSchema(Schema):
    user_id = fields.Int(required=True)
    record_id = fields.Int(required=True)

class RecordGetSchema(Schema):
    user_id = fields.Int(required=True)
    date = fields.Str(required=True)

class RecordPostSchema(Schema):
    record_id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    user_id = fields.Int(required=True)
    date = fields.Str(required=True)
    start_time = fields.Str(required=True)
    duration = fields.Str(required=True)
