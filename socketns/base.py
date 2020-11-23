import datetime

import flask
import flask_socketio


class BaseNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_connect(self):
        self.connect_user(flask.request)

    def connect_user(self, request):
        print('!' * 16, 'connect', request.sid)
        user = self.flaskserver.create_user_from_request(request)
        user.socket_connected = True
        user.last_socket_connect = None

    def on_disconnect(self):
        self.disconnect_user(flask.request)

    def disconnect_user(self, request):
        print('!' * 16, 'connect', request.sid)
        user = self.flaskserver.get_user_by_request(request)
        user.socket_connected = False
        user.last_socket_connect = datetime.datetime.utcnow()
        # delete on logout
        #self.flaskserver.delete_user(user)
