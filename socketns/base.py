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
        print("base connect", request.sid)
        self.flaskserver.create_user_from_request(request)

    def on_disconnect(self):
        self.disconnect_user(flask.request)

    def disconnect_user(self, request):
        print("base disconnect", request.sid)
        user = self.flaskserver.get_user_by_request(request)
        self.flaskserver.delete_user(user)
