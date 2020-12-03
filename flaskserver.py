import json

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

import utils


COOKIE_SESSION_ID = 'session_id'
COOKIE_SESSION_TOKEN = 'session_token'

MESSAGES_EMIT_CHANNEL = 'messages_received'


class FlaskServer:
    def __init__(self, app, db):
        self.app = app
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/debug', 'debug', self.debug)
        self.app.add_url_rule('/debug.json', 'debug.json', self.debug_json)

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
        resp = flask.make_response(flask.render_template('index.html'))

        session_id = flask.request.cookies.get(COOKIE_SESSION_ID)
        if session_id is None:
            resp.set_cookie(COOKIE_SESSION_ID, utils.random_hex(32))

        session_token = flask.request.cookies.get(COOKIE_SESSION_TOKEN)
        if session_token is None:
            resp.set_cookie(COOKIE_SESSION_TOKEN, utils.random_hex(64))

        return resp

    def debug(self):
        return flask.render_template('debug.html')

    def debug_json(self):
        return flask.Response(
            json.dumps(self.get_debug_data()),
            mimetype='application/json'
        )

    def get_debug_data(self):
        data = {
            'rooms': {},
            'users': {}
        }
        rooms = data['rooms']
        users = data['users']

        for room_id, room in self.rooms.items():
            rooms[room_id] = room.serialize()
        for sid, user in self.users.items():
            users[sid] = user.serialize()

        return data

    def emit_all_messages(self, room):
        if not self.db_connected():
            return

        cur = self.db.cursor()
        messages = Message.get_messages(cur, room_id=room.room_id)
        cur.close()

        room.emit(MESSAGES_EMIT_CHANNEL, list(map(
            lambda msg: msg.serialize(),
            messages
        )))

    def create_user_from_request(self, request):
        user = self.get_user_by_request(request)
        if user is not None:
            user.sid = request.sid

        if user is None:
            user = User.from_request(request)
            self.users[user.get_session_id()] = user

        return user

    def delete_user(self, user):
        del self.users[user.get_session_id()]

    def get_user_by_request(self, request):
        session_id = request.cookies.get(COOKIE_SESSION_ID, request.sid)
        session_token = request.cookies.get(COOKIE_SESSION_TOKEN)

        user = self.users.get(session_id)
        if user is None or session_token != user.session_token:
            return None
        return user

    def create_room(self, room_id):
        if room_id in self.rooms:
            room = self.rooms[room_id]
        else:
            room = Room(self.socketio, room_id)
            self.rooms[room.room_id] = room

            if self.db_connected():
                cur = self.db.cursor()
                room.insert_to_db(cur)
                self.db.commit()
                cur.close()

        return room

    def delete_room(self, room):
        for user in list(room.users.values()):
            room.remove_user(user)

        del self.rooms[room.room_id]

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def db_connected(self):
        return self.db is not None and self.db.is_connected()
