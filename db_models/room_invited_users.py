class RoomInvitedUsers:
    def __init__(self, room_id=None, user_id=None):
        self.room_id = room_id
        self.user_id = user_id

    @staticmethod
    def create_table(cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS room_invited_users (
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
