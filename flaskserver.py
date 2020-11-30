import flask
import flask_socketio

from db_models.message import Message
from db_models.room import Room
from db_models.user import User

import socketns
import socketns.base
import socketns.chat
import socketns.login
import socketns.youtube
import socketns.room

MESSAGES_EMIT_CHANNEL = 'messages_received'


class FlaskServer:
    def __init__(self, app, db):
        self.app = app
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/debug', 'debug', self.debug)

        self.socketio = flask_socketio.SocketIO(self.app)
        self.socketio.init_app(self.app, cors_allowed_origins='*')

        self.db = db

        self.base_ns = socketns.base.BaseNamespace('/', self)
        self.chat_ns = socketns.chat.ChatNamespace('/', self)
        self.youtube_ns = socketns.youtube.YoutubeNamespace('/', self)
        self.login_ns = socketns.login.LoginNamespace('/', self)
        self.room_ns = socketns.room.RoomNamespace('/', self)

        self.socketio.on_namespace(socketns.CustomCombinedNamespace('/', self, [
            self.base_ns,
            self.chat_ns,
            self.youtube_ns,
            self.room_ns,
            self.login_ns
        ]))

        self.rooms = {}
        self.users = {}

    def run(self, host, port, debug=False):
        self.socketio.run(
            self.app,
            host=host,
            port=port,
            debug=debug
        )

    def index(self):
        return flask.render_template('index.html')

    def debug(self):
        rooms = {}
        users = {}

        for room_id, room in self.rooms.items():
            rooms[room_id] = room.serialize()
        for sid, user in self.users.items():
            users[sid] = user.serialize()

        return flask.render_template('debug.html',
            rooms=rooms,
            users=users
        )

    def emit_all_messages(self):
        if not self.db_connected():
            return

        cur = self.db.cursor()
        messages = Message.get_messages(cur, room_id=None)
        cur.close()

        self.socketio.emit(MESSAGES_EMIT_CHANNEL, list(map(
            lambda msg: msg.serialize(),
            messages
        )))

    def create_user_from_request(self, request):
        user = User.from_request(request)
        self.users[user.sid] = user

        return user

    def delete_user(self, user):
        del self.users[user.sid]

    def get_user_by_request(self, request):
        return self.users[request.sid]

    def create_room(self, room_id=None):
        room = Room(room_id)
        self.rooms[room.room_id] = room

        return room

    def delete_room(self, room):
        for user in list(room.users.values()):
            room.remove_user(user)

        del self.rooms[room.room_id]

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def db_connected(self):
        return self.db is not None and self.db.is_connected()
