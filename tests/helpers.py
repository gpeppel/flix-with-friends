from contextlib import contextmanager
import unittest.mock as mock

def connect_test_user(flaskserver):
    client = flaskserver.app.test_client()
    sio_client = flaskserver.socketio.test_client(flaskserver.app, flask_test_client=client)
    return client, sio_client
def connect_login_test_user(flaskserver):
    client, sio_client = connect_test_user(flaskserver)
    sio_client.emit('login_test', {})

    return client, sio_client

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
