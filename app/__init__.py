from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_rest_jsonapi import Api
import logging

import json
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI');
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

db.init_app(app)

from . import middleware
from . import routes
from . import error_handlers
