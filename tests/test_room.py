import random
import unittest

from db_models.room import Room
from db_models.user import User


USERS = [
    User('01234567890'),
    User('abcdef'),
    User('a1b2c3d4e5f6'),
]


class RoomTest(unittest.TestCase):
    def test_add_users(self):
        testRoom = Room()

        for testUser in USERS:
            testRoom.addUser(testUser)
            self.assertTrue(testRoom.hasUser(testUser))

    def test_remove_users_success(self):
        testRoom = Room()

        for testUser in USERS:
            testRoom.addUser(testUser)

        testRoom.removeUser(USERS[0])
        self.assertFalse(testRoom.hasUser(USERS[0]))

    def test_remove_users_fail(self):
        testRoom = Room()
        testRoom.addUser(USERS[0])

        testRoom.removeUser(USERS[1])
        self.assertFalse(testRoom.hasUser(USERS[1]))

    def test_is_creator_success(self):
        testRoom = Room()
        testRoom.addUser(USERS[0])
        testRoom.setCreator(USERS[0])

        self.assertTrue(testRoom.isCreator(USERS[0]))

        testRoom.setCreator(USERS[1])
        self.assertTrue(testRoom.hasUser(USERS[1]))
        self.assertTrue(testRoom.isCreator(USERS[1]))

    def test_is_creator_fail(self):
        testRoom = Room()
        testRoom.addUser(USERS[0])
        testRoom.setCreator(None)

        self.assertFalse(testRoom.isCreator(USERS[0]))

    def test_length(self):
        testRoom = Room()

        for testUser in USERS:
            testRoom.addUser(testUser)

        self.assertEqual(len(testRoom), len(USERS))

    def test_generateRoomId(self):
        random.seed(7883)
        self.assertEqual(Room().id, 'Zp5s_mMGCaTy')
