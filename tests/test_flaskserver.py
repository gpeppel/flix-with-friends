import random
import unittest

import app
import tests.helpers as helpers
from tests.helpers import MockRequest, hookSocketEmit


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


class FlaskServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.createFlaskServer(app.db)

    def test_create_delete_user(self):
        mockReq = MockRequest(TEST_SID)
        user = self.flaskserver.createUserFromRequest(mockReq)

        self.assertEqual(user.id, TEST_SID)
        self.assertEqual(self.flaskserver.users[TEST_SID], user)

        self.flaskserver.deleteUser(user)
        self.assertFalse(TEST_SID in self.flaskserver.users)

    def test_create_delete_room(self):
        roomAbc = self.flaskserver.createRoom('abc')
        self.assertEqual(roomAbc.id, 'abc')
        self.assertEqual(self.flaskserver.rooms['abc'], roomAbc)

        random.seed(376)
        roomRand = self.flaskserver.createRoom()
        self.assertEqual(roomRand.id, 'z8lUM2xXA5pV')
        self.assertEqual(self.flaskserver.rooms['z8lUM2xXA5pV'], roomRand)

        self.flaskserver.deleteRoom(roomRand)
        self.assertFalse('z8lUM2xXA5pV' in self.flaskserver.rooms)

        mockReq = MockRequest(TEST_SID)
        user = self.flaskserver.createUserFromRequest(mockReq)
        roomAbc.addUser(user)

        self.flaskserver.deleteRoom(roomAbc)
        self.assertFalse('abc' in self.flaskserver.rooms)

        self.assertTrue(len(roomAbc) == 0)
