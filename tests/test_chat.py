from datetime import datetime
import unittest
import unittest.mock as mock
import sys
import time

import app

INPUT_MESSAGE = 'message'
MESSAGE_EXPECTED = 'Message()_expected'


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
                    'id': 1,
                    'text': 'test_message_text',
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'room_id': 'room_id_here',
                    'user_id': 1,
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
        for test in self.success_tests:
            with mock.patch('socketns.youtube.YoutubeNamespace.add_to_db', self.mocked_db_add):
                mocked_id_generator.return_value = 1
                response = self.flaskserver.youtube_ns.on_message_send(
                    test[INPUT_MESSAGE])
                expected = test[MESSAGE_EXPECTED]

                self.assertEqual(response, expected)
