import unittest

import app
from tests.helpers import MockRequest, MockSession, hook_socket_emit
import utils


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'
TEST_SID2 = '0123456789abcdef'

URL = 'url'
ID = 'id'

YOUTUBE_VIDEO_IDS = [
    {
        URL: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
        ID: 'dQw4w9WgXcQ'
    },
    {
        URL: 'https://youtube.com/embed/dQw4w9WgXcQ',
        ID: 'dQw4w9WgXcQ'
    },
    {
        URL: 'youtu.be/dQw4w9WgXcQ',
        ID: 'dQw4w9WgXcQ'
    },
    {
        URL: 'dQw4w9WgXcQ',
        ID: 'dQw4w9WgXcQ'
    },
    {
        URL: 'http://example.com',
        ID: None
    }
]

INPUT = 'input'
OUTPUT = 'output'

YT_STATE_NAMES_VALID = [
    'ready',
    'rEaDy',
    'unstarted',
    'ended',
    'playing',
    'paused',
    'buffering',
    'cued',
    'playback'
]

YT_STATE_NAMES_INVALID = [
    'invalid'
]

YT_STATE_CHANGES = {
    'offset': [
        {
            INPUT: None,
            OUTPUT: 0
        },
        {
            INPUT: 0,
            OUTPUT: 0
        },
        {
            INPUT: -6,
            OUTPUT: 6
        },
        {
            INPUT: 6,
            OUTPUT: 6
        },
        {
            INPUT: 12.4,
            OUTPUT: 12.4
        },
        {
            INPUT: 'asdf',
            OUTPUT: 0
        }
    ],
    'rate': [
        {
            INPUT: None,
            OUTPUT: 1
        },
        {
            INPUT: 0,
            OUTPUT: 0
        },
        {
            INPUT: 'asdf',
            OUTPUT: 1
        },
        {
            INPUT: 0.5,
            OUTPUT: 0.5
        },
        {
            INPUT: 2,
            OUTPUT: 2
        },
    ],
    'runAt': [
        {
            INPUT: None,
            OUTPUT: 0
        },
        {
            INPUT: 0,
            OUTPUT: 0
        },
        {
            INPUT: -5,
            OUTPUT: -5
        },
        {
            INPUT: 'asdf',
            OUTPUT: 0
        },
    ],
    'timestamp': [
        {
            INPUT: None,
            OUTPUT: 'eval:utils.unix_timestamp()'
        },
        {
            INPUT: 0,
            OUTPUT: 0
        },
        {
            INPUT: 'asdf',
            OUTPUT: 'eval:utils.unix_timestamp()'
        },
        {
            INPUT: 100,
            OUTPUT: 100
        },
    ]
}

YT_SPHERE_UPDATES = {
    'properties.yaw': [
        {
            INPUT: None,
            OUTPUT: 0
        },
        {
            INPUT: -6,
            OUTPUT: 0
        },
        {
            INPUT: 6,
            OUTPUT: 6
        },
        {
            INPUT: 12.4,
            OUTPUT: 12.4
        },
        {
            INPUT: 'asdf',
            OUTPUT: 0
        }
    ],
    'properties.pitch|properties.roll': [
        {
            INPUT: None,
            OUTPUT: 0
        },
        {
            INPUT: -6,
            OUTPUT: -6
        },
        {
            INPUT: 6,
            OUTPUT: 6
        },
        {
            INPUT: 12.4,
            OUTPUT: 12.4
        },
        {
            INPUT: 'asdf',
            OUTPUT: 0
        }
    ],
    'properties.fov': [
        {
            INPUT: None,
            OUTPUT: 100
        },
        {
            INPUT: 'asdf',
            OUTPUT: 100
        },
        {
            INPUT: 0,
            OUTPUT: 30
        },
        {
            INPUT: 100,
            OUTPUT: 100
        },
        {
            INPUT: 80.5421,
            OUTPUT: 80.5421
        },
        {
            INPUT: 150,
            OUTPUT: 120
        },
    ]
}


class YoutubeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flaskserver = app.create_flask_server(app.db)

    def test_get_youtube_video_id(self):
        for vobj in YOUTUBE_VIDEO_IDS:
            self.assertEqual(
                self.flaskserver.youtube_ns.get_youtube_video_id(vobj[URL]),
                vobj[ID]
            )

    def test_handle_yt_load(self):
        mock_req = MockRequest(TEST_SID)
        mock_session = MockSession()

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req, mock_session)
            user = self.flaskserver.get_user_by_request(mock_req, mock_session)
            room = self.flaskserver.create_room(TEST_SID)
            room.add_user(user)
            room.set_creator(user)
            emit_list.clear()

            self.flaskserver.youtube_ns.handle_yt_load(mock_req, mock_session, {})

            self.assertTrue(len(emit_list) == 0)

            for vobj in YOUTUBE_VIDEO_IDS:
                self.flaskserver.youtube_ns.handle_yt_load(mock_req, mock_session, {
                    'url': vobj[URL]
                })

                if len(emit_list) == 0:
                    self.assertIsNone(vobj[ID])
                    continue

                emit = emit_list.pop()

                self.assertEqual(emit['event'], 'yt_load')
                self.assertEqual(emit['args'][0]['videoId'], vobj[ID])

            self.flaskserver.base_ns.disconnect_user(mock_req, mock_session)
            self.flaskserver.delete_room(room)

    def test_handle_yt_state_change_success(self):
        mock_req = MockRequest(TEST_SID)
        mock_session = MockSession()

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req, mock_session)
            user = self.flaskserver.get_user_by_request(mock_req, mock_session)
            room = self.flaskserver.create_room(TEST_SID)
            room.add_user(user)
            room.set_creator(user)
            emit_list.clear()

            for key, value_list in YT_STATE_CHANGES.items():
                state = {
                    'state': 'ready',
                    'offset': 0,
                    'rate': 1,
                    'runAt': 0,
                    'timestamp': 0
                }

                for val in value_list:
                    outval = self.get_outval(state, key, val[INPUT], val[OUTPUT])
                    self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, mock_session, state)
                    emit = emit_list.pop()

                    self.assertEqual(emit['event'], 'yt_state_change')

                    if key == 'timestamp':
                        self.assertTrue(int(outval) - utils.getval(emit['args'][0], key) < 5)
                    else:
                        self.assertEqual(utils.getval(emit['args'][0], key), outval)

            self.flaskserver.base_ns.disconnect_user(mock_req, mock_session)
            self.flaskserver.delete_room(room)

    def test_handle_yt_state_change_fail(self):
        mock_req = MockRequest(TEST_SID)
        mock_session = MockSession()

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req, mock_session)
            user = self.flaskserver.get_user_by_request(mock_req, mock_session)
            room = self.flaskserver.create_room(TEST_SID)
            room.add_user(user)
            emit_list.clear()

            for name in YT_STATE_NAMES_INVALID:
                self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, mock_session, {
                    'state': name
                })

                self.assertTrue(len(emit_list) == 0)

            self.flaskserver.base_ns.disconnect_user(mock_req, mock_session)
            self.flaskserver.delete_room(room)

    def test_handle_yt_sphere_update(self):
        mock_req = MockRequest(TEST_SID)
        mock_req2 = MockRequest(TEST_SID2)
        mock_session = MockSession()
        mock_session2 = MockSession()

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req, mock_session)
            self.flaskserver.base_ns.connect_user(mock_req2, mock_session2)

            user = self.flaskserver.get_user_by_request(mock_req, mock_session)
            user2 = self.flaskserver.get_user_by_request(mock_req2, mock_session2)
            room = self.flaskserver.create_room(TEST_SID)
            room.add_user(user)
            room.set_creator(user)
            room.add_user(user2)
            emit_list.clear()

            for key, value_list in YT_SPHERE_UPDATES.items():
                props = {
                    'properties': {
                        'yaw': 0,
                        'pitch': 0,
                        'roll': 0,
                        'fov': 100
                    }
                }

                for val in value_list:
                    outval = self.get_outval(props, key, val[INPUT], val[OUTPUT])
                    self.flaskserver.youtube_ns.handle_yt_sphere_update(mock_req, mock_session, props)
                    emit = emit_list.pop()

                    self.assertEqual(emit['event'], 'yt_sphere_update')

                    data = emit['args'][0]
                    for k in key.split('|'):
                        self.assertEqual(utils.getval(data, k), outval)

            self.flaskserver.base_ns.disconnect_user(mock_req, mock_session)
            self.flaskserver.base_ns.disconnect_user(mock_req2, mock_session2)
            self.flaskserver.delete_room(room)

    def get_outval(self, data, key, inval, outval):
        for k in key.split('|'):
            obj, last = utils.getdict(data, k)

            if inval is None:
                del obj[last]
            else:
                obj[last] = inval

        if isinstance(outval, str) and outval.startswith('eval:'):
            return eval(outval[len('eval:'):])
        return outval
