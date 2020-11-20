import unittest

import app
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
    'properties.yaw|properties.pitch|properties.roll': [
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
    'properties.fov': [
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
                    outvals = self.f(state, key, val[INPUT], val[OUTPUT])

                    self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, state)

                    emit = emit_list.pop()

                    self.assertEqual(emit['event'], 'yt_state_change')

                    for outval in outvals:
                        if key == 'timestamp':
                            self.assertTrue(int(outval) - self.getval(emit['args'][0], key) < 5)
                        else:
                            self.assertEqual(self.getval(emit['args'][0], key), outval)

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
                    outvals = self.f(state, key, val[INPUT], val[OUTPUT])

                    self.flaskserver.youtube_ns.handle_yt_sphere_update(mock_req, state)

                    emit = emit_list.pop()

                    self.assertEqual(emit['event'], 'yt_sphere_update')

                    data = emit['args'][0]
                    if key == 'properties.yaw|properties.pitch|properties.roll':
                        self.assertEqual(self.getval(data, 'properties.yaw'), outvals[0])
                        self.assertEqual(self.getval(data, 'properties.pitch'), outvals[0])
                        self.assertEqual(self.getval(data, 'properties.roll'), outvals[0])
                    else:
                        self.assertEqual(self.getval(data, 'properties.fov'), outvals[0])

            self.flaskserver.base_ns.disconnect_user(mock_req)

    def getval(self, data, key, default=None):
        obj = data
        spl = key.split('.')
        for i in range(0, len(spl) - 1):
            if spl[i] not in obj:
                return default
            obj = obj[spl[i]]

        return obj.get(spl[-1], default)

    def f(self, data, key, inval, outval):
        values = []

        for k in key.split('|'):
            obj = data
            spl = k.split('.')
            for i in range(0, len(spl) - 1):
                obj = obj[spl[i]]

            if inval is None:
                del obj[spl[-1]]
            else:
                obj[spl[-1]] = inval

            if isinstance(outval, str) and outval.startswith('eval:'):
                outval = eval(outval[len('eval:'):])
            values.append(outval)
        return values
