import flask_sqlalchemy
from app import db

class RoomAllowedUsers(db.Model):
    room_id = db.Column(db.Text, primary_key=True)
    user_id = db.Column(db.BigInteger)

    def __init__(self, room_id=None, user_id=None):
        self.room_id = room_id
        self.user_id = user_id
