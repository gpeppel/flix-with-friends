from db_models.base import Base


class RoomVideoPlaylist(Base):
    def __init__(self, playlist_id, room_id):
        self.playlist_id = playlist_id
        self.room_id = room_id

    def insert_to_db(self, cur):
        cur.execute("""
            INSERT INTO room_video_playlist VALUES (%s, %s);
        """, (
            self.playlist_id,
            self.room_id
        ))

    def serialize(self):
        return {
            'playlist_id': self.playlist_id,
            'room_id': self.room_id
        }

    def from_room_id(room_id):
        playlist = RoomVideoPlaylist(
            None,
            room_id
            )
        return playlist

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
