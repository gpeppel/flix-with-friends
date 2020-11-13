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
        mock_req = MockRequest(TEST_SID)

        with hookSocketEmit() as emitList:
            self.flaskserver.youtube_ns.connect_user(mock_req)
            self.flaskserver.youtube_ns.handle_yt_state_change(mock_req, test_data)

            print(emitList)

            # TODO

            self.flaskserver.youtube_ns.disconnect_user(mock_req)
