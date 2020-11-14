import flask_sqlalchemy

from app import db


class User(db.Model):
    id = db.Column(db.Text, primary_key=True)
    name = db.Column(db.String(120))
    image_url = db.Column(db.Text)
    settings = db.Column(db.String(120))
    oauth_id = db.Column(db.Text)
    oauth_type = db.Column(db.Text)

    def __init__(self, id, name=None, image_url=None, settings=None, oauth_id=None, oauth_type=None):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.settings = settings
        self.oauth_id = oauth_id
        self.oauth_type = oauth_type
        self.sid = None
        self.room = None

    @staticmethod
    def from_request(req):
        user = User(req.sid)
        user.sid = req.sid
        return user
