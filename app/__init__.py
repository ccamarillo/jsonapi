from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gevent import monkey
from flask_rest_jsonapi import Api
import logging
from appoptics_apm.middleware import AppOpticsApmMiddleware

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.wsgi_app = AppOpticsApmMiddleware(app.wsgi_app)
db = SQLAlchemy(app)
api = Api(app)
monkey.patch_all() # This prevents a threading error
db.init_app(app)

from . import middleware
from . import routes