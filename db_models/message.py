from app import db


class Message(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    text = db.Column(db.String(280))
    timestamp = db.Column(db.Time)
    room_id = db.Column(db.String(12))
    user_id = db.Column(db.BigInteger)

    def __init__(self,
		msg_id, msg_text, msg_timestamp, msg_room_id, msg_user_id
	):
        self.id = msg_id
        self.text = msg_text
        self.timestamp = msg_timestamp
        self.room_id = msg_room_id
        self.user_id = msg_user_id
