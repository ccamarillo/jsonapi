from marshmallow_jsonapi import Schema, fields


class UserSchema(Schema):
    class Meta:
        type_ = "user"
        self_view = "user_detail"
        self_view_kwargs = {"id": "<id>"}
        self_view_many = "user_list"

    id = fields.Integer(as_string=True, dump_only=True)
    name_first = fields.Str(required=True)
    name_last = fields.Str(required=True)
    email = fields.Email(required=True)
    zip = fields.Str(required=True)
