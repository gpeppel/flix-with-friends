import json
import os

from dotenv import load_dotenv
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

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask.env')
load_dotenv(dotenv_path)


COOKIE_SESSION_ID = 'sessionId'
MESSAGES_EMIT_CHANNEL = 'messages_received'

DEBUG = True

class FlaskServer:
    def __init__(self, app, db):
        self.app = app
        self.app.add_url_rule('/', 'index', self.index)

        if DEBUG:
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

        self.room_alias = {}

        self.test_login_enabled = False

    def run(self, host, port, debug=False):
        self.socketio.run(
            self.app,
            host=host,
            port=port,
            debug=debug
        )

    def index(self):
        resp = flask.make_response(flask.render_template('index.html'))
        if flask.request.cookies.get(COOKIE_SESSION_ID) is None:
            resp.set_cookie(COOKIE_SESSION_ID, User.create_session_id())

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

    def emit_playlist(self, room_id):
        if not self.db_connected():
            return

        cur = self.db.cursor()
        playlist = self.get_playlist_from_room_id(cur, room_id)
        playlist_id = playlist['playlist_id']

        videos = self.get_videos_from_playlist_id(cur, playlist_id)
        video_list = []

        for video in videos:
            video_list.append({
                'video_id': video['video_id'],
                'video_source': video['video_source']
            })

        room = self.get_room(room_id)
        room.emit('queue_updated', {
            'videos': video_list
        })

    def create_user_from_request(self, request, session):
        user = self.get_user_by_request(request, session)
        if user is not None:
            user.sid = request.sid

        if user is None:
            user = User.from_request(request, session)

        session_id = request.cookies.get(COOKIE_SESSION_ID)
        if session_id is None:
            session_id = User.create_session_id()
            #raise Exception()

        user.session_id = session_id
        self.users[user.get_session_id()] = user

        return user

    def delete_user(self, user):
        if user.room is not None:
            user.room.remove_user(user)

        del self.users[user.get_session_id()]
        user.session_id = None

    def get_user_by_request(self, request, session):
        session_id = request.cookies.get(COOKIE_SESSION_ID)
        if session_id is None:
            if not hasattr(request, 'sid'):
                return None
            return self.get_user_by_sid(request.sid)

        user = self.get_user_by_session_id(session_id)
        if user is not None and hasattr(request, 'sid'):
            user.sid = request.sid

        return user

    def get_user_by_session_id(self, session_id):
        return self.users.get(session_id)

    def get_user_by_sid(self, sid):
        for _, user in self.users.items():
            if user.sid == sid:
                return user
        return None

    def emit_room_info(self, room):
        room_info_dict = room.serialize()

        room.emit('room_info_received', {
            'room_info': room_info_dict
        })

    def create_room(self, room_id):
        if room_id in self.rooms:
            room = self.rooms[room_id]
        else:
            room = Room(self.socketio, room_id)
            self.rooms[room.room_id] = room
            self.room_alias[room.room_code] = room

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
        del self.room_alias[room.room_code]

    def get_room(self, room_id):
        room = self.room_alias.get(room_id)
        if room is not None:
            return room
        return self.rooms.get(room_id)

    def db_connected(self):
        return self.db is not None and self.db.is_connected()

    def get_playlist_from_room_id(self, cur, room_id):
        cur.execute("""
            SELECT * FROM room_video_playlist
            WHERE room_video_playlist.room_id = %s;
        """, (room_id,))
        result = cur.fetchone()
        return result

    def get_videos_from_playlist_id(self, cur, playlist_id):
        cur.execute("""
            SELECT * FROM video
            WHERE video.playlist_id = %s;
        """, (playlist_id,))
        result = cur.fetchall()
        return result
