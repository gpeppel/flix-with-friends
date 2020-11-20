import random
import unittest

import app
import tests.helpers as helpers
from tests.helpers import MockRequest, hook_socket_emit


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'

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
            OUTPUT: 'eval:self.flaskserver.youtube_ns.unix_timestamp()'
        },
        {
            INPUT: 0,
            OUTPUT: 0
        },
        {
            INPUT: 'asdf',
            OUTPUT: 'eval:self.flaskserver.youtube_ns.unix_timestamp()'
        },
        {
            INPUT: 100,
            OUTPUT: 100
        },
    ]
}

YT_SPHERE_UPDATES = {
    'angle': [
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
    'fov': [
        {
            INPUT: None,
            OUTPUT: 100
        },
        {
            INPUT: 0,
            OUTPUT: 30
        },
        {
            INPUT: 'asdf',
            OUTPUT: 100
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

        with hook_socket_emit() as emit_list:
            self.flaskserver.youtube_ns.handle_yt_load(mock_req, {})

            self.assertTrue(len(emit_list) == 0)

            for vobj in YOUTUBE_VIDEO_IDS:
                self.flaskserver.youtube_ns.handle_yt_load(mock_req, {
                    'url': vobj[URL]
                })

                if len(emit_list) == 0:
                    self.assertIsNone(vobj[ID])
                    continue

                emit = emit_list.pop()

                self.assertEqual(emit['event'], 'yt_load')
                self.assertEqual(emit['args'][0]['videoId'], vobj[ID])

    def test_handle_yt_state_change_success(self):
        def get_state_template():
            return {
                'state': 'ready',
                'offset': 0,
                'rate': 1,
                'runAt': 0,
                'timestamp': 0
            }

        mock_req = MockRequest(TEST_SID)

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req)
            emit_list.clear()

            for key, value_list in YT_STATE_CHANGES.items():
                state = get_state_template()

                for val in value_list:
                    in_val = val[INPUT]
                    out_val = val[OUTPUT]

                    if in_val is None:
                        if key in state:
                            del state[key]
                    else:
                        state[key] = in_val

                    self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, state)

                    emit = emit_list.pop()

                    self.assertEqual(emit['event'], 'yt_state_change')

                    if isinstance(out_val, str) and out_val.startswith('eval:'):
                        out_val = eval(out_val[len('eval:'):])

                    if key == 'timestamp':
                        self.assertTrue(int(out_val) - emit['args'][0][key] < 5)
                    else:
                        self.assertEqual(emit['args'][0][key], out_val)

            self.flaskserver.base_ns.disconnect_user(mock_req)

    def test_handle_yt_state_change_fail(self):
        mock_req = MockRequest(TEST_SID)

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req)
            emit_list.clear()

            for name in YT_STATE_NAMES_INVALID:
                self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, {
                    'state': name
                })

                self.assertTrue(len(emit_list) == 0)

            self.flaskserver.base_ns.disconnect_user(mock_req)

    def test_handle_yt_sphere_update(self):
        def get_sphere_update_template():
            return {
                'properties': {
                    'yaw': 0,
                    'pitch': 0,
                    'roll': 0,
                    'fov': 100
                }
            }

        mock_req = MockRequest(TEST_SID)

        with hook_socket_emit() as emit_list:
            self.flaskserver.base_ns.connect_user(mock_req)
            emit_list.clear()

            for key, value_list in YT_SPHERE_UPDATES.items():
                state = get_sphere_update_template()

                for val in value_list:
                    in_val = val[INPUT]
                    out_val = val[OUTPUT]

                    if in_val is None:
                        if key == 'angle':
                            if 'yaw' in state:
                                del state['properties']['yaw']
                            if 'pitch' in state:
                                del state['properties']['pitch']
                            if 'roll' in state:
                                del state['properties']['roll']
                        else:
                            if key in state:
                                del state['properties'][key]
                    else:
                        if key == 'angle':
                            state['properties']['yaw'] = in_val
                            state['properties']['pitch'] = in_val
                            state['properties']['roll'] = in_val
                        else:
                            state['properties'][key] = in_val

                    self.flaskserver.youtube_ns.handle_yt_sphere_update(mock_req, state)

                    emit = emit_list.pop()

                    self.assertEqual(emit['event'], 'yt_sphere_update')

                    print(emit['args'])

                    if key == 'angle':
                        self.assertEqual(emit['args'][0]['properties']['yaw'], out_val)
                        self.assertEqual(emit['args'][0]['properties']['pitch'], out_val)
                        self.assertEqual(emit['args'][0]['properties']['roll'], out_val)
                    else:
                        self.assertEqual(emit['args'][0]['properties'][key], out_val)

            self.flaskserver.base_ns.disconnect_user(mock_req)
