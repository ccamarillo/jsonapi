from flask import Flask
from flask_rest_jsonapi import Api, ResourceDetail, ResourceList
from flask_rest_jsonapi.exceptions import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from marshmallow_jsonapi import Schema, fields
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/brightMd.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)
    zip = db.Column(db.String)

db.create_all()

class UserSchema(Schema):
    class Meta:
        type_ = 'user'
        self_view = 'user_detail'
        self_view_kwargs = {'id': '<id>'}
        self_view_many = 'user_list'

    id = fields.Integer(as_string=True, dump_only=True)
    name_first = fields.Str(required=True)
    name_last = fields.Str(required=True)
    email = fields.Email(required=True)
    zip = fields.Str(required=True)

class UserList(ResourceList):
    schema = UserSchema
    data_layer = {'session': db.session, 'model': User}

class UserDetail(ResourceDetail):
    def before_get_object(self, kwargs):
        try:
            user = self.session.query(User).filter_by(id=kwargs['id']).one()
        except NoResultFound:
            raise ObjectNotFound({'parameter': 'id'}, f"User: {kwargs['id']} not found")
        
    schema = UserSchema
    data_layer = {'session': db.session, 'model': User, 'methods': {
        'before_get_object': before_get_object
    }}

api = Api(app)
api.route(UserList, 'user_list', '/users')
api.route(UserDetail, 'user_detail', '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)