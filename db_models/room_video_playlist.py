import flask_sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class RoomVideoPlaylist(db.Model):
    __tablename__ = 'room_video_playlist'
    playlist_id = db.Column(db.Text, primary_key=True)
    room_id = db.Column(db.Text)
    videos = relationship('Video') 

    def __init__(self, playlist_id, room_id=None):
        self.playlist_id = playlist_id
        self.room_id = room_id
