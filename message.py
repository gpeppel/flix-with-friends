from app import db

class Message(db.Model):
	id = db.Column(db.BigInteger, primary_key=True)
	text = db.Column(db.String(280))
	timestamp = db.Column(db.Time)
	roomId = db.Column(db.String(12))
	userId = db.Column(db.BigInteger)

	def __init__(self, messageId, messageText, messageTimestamp, messageRoomId, messageUserId):
		self.id = messageId
		self.text = messageText
		self.timestamp = messageTimestamp
		self.roomId = messageRoomId
		self.userId = messageUserId
