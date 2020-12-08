import datetime

import flask
import flask_socketio


class BaseNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_connect(self):
        self.connect_user(flask.request, flask.session)

    def connect_user(self, request, session):
        user = self.flaskserver.create_user_from_request(request, session)
        user.socket_connected = True
        user.last_socket_connect = None

    def on_disconnect(self):
        self.disconnect_user(flask.request, flask.session)

    def disconnect_user(self, request, session):
        user = self.flaskserver.get_user_by_request(request, session)
        if user is None:
            return

        room = user.room

        user.socket_connected = False
        user.last_socket_connect = datetime.datetime.utcnow()

        cur = self.flaskserver.db.cursor()
        user.remove_from_db(cur)
        self.flaskserver.db.commit()
        cur.close()

        self.flaskserver.delete_user(user)

        if room is not None:
            self.flaskserver.emit_room_info(room)
