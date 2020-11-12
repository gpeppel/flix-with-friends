import unittest
import unittest.mock as mock

import tests.helpers as helpers
from tests.helpers import hookSocketEmit

import app


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


class MockRequest:
	def __init__(self, sid):
		self.sid = sid

class AppTest(unittest.TestCase):
	def test_handle_yt_state_change(self):
		testData = {
			'state': 'unstarted'
		}

		mockReq = MockRequest(TEST_SID)

		with hookSocketEmit() as emitList:
			app.connectUser(mockReq)
			app.handleYtStateChange(mockReq, testData)

			print(emitList)

			# TODO

			app.disconnectUser(mockReq)


	def test_get_youtube_video_id(self):
		for vobj in YOUTUBE_VIDEO_IDS:
			self.assertEqual(app.getYoutubeVideoId(vobj[URL]), vobj[ID])
