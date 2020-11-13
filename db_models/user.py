import flask_sqlalchemy

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    settings = db.Column(db.String(120))

    def __init__(self, user_id=None, name=None, email=None, settings=None):
        self.id = user_id
        self.name = name
        self.email = email
        self.settings = settings

        self.sid = None
        self.room = None

    @staticmethod
    def from_request(req):
        user = User(req.sid)
        user.sid = req.sid

        return user
