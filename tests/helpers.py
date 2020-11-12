from contextlib import contextmanager
import unittest.mock as mock


# https://docs.python.org/2.5/whatsnew/pep-343.html
@contextmanager
def hookSocketEmit(request=None):
	emitList = []

	def emit(event, *args, **kwargs):
		emitList.append({
			'event': event,
			'args': args
		})

	with mock.patch('flask_socketio.SocketIO.emit', wraps=emit):
		yield emitList
