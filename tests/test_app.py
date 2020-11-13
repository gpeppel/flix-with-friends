import unittest
import unittest.mock as mock

import tests.helpers as helpers
from tests.helpers import hookSocketEmit

import app


TEST_SID = '69cbaae81f874b36ae9e24be92f79006'


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
