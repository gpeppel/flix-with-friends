import flask_sqlalchemy
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    settings = db.Column(db.String(120))

    def __init__(self, usr):
        self.id = usr["user"]["id"]
        self.name = usr["name"]
        self.email = usr["email"]
        self.settings = usr["settings"]