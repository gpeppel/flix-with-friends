import flask
import flask_socketio

from db_models.message import Message
from db_models.room import Room
from db_models.user import User

import socketns.youtube


MESSAGES_EMIT_CHANNEL = 'messages_received'


class FlaskServer:
    def __init__(self, app, db):
        self.app = app
        self.app.add_url_rule('/', 'index', self.index)

        self.socketio = flask_socketio.SocketIO(self.app)
        self.socketio.init_app(self.app, cors_allowed_origins='*')

        self.db = db

        self.youtube_ns = socketns.youtube.YoutubeNamespace('/', self)
        self.socketio.on_namespace(self.youtube_ns)

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

    def emit_all_messages(self, channel):
        all_messages = [
            # TODO decide if userId should even be sent to clients
            (db_message.id, db_message.text, str(
                db_message.timestamp), db_message.user_id)
            for db_message in self.db.session.query(Message).all()
        ]
        self.socketio.emit(MESSAGES_EMIT_CHANNEL, all_messages)

    def create_user_from_request(self, request):
        user = User.from_request(request)
        self.users[user.id] = user

        return user

    def delete_user(self, user):
        del self.users[user.id]

    def get_user_by_request(self, request):
        return self.users[request.sid]

    def create_room(self, room_id=None):
        room = Room(room_id)
        self.rooms[room.id] = room

        return room

    def delete_room(self, room):
        for user in list(room.users.values()):
            room.remove_user(user)

        del self.rooms[room.id]
