import flask
import flask_socketio


class RoomNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_room_create(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)
        room = self.flaskserver.create_room()

        room.add_user(user)
        room.set_creator(user)

        return {
            'status': 'ok',
            'roomId': room.room_id,
            'roomName': data['roomName']
        }

    def on_room_join(self, data):
        print(data)

        user = self.flaskserver.get_user_by_request(flask.request)
        room = self.flaskserver.get_room(data['roomId'])

        if room is None:
            return {
                'status': 'fail',
                'error': 'noexist'
            }

        room.add_user(user)

        self.flaskserver.emit_all_messages()

        for member in room.users:
            self.flaskserver.socketio.emit('user_join', {
                'user_id': user.user_id,
                'username': user.username
            }, room=member.sid)

        return {
            'status': 'ok',
        }
