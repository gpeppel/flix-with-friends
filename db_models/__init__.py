from db_models.message import Message
from db_models.room_video_playlist import RoomVideoPlaylist
from db_models.room import Room
from db_models.room_invited_users import RoomInvitedUsers
from db_models.user import User
from db_models.video import Video

def create_tables(cur):
    User.create_table(cur)
    Room.create_table(cur)
    Message.create_table(cur)

    RoomInvitedUsers.create_table(cur)

    RoomVideoPlaylist.create_table(cur)
    Video.create_table(cur)
