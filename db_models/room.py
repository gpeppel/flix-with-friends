import random

from db_models.base import Base
import utils


class Room(Base):
    def __init__(self, socketio, room_id, description=None):
        self.socketio = socketio
        self.room_id = room_id
        self.description = description

        self.room_code = Room.generate_room_id(length=6)
        self.settings = None

        self.users = {}
        self.creator = None

        self.current_video_code = None

        self.host_mode = True
        self.vote_threshold = 0
        self.users_add_video_enabled = False

    def emit(self, event, *args, sender=None):
        for sid in self.users:
            if sender is not None and sender.sid == sid:
                continue
            self.socketio.emit(event, *args, room=sid)

    def add_user(self, user):
        self.users[user.sid] = user
        user.room = self

        if self.creator is None:
            self.creator = user

    def remove_user(self, user):
        if user.sid not in self.users:
            return False

        user.room = None
        del self.users[user.sid]

        if self.is_creator(user):
            self.set_random_host()

        return True

    def empty_room(self):
        for user in list(self.users.values()):
            self.remove_user(user)

    def get_current_video_code(self):
        return self.current_video_code

    def has_user(self, user):
        return user.sid in self.users

    def is_creator(self, user):
        if self.creator is None:
            return False
        return user.sid == self.creator.sid

    def set_creator(self, user):
        if user is not None and not self.has_user(user):
            self.add_user(user)

        self.creator = user

    def get_host_mode(self):
        return self.host_mode

    def set_host_mode(self, val):
        self.host_mode = val

    def reaches_vote_threshold(self, vote_count):
        if self.vote_threshold <= 0:
            return False
        if self.vote_threshold < 1:
            return vote_count / len(self) >= self.vote_threshold
        return vote_count >= self.vote_threshold

    def set_vote_threshold(self, threshold):
        self.vote_threshold = utils.clamp(threshold, 0, len(self))

    def can_users_add_videos(self):
        return self.users_add_video_enabled

    def set_random_host(self):
        if len(self) == 0:
            self.set_creator(None)
            return
        self.set_creator(random.choice(list(self.users.values())))

    def set_users_can_add_video(self, val):
        self.users_add_video_enabled = val

    def get_settings(self):
        return {
            'host_mode': self.host_mode,
            'vote_threshold': self.vote_threshold,
            'users_add_video_enabled': self.users_add_video_enabled
        }

    def __len__(self):
        return len(self.users)

    def insert_to_db(self, cur):
        cur.execute("""
            INSERT INTO room VALUES (%s, %s, %s)
            ON CONFLICT (room_id) DO NOTHING;
        """, (
            self.room_id,
            self.description,
            self.settings
        ))

    def serialize(self):
        obj = {
            'room_id': self.room_id,
            'description': self.description,
            'creator': None,
            'users': {}
        }

        if self.creator is not None:
            obj['creator'] = self.creator.serialize()

        for user in self.users.values():
            obj['users'][user.get_session_id()] = user.serialize()

        return obj

    @staticmethod
    def generate_room_id(length=16):
        charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
        room_id = ''

        for _ in range(length):
            room_id += charset[random.randint(0, len(charset) - 1)]
        return room_id

    @staticmethod
    def create_table(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS room (
                room_id TEXT PRIMARY KEY,
                description TEXT,
                settings TEXT
            );
        """)
