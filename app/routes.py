from . import app, db
from .resources import UserList, UserDetail
from flask_rest_jsonapi import Api

# Build flask-rest-jsonapi routes from resources
api = Api(app)
api.route(UserList, "user_list", "/users")
api.route(UserDetail, "user_detail", "/users/<int:id>")
