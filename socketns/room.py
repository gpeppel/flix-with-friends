import flask
import flask_socketio


ROOM_SETTINGS_GET = 'room_settings_get'


class RoomNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_room_create(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)
        room = self.flaskserver.create_room(user.get_session_id())

        room.add_user(user)
        room.set_creator(user)

        room.current_video_code = data['playlist'][0]
        if len(room.current_video_code) == 0:
            room.current_video_code = 'dQw4w9WgXcQ'

        return {
            'status': 'ok',
            'room_id': room.room_id,
            'description': data['description'],
            'current_video_code': room.get_current_video_code()
        }

    def on_room_join(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)
        room = self.flaskserver.get_room(data['roomId'])

        if room is None:
            return {
                'status': 'fail',
                'error': 'noexist'
            }

        room.add_user(user)

        room.emit('user_join', {
            'user_id': user.user_id,
            'username': user.username
        })

        return {
            'status': 'ok',
            'room_id': room.room_id,
            'description': room.description,
            'current_video_code': room.get_current_video_code()
        }

    def on_room_settings_set(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)

        try:
            user.room.set_vote_threshold(data['voteThreshold'])
        except:
            pass

        user.room.emit(ROOM_SETTINGS_GET, {})
