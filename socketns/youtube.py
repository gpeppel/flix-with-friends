import datetime
import json
import re
import random
import sys

import flask
import flask_socketio

import flaskserver
from db_models.message import Message


EVENT_YT_STATE_CHANGE = 'yt_state_change'
MESSAGES_EMIT_CHANNEL = 'messages_received'


class YoutubeNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_connect(self):
        self.connect_user(flask.request)
        self.flaskserver.emit_all_messages(flaskserver.MESSAGES_EMIT_CHANNEL)

    def connect_user(self, request):
        self.flaskserver.create_user_from_request(request)

    def on_disconnect(self):
        self.disconnect_user(flask.request)

    def disconnect_user(self, request):
        user = self.flaskserver.get_user_by_request(request)
        self.flaskserver.delete_user(user)

    def on_new_temp_user(self, data):
        # db.session.add(tables.Users(data['name'], data['email'], data['username']))
        # db.session.commit()
        print("Got an event for new temp user input with data:", data)

    def on_new_facebook_user(self, data):
        key = 'status'
        if key in data['response'].keys():
            self.flaskserver.socketio.emit('unverified_user')
        else:
            self.flaskserver.socketio.emit('verified_user')
        
            user = self.flaskserver.create_user_from_request(flask.request)
            self.flaskserver.db.session.add(user)
        
            user.name = data['response']['name']
            # user.email = data['response']['email']
            user.image_url = data['response']['picture']['data']['url']
            user.settings = None
            user.oauth_id = data['response']['id']
            user.oauth_type = 'FACEBOOK'
        
            self.flaskserver.db.session.add(user)
            self.flaskserver.db.session.commit()

    def new_user_handler(self, data):
        # db.session.add(tables.Users(data['username'], data['password']))
        # db.session.commit()
        self.flaskserver.socketio.emit('new_user_recieved')

    # TODO - GET ACCESSS TOKEN FROM USER

    def handle_user_status(self, data):
        # TODO
        # for user in db.session.query(tables.Users).all():
        #     if user.username == data['username'] and user.password == data['password']:
        #         print('existing_user')
        #         socketio.emit('existing_user', {'status' : True , 'username': data['username']} )
        #         socketio.emit
        #         db.session.commit()
        #         break
        #     else:
        #         if user.username == data['username'] and user.password != data['password']:
        #             print('wrong_password')
        #             socketio.emit('wrong_password', { 'status' : False })
        #             break
        #         if user.username != data['username'] and user.password != data['password']:
        #             print('new_user')
        #             newUserHandler(data)
        #             socketio.emit('existing_user',  { 'status' : True })
        #             break
        self.flaskserver.db.session.commit()

    def on_chat_loaded(self):
        print('\n\n\nCHAT_LOADED\n\n\n')
        self.flaskserver.emit_all_messages(MESSAGES_EMIT_CHANNEL)

    def add_to_db(self, message_to_add):
        self.flaskserver.db.session.add(message_to_add)
        self.flaskserver.db.session.commit()
        self.flaskserver.emit_all_messages(MESSAGES_EMIT_CHANNEL)

    def on_message_send(self, data):
        user_request = flask.request
        
        user_from_request = self.flaskserver.get_user_by_request(user_request)
        self.flaskserver.db.session.add(user_from_request)
        user_oauth_id = user_from_request.oauth_id
        
        text = data['text']
        message_id = random.randint(1 - sys.maxsize, sys.maxsize) # TODO use an agreed upon id scheme
        user_id = user_oauth_id
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        room_id = 'room_id_here' # TODO use actual room id
        
        print('\nAdding message to database:')
        print('messageId:%s' % message_id)
        print('text: %s' % text)
        print('timestamp: %s' % timestamp)
        print('roomId: %s' % room_id)
        print('userId: %s\n' % user_id)
        
        message_to_add = Message(message_id, text, timestamp, room_id, user_id)
        return self.add_to_db(message_to_add)
    
    def on_yt_load(self, data):
        url = data.get('url')
        if url is None:
            return

        video_id = self.get_youtube_video_id(url)
        if video_id is None:
            return

        self.flaskserver.socketio.emit('yt_load', {
            'videoId': video_id
        })

    def get_youtube_video_id(self, url):
        match = re.match(
            r'^(?:https?://)?(?:www\.)?youtu(?:\.be/|be\.com/(?:embed/|watch\?v=))([A-Za-z0-9_-]+)',
            url
        )
        if match is not None:
            return match[1]

        match = re.match(r'^([A-Za-z0-9_-]+)$', url)
        if match is not None:
            return match[1]

        return None

    def on_yt_state_change(self, data):
        self.handle_yt_state_change(flask.request, data)

    def handle_yt_state_change(self, request, data):
        user = self.flaskserver.get_user_by_request(request)

        print(
            json.dumps(data).encode(
                "ascii", errors="backslashreplace").decode("ascii")
        )

        def getval(key, fnc_chk, fnc_fix, default=None):
            val = data.get(key, default)
            if not fnc_chk(val):
                try:
                    val = fnc_fix(val)
                except Exception:
                    val = default
            return val

        offset = getval('offset', lambda x: isinstance(x, float), lambda x: abs(float(x)), 0)
        run_at = getval('runAt', lambda x: isinstance(x, int), lambda x: max(0, int(x)), 0)
        rate = getval('rate', lambda x: isinstance(x, int), lambda x: int(x), 1)
        timestamp = getval(
		    'timestamp',
		    lambda x: isinstance(x, int),
		    lambda x: int(x),
		    self.unix_timestamp()
		)


        if data.get('state') not in [
                'ready',
                'unstarted',
                'ended',
                'playing',
                'paused',
                'buffering',
                'cued',
                'playback'

        ]:
            return

        self.flaskserver.socketio.emit(EVENT_YT_STATE_CHANGE, {
            'state': data['state'],
            'sender': user.id,
            'offset': offset,
            'rate': rate,
            'runAt': run_at,
            'timestamp': timestamp
        }, include_self=False)

    def unix_timestamp(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()
        return int((timestamp - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
