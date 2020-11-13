import random
import unittest

import app


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
		cls.flaskserver = app.createFlaskServer(app.app, app.db)


	def test_get_youtube_video_id(self):
		for vobj in YOUTUBE_VIDEO_IDS:
			self.assertEqual(self.flaskserver.youtubeNs.getYoutubeVideoId(vobj[URL]), vobj[ID])
