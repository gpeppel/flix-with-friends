from contextlib import contextmanager
import unittest.mock as mock

import utils


class MockRequest:
    def __init__(self, sid):
        self.sid = sid

        self.cookies = {}

    def set_cookie(self, key, val):
        self.cookies[key] = val

class MockSession:
    def __init__(self):
        self.session = {
            'id': utils.random_hex(32)
        }

    def get(self, key, default=None):
        return self.session.get(key, default)

    def __contains__(self, key):
        return key in self.session

    def __getitem__(self, key):
        return self.session[key]

    def __setitem__(self, key, val):
        self.session[key] = val

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
