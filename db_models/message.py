class Message:
    def __init__(self, message_id, text, timestamp, room_id, user_id):
        self.message_id = message_id
        self.text = text
        self.timestamp = timestamp
        self.room_id = room_id
        self.user_id = user_id
