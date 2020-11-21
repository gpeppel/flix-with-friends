class Message:
    def __init__(self, message_id, text, timestamp, room_id, user_id):
        self.message_id = message_id
        self.text = text
        self.timestamp = timestamp
        self.room_id = room_id
        self.user_id = user_id

    @staticmethod
    def create_table(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS message (
                message_id BIGSERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                room_id TEXT NOT NULL,
                user_id BIGINT NOT NULL,
                FOREIGN KEY (room_id)
                    REFERENCES room (room_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (user_id)
                    REFERENCES account (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );
        """)
