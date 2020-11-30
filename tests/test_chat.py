from datetime import datetime
import unittest
import unittest.mock as mock
import sys
import time

import app
from tests.helpers import MockRequest

INPUT_MESSAGE = 'message'
MESSAGE_EXPECTED = 'Message()_expected'

TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


class ChatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.create_flask_server(app.db)

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
                    'room_id': 'testroom',
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

    @mock.patch('random.randint')
    def test_parse_chat_message_success(self, mocked_id_generator):
        mock_req = MockRequest(TEST_SID)
        user = self.flaskserver.create_user_from_request(mock_req)

        with mock.patch('flask.request', mock_req):
            with mock.patch('socketns.chat.ChatNamespace.add_to_db', self.mocked_db_add):
                for test in self.success_tests:
                    mocked_id_generator.return_value = 1
                    response = self.flaskserver.chat_ns.on_message_send(
                        test[INPUT_MESSAGE])
                    expected = test[MESSAGE_EXPECTED]

                    for key, val in expected.items():
                        if key == 'timestamp':
                            self.assertTrue((response[key] - val).total_seconds() < 3)
                        else:
                            self.assertEqual(response[key], val)
