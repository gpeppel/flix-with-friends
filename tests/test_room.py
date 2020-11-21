import random
import unittest

from db_models.room import Room
from db_models.user import User


USERS = [
    User(None, sid='01234567890'),
    User(None, sid='abcdef'),
    User(None, sid='a1b2c3d4e5f6'),
]


class RoomTest(unittest.TestCase):
    def test_add_users(self):
        test_room = Room()

        for test_user in USERS:
            test_room.add_user(test_user)
            self.assertTrue(test_room.has_user(test_user))

    def test_remove_users_success(self):
        test_room = Room()

        for test_user in USERS:
            test_room.add_user(test_user)

        test_room.remove_user(USERS[0])
        self.assertFalse(test_room.has_user(USERS[0]))

    def test_remove_users_fail(self):
        test_room = Room()
        test_room.add_user(USERS[0])

        test_room.remove_user(USERS[1])
        self.assertFalse(test_room.has_user(USERS[1]))

    def test_is_creator_success(self):
        test_room = Room()
        test_room.add_user(USERS[0])
        test_room.set_creator(USERS[0])

        self.assertTrue(test_room.is_creator(USERS[0]))

        test_room.set_creator(USERS[1])
        self.assertTrue(test_room.has_user(USERS[1]))
        self.assertTrue(test_room.is_creator(USERS[1]))

    def test_is_creator_fail(self):
        test_room = Room()
        test_room.add_user(USERS[0])
        test_room.set_creator(None)

        self.assertFalse(test_room.is_creator(USERS[0]))

    def test_length(self):
        test_room = Room()

        for test_user in USERS:
            test_room.add_user(test_user)

        self.assertEqual(len(test_room), len(USERS))

    def test_generateRoomId(self):
        random.seed(7883)
        self.assertEqual(Room().room_id, 'Zp5s_mMGCaTy')
