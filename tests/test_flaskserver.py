import unittest

import app
from tests.helpers import connect_login_test_user


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


class FlaskServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.create_flask_server(app.db)
        cls.flaskserver.test_login_enabled = True

    def test_create_delete_user(self):
        _, sio_client = connect_login_test_user(self.flaskserver)
        user = self.flaskserver.get_user_by_session_id(sio_client.sid)

        self.assertEqual(user.sid, sio_client.sid)
        self.flaskserver.delete_user(user)
        self.assertIsNone(self.flaskserver.get_user_by_session_id(sio_client.sid))

    def test_create_delete_room(self):
        room_abc = self.flaskserver.create_room('abc')
        self.assertEqual(room_abc.room_id, 'abc')
        self.assertEqual(self.flaskserver.rooms['abc'], room_abc)

        _, sio_client = connect_login_test_user(self.flaskserver)
        user = self.flaskserver.get_user_by_session_id(sio_client.sid)
        room_abc.add_user(user)

        self.assertTrue(len(room_abc) == 1)

        self.flaskserver.delete_room(room_abc)
        self.assertFalse('abc' in self.flaskserver.rooms)

        self.assertTrue(len(room_abc) == 0)
