import flask
import flask_socketio


ROOM_SETTINGS_GET = 'room_settings_get'
from db_models.room_video_playlist import RoomVideoPlaylist


class RoomNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_room_create(self, data):
        print(data)
        user = self.flaskserver.get_user_by_request(flask.request)
        if not user.is_authenticated():
            return {
                'status': 'fail'
            }

        room = self.flaskserver.create_room(user.get_session_id())
        playlist = RoomVideoPlaylist.from_room_id(room.room_id)
        cur = self.flaskserver.db.cursor()
        playlist.insert_to_db(cur)
        self.flaskserver.db.commit()
        cur.close()

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
        if not user.is_authenticated():
            return {
                'status': 'fail',
                'error': 'authenticated'
            }

        room = self.flaskserver.get_room(data.get('roomId'))

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

    def on_user_join(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)
        if not user.is_authenticated() or user.room is None:
            return

        user.room.emit(ROOM_SETTINGS_GET, user.room.get_settings())
        self.flaskserver.emit_all_messages(user.room)

    def on_room_settings_set(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)
        if not user.is_authenticated() or user.room is None:
            return{
                'status': 'fail',
                'error': 'Not authenticated.'
            }

        if not user.room.is_creator(user):
            self.flaskserver.socketio.emit(
                ROOM_SETTINGS_GET,
                user.room.get_settings(),
                room=user.sid
            )
            return {
                'status': 'fail',
                'error': 'You are not the room host.'
            }

        if 'hostMode' in data:
            user.room.set_host_mode(data['hostMode'])

        try:
            user.room.set_vote_threshold(data['voteThreshold'])
        except:
            pass

        if 'usersAddVideoEnabled' in data:
            user.room.set_users_can_add_video(data['usersAddVideoEnabled'])

        user.room.emit(ROOM_SETTINGS_GET, user.room.get_settings())

        return {
            'status': 'ok'
        }
