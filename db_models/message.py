class Message:
    def __init__(self, message_id, text, timestamp, room_id, user_id):
        self.message_id = message_id
        self.text = text
        self.timestamp = timestamp
        self.room_id = room_id
        self.user_id = user_id

    @staticmethod
    def get_messages(cur, room_id=None):
        query = """
            SELECT m.message_id, m.text, m.timestamp, m.room_id, m.user_id, a.username, a.profile_url
            FROM message m INNER JOIN account a ON m.user_id = a.user_id
        """
        values = ()

        if room_id is not None:
            query += ' WHERE m.room_id = %s'
            values = (room_id)

        query += ';'
        cur.execute(query, values)

        messages = []
        for result in cur:
            messages.append(Message(
                result['message_id'],
                result['text'],
                result['timestamp'],
                result['room_id'],
                result['user_id']
            ))

        return messages

    @staticmethod
    def insert_to_db(cur, msg):
        cur.execute("""
            INSERT INTO message VALUES (DEFAULT, %s, %s, %s, %s) RETURNING message_id
        """, (
            msg.text,
            msg.timestamp,
            msg.room_id,
            msg.user_id
        ))

        result = cur.fetchone()
        msg.message_id = result['message_id']

        return msg

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
