import unittest

import app
from tests.helpers import MockRequest


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


class FlaskServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.create_flask_server(app.db)

    def test_create_delete_user(self):
        mock_req = MockRequest(TEST_SID)
        user = self.flaskserver.create_user_from_request(mock_req)

        self.assertEqual(user.sid, TEST_SID)
        self.assertEqual(self.flaskserver.users[TEST_SID], user)

        self.flaskserver.delete_user(user)
        self.assertFalse(TEST_SID in self.flaskserver.users)

    def test_create_delete_room(self):
        room_abc = self.flaskserver.create_room('abc')
        self.assertEqual(room_abc.room_id, 'abc')
        self.assertEqual(self.flaskserver.rooms['abc'], room_abc)

        mock_req = MockRequest(TEST_SID)
        user = self.flaskserver.create_user_from_request(mock_req)
        room_abc.add_user(user)

        self.assertTrue(len(room_abc) == 1)

        self.flaskserver.delete_room(room_abc)
        self.assertFalse('abc' in self.flaskserver.rooms)

        self.assertTrue(len(room_abc) == 0)
