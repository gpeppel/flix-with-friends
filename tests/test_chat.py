from datetime import datetime
import unittest
import unittest.mock as mock

import app
from tests.helpers import connect_login_test_user, create_room, hook_socket_emit

INPUT_MESSAGE = 'message'
MESSAGE_EXPECTED = 'Message()_expected'

TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


class ChatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.create_flask_server(app.db)
        cls.flaskserver.test_login_enabled = True

    def setUp(self):
        self.success_tests = [
            {
                INPUT_MESSAGE: {
                    'text': 'test_message_text'
                },
                MESSAGE_EXPECTED: {
                    'message_id': None,
                    'text': 'test_message_text',
                    'timestamp': datetime.now(),
                    'room_id': '69cbaae81f874b36ae9e24be92f79006',
                    'user_id': None,
                }
            }
        ]

    def mocked_db_add(self, message):
        attribute_dict = {}
        message_dict = message.__dict__
        for key in message_dict.keys():
            if not key.startswith('_'):
                attribute_dict[key] = message_dict[key]
        return attribute_dict

    def test_parse_chat_message_success(self):
        with connect_login_test_user(self.flaskserver) as result:
            _, sio_client = result
            with create_room(self.flaskserver, sio_client):
                # TODO
                return

            with mock.patch('socketns.chat.ChatNamespace.add_to_db', self.mocked_db_add):
                for test in self.success_tests:
                    sio_client.emit('message_send', (
                        test[INPUT_MESSAGE]
                    ))
                    expected = test[MESSAGE_EXPECTED]

                    with hook_socket_emit() as emit_list:
                        emit = emit_list.pop()
                        for key, val in expected.items():
                            if key == 'timestamp':
                                self.assertTrue((emit['args'][key] - val).total_seconds() < 3)
                            else:
                                self.assertEqual(emit['args'][key], val)
