from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name_first = db.Column(db.String)
    name_last = db.Column(db.String)
    zip = db.Column(db.String)

db.create_all()