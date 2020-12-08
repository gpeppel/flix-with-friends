import datetime

import flask
import flask_socketio


class BaseNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_connect(self):
        print('----------------------')
        print('...Socket Connected...')
        print('----------------------')
        self.connect_user(flask.request)

    def connect_user(self, request):
        user = self.flaskserver.create_user_from_request(request)
        user.socket_connected = True
        user.last_socket_connect = None
        print('----------------------')
        print(str(user.username) + ' connected')
        print('inside connect_user')
        print('----------------------')

    def on_disconnect(self):
        print('-------------------------')
        print('...Socket Disconnected...')
        print('-------------------------')
        self.disconnect_user(flask.request)
        

    def disconnect_user(self, request):
        user = self.flaskserver.get_user_by_request(request)
        room = user.room
        if user is None or user == False:
            return
       
        print('---------------------------')
        print('Inside disconnect_user -->' + print(str(user.username)))
        print('Room ---> ' + str(room))
        print('---------------------------')

        user.socket_connected = False
        user.last_socket_connect = datetime.datetime.utcnow()

        host = False
        if user.room.is_creator(user):
            host = True

        if user.room is None:
            pass
        else:
            if host:
                user.room.set_random_host()
            user.room.remove_user(user)

        cur = self.flaskserver.db.cursor()
        user.remove_from_db(cur)
        self.flaskserver.db.commit()
        cur.close()
        self.flaskserver.emit_room_info(room)
