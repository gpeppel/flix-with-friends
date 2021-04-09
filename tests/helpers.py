from contextlib import contextmanager
import time
import unittest.mock as mock


@contextmanager
def connect_test_user(flaskserver):
    sio_client = None

    try:
        client = flaskserver.app.test_client()
        sio_client = flaskserver.socketio.test_client(flaskserver.app, flask_test_client=client)
        yield client, sio_client
    finally:
        if sio_client is not None:
            sio_client.disconnect()

@contextmanager
def connect_login_test_user(flaskserver):
    with connect_test_user(flaskserver) as result:
        client, sio_client = result
        client.get('/')

        sio_client.emit('login_test', {})
        user = flaskserver.get_user_by_sid(sio_client.sid)

        yield client, sio_client, user

@contextmanager
def create_room(flaskserver, sio_client):
    room = None

    try:
        sio_client.emit('room_create', {
            'playlist': '',
            'description': ''
        })

        user = flaskserver.get_user_by_sid(sio_client.sid)
        room = user.room
        yield room
    finally:
        if room is not None:
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
