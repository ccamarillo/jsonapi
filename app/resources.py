from . import db
from .libs.exceptions import ValidationException
from .models import User
from .schemas import UserSchema

from flask import abort
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from sqlalchemy.orm.exc import NoResultFound


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {"session": db.session, "model": User}


class UserDetail(ResourceDetail):
    def before_get_object(self, kwargs):
        try:
            user = self.session.query(User).filter_by(id=kwargs["id"]).one()
        except NoResultFound:
            raise ObjectNotFound({"parameter": "id"}, f"User: {kwargs['id']} not found")

    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        "methods": {"before_get_object": before_get_object},
    }
