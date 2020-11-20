import random

class Room:
    def __init__(self, room_id=None):
        self.room_id = room_id
        if self.room_id is None:
            self.room_id = Room.generate_room_id(12)

        self.users = {}
        self.creator = None

    def add_user(self, user):
        self.users[user.sid] = user

        if self.creator is None:
            self.creator = user

    def remove_user(self, user):
        if user.sid not in self.users:
            return False

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

    @staticmethod
    def generate_room_id(length=12):
        charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        room_id = ""

        for _ in range(length):
            room_id += charset[random.randint(0, len(charset) - 1)]
        return room_id
