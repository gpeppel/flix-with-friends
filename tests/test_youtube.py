import random
import unittest

import app
import tests.helpers as helpers
from tests.helpers import MockRequest, hookSocketEmit


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

        with hookSocketEmit() as emitList:
            self.flaskserver.youtube_ns.handle_yt_load(mock_req, {})

            self.assertTrue(len(emitList) == 0)

            for vobj in YOUTUBE_VIDEO_IDS:
                self.flaskserver.youtube_ns.handle_yt_load(mock_req, {
                    'url': vobj[URL]
                })

                if len(emitList) == 0:
                    self.assertIsNone(vobj[ID])
                    continue

                emit = emitList.pop()

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

        with hookSocketEmit() as emitList:
            self.flaskserver.youtube_ns.connect_user(mock_req)
            emitList.clear()

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

                    emit = emitList.pop()

                    self.assertEqual(emit['event'], 'yt_state_change')

                    if isinstance(out_val, str) and out_val.startswith('eval:'):
                        out_val = eval(out_val[len('eval:'):])

                    self.assertEqual(emit['args'][0][key], out_val)

            self.flaskserver.youtube_ns.disconnect_user(mock_req)

    def test_handle_yt_state_change_fail(self):
        mock_req = MockRequest(TEST_SID)

        with hookSocketEmit() as emitList:
            self.flaskserver.youtube_ns.connect_user(mock_req)
            emitList.clear()

            for name in YT_STATE_NAMES_INVALID:
                self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, {
                    'state': name
                })

                self.assertTrue(len(emitList) == 0)

            self.flaskserver.youtube_ns.disconnect_user(mock_req)
