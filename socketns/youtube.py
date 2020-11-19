import datetime
import json
import re

import flask
import flask_socketio


EVENT_YT_STATE_CHANGE = 'yt_state_change'
MESSAGES_EMIT_CHANNEL = 'messages_received'


class YoutubeNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_yt_load(self, data):
        self.handle_yt_load(flask.request, data)

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

    def handle_yt_load(self, request, data):
        url = data.get('url')
        if url is None:
            return

        video_id = self.get_youtube_video_id(url)
        if video_id is None:
            return

        self.flaskserver.socketio.emit('yt_load', {
            'videoId': video_id
        })

    def on_yt_state_change(self, data):
        self.handle_yt_state_change(flask.request, data)

    def handle_yt_state_change(self, request, data):
        user = self.flaskserver.get_user_by_request(request)

        print(
            json.dumps(data).encode(
                "ascii", errors="backslashreplace"
            ).decode("ascii")
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
        rate = getval('rate', lambda x: isinstance(x, float), lambda x: abs(float(x)), 1)
        run_at = getval('runAt', lambda x: isinstance(x, int), lambda x: max(0, int(x)), 0)
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

    def on_yt_sphereupdate(self, data):
        self.handle_yt_sphereupdate(flask.request, data)

    def handle_yt_sphereupdate(self, request, data):
        user = self.flaskserver.get_user_by_request(request)

        print('sphereupdate')

        self.flaskserver.socketio.emit('yt_sphereupdate', {
            'properties': data['properties']
        }, include_self=False)

    def unix_timestamp(self, timestamp=None):
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()
        return int((timestamp - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
