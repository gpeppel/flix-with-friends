class RoomVideoPlaylist:
    def __init__(self, playlist_id, room_id):
        self.playlist_id = playlist_id
        self.room_id = room_id

    @staticmethod
    def create_table(cur):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS room_video_playlist (
            playlist_id BIGSERIAL PRIMARY KEY,
            room_id TEXT,
            FOREIGN KEY (room_id)
                REFERENCES room (room_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        );
        """)
