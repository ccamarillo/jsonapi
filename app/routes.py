from . import app, db
from .libs.batch import Batch
from .resources import UserList, UserDetail
from .libs.exceptions import ValidationException
from .error_handlers import get_standard_error

from flask import request
from flask_rest_jsonapi import Api

import json
import pprint


# Build flask-rest-jsonapi routes from resources
api = Api(app)
api.route(UserList, "user_list", "/users")
api.route(UserDetail, "user_detail", "/users/<int:id>")


@app.route("/batch", methods=["POST"])
def batch():
    batch = Batch(request)
    return batch.execute()