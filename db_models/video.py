import flask_sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Text, primary_key=True)
    playlist_id = db.Column(db.Text, ForeignKey('room_video_playlist.playlist_id'))
    room_video_playlist = relationship("RoomVideoPlaylist")

    def init(self, id, playlist_id):
        self.id = id
        self.playlist_id = playlist_id
