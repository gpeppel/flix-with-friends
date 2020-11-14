import random
import unittest

import app
import tests.helpers as helpers
from tests.helpers import MockRequest, hook_socket_emit


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


class FlaskServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.create_flask_server(app.db)

    def test_create_delete_user(self):
        mock_req = MockRequest(TEST_SID)
        user = self.flaskserver.create_user_from_request(mock_req)

        self.assertEqual(user.id, TEST_SID)
        self.assertEqual(self.flaskserver.users[TEST_SID], user)

        self.flaskserver.delete_user(user)
        self.assertFalse(TEST_SID in self.flaskserver.users)

    def test_create_delete_room(self):
        room_abc = self.flaskserver.create_room('abc')
        self.assertEqual(room_abc.id, 'abc')
        self.assertEqual(self.flaskserver.rooms['abc'], room_abc)

        random.seed(376)
        room_rand = self.flaskserver.create_room()
        self.assertEqual(room_rand.id, 'z8lUM2xXA5pV')
        self.assertEqual(self.flaskserver.rooms['z8lUM2xXA5pV'], room_rand)

        self.flaskserver.delete_room(room_rand)
        self.assertFalse('z8lUM2xXA5pV' in self.flaskserver.rooms)

        mock_req = MockRequest(TEST_SID)
        user = self.flaskserver.create_user_from_request(mock_req)
        room_abc.add_user(user)

        self.flaskserver.delete_room(room_abc)
        self.assertFalse('abc' in self.flaskserver.rooms)

        self.assertTrue(len(room_abc) == 0)
