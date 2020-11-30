import random

from db_models.base import Base


class Room(Base):
    def __init__(self, room_id=None, name=None):
        self.room_id = room_id
        if self.room_id is None:
            self.room_id = Room.generate_room_id(12)

        self.name = name

        self.settings = None

        self.users = {}
        self.creator = None

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
            self.creator = None
        return True

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
            INSERT INTO room VALUES (%s, %s, %s);
        """, (
            self.room_id,
            self.name,
            self.settings
        ))

    def serialize(self):
        obj = {
            'room_id': self.room_id,
            'creator': self.creator,
            'users': {}
        }

        for user in self.users:
            obj['users'][user.get_session_id()] = user.serialize()

        return obj

    @staticmethod
    def generate_room_id(length=12):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        room_id = ""

        for _ in range(length):
            room_id += charset[random.randint(0, len(charset) - 1)]
        return room_id

    @staticmethod
    def create_table(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS room (
                room_id TEXT PRIMARY KEY,
                name TEXT,
                settings TEXT
            );
        """)
