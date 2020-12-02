class Video:
    def __init__(self, video_id, video_source, playlist_id):
        self.video_id = video_id
        self.video_source = video_source
        self.playlist_id = playlist_id

    @staticmethod
    def create_table(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS video (
                video_id BIGSERIAL PRIMARY KEY,
                video_source TEXT NOT NULL,
                playlist_id BIGINT,
                FOREIGN KEY (playlist_id)
                    REFERENCES room_video_playlist (playlist_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
            );
        """)
