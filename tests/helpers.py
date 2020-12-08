from contextlib import contextmanager
import unittest.mock as mock


@contextmanager
def connect_test_user(flaskserver):
    try:
        client = flaskserver.app.test_client()
        sio_client = flaskserver.socketio.test_client(flaskserver.app, flask_test_client=client)
        yield client, sio_client
    finally:
        sio_client.disconnect()

@contextmanager
def connect_login_test_user(flaskserver):
    with connect_test_user(flaskserver) as result:
        client, sio_client = result
        sio_client.emit('login_test', {})

        yield client, sio_client

@contextmanager
def create_room(flaskserver, sio_client):
    try:
        sio_client.emit('room_create', {
            'playlist': '',
            'description': ''
        })

        user = flaskserver.get_user_by_session_id(sio_client.sid)
        room = user.room
        yield room
    finally:
        flaskserver.delete_room(room)

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
