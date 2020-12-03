import random
import unittest

from db_models.room import Room
from db_models.user import User


INPUT = 'input'
OUTPUT = 'output'

USERS = [
    User(None, sid='01234567890'),
    User(None, sid='abcdef'),
    User(None, sid='a1b2c3d4e5f6'),
]

THRESHOLD = 'threshold'
USER_COUNT = 'user_count'
REACHES_VOTE_THRESHOLDS = [
    {
        INPUT: 3,
        THRESHOLD: 0,
        OUTPUT: False
    },
    {
        INPUT: 0,
        THRESHOLD: 0,
        OUTPUT: False
    },
    {
        INPUT: 4,
        THRESHOLD: 2,
        OUTPUT: True
    },
    {
        INPUT: 1,
        THRESHOLD: 2,
        OUTPUT: False
    },
    {
        INPUT: 6,
        THRESHOLD: 0.5,
        USER_COUNT: 10,
        OUTPUT: True
    },
    {
        INPUT: 4,
        THRESHOLD: 0.5,
        USER_COUNT: 10,
        OUTPUT: False
    },
]


class RoomTest(unittest.TestCase):
    def test_add_users(self):
        test_room = Room(None, None)

        for test_user in USERS:
            test_room.add_user(test_user)
            self.assertTrue(test_room.has_user(test_user))

    def test_remove_users_success(self):
        test_room = Room(None, None)

        for test_user in USERS:
            test_room.add_user(test_user)

        test_room.remove_user(USERS[0])
        self.assertFalse(test_room.has_user(USERS[0]))

    def test_remove_users_fail(self):
        test_room = Room(None, None)
        test_room.add_user(USERS[0])

        test_room.remove_user(USERS[1])
        self.assertFalse(test_room.has_user(USERS[1]))

    def test_empty_room(self):
        test_room = Room(None, None)
        test_room.add_user(USERS[0])

        test_room.empty_room()
        self.assertTrue(len(test_room) == 0)

    def test_is_creator_success(self):
        test_room = Room(None, None)
        test_room.add_user(USERS[0])
        test_room.set_creator(USERS[0])

        self.assertTrue(test_room.is_creator(USERS[0]))

        test_room.set_creator(USERS[1])
        self.assertTrue(test_room.has_user(USERS[1]))
        self.assertTrue(test_room.is_creator(USERS[1]))

    def test_is_creator_fail(self):
        test_room = Room(None, None)
        test_room.add_user(USERS[0])
        test_room.set_creator(None)

        self.assertFalse(test_room.is_creator(USERS[0]))

    def test_reaches_vote_threshold(self):
        test_room = Room(None, None)
        for entry in REACHES_VOTE_THRESHOLDS:
            if USER_COUNT in entry:
                for i in range(entry[USER_COUNT]):
                    test_room.add_user(User(None, sid=i))

            test_room.vote_threshold = entry[THRESHOLD]
            self.assertEqual(test_room.reaches_vote_threshold(entry[INPUT]), entry[OUTPUT])

            if len(test_room) != 0:
                test_room.empty_room()

    def test_length(self):
        test_room = Room(None, None)

        for test_user in USERS:
            test_room.add_user(test_user)

        self.assertEqual(len(test_room), len(USERS))

    def test_generate_room_id(self):
        random.seed(7883)
        self.assertEqual(Room(None, None).room_code, 'Zp5s_mMGCaTykVbk')
