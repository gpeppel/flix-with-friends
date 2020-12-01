import random

from db_models.base import Base


class Room(Base):
    def __init__(self, socketio, room_id, description=None):
        self.socketio = socketio
        self.room_id = room_id
        self.description = description

        self.room_code = Room.generate_room_id(length=16)
        self.settings = None

        self.users = {}
        self.creator = None

        self.current_video_code = None

    def emit(self, event, *args, sender=None):
        for sid, user in self.users.items():
            if sender is not None and sender.sid == sid:
                continue
            self.socketio.emit(event, *args, room=sid)

    def add_user(self, user):
        self.users[user.sid] = user
        user.room = self

    def remove_user(self, user):
        if user.sid not in self.users:
            return False

        user.room = None
        del self.users[user.sid]
        return True

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
            'creator': self.creator.serialize(),
            'users': {}
        }

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
