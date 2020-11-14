from contextlib import contextmanager
import unittest.mock as mock


class MockRequest:
    def __init__(self, sid):
        self.sid = sid


# https://docs.python.org/2.5/whatsnew/pep-343.html
@contextmanager
def hook_socket_emit(request=None):
    emit_list = []

    def emit(event, *args, **kwargs):
        emit_list.append({
            'event': event,
            'args': args
        })

    with mock.patch('flask_socketio.SocketIO.emit', wraps=emit):
        yield emit_list
