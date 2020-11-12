import datetime
import json
import os
import re

import flask
import flask_socketio

from room import Room
from user import User


EVENT_YT_STATE_CHANGE = 'yt-state-change'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

appRooms = {}


@socketio.on('connect')
def on_connect():
	connectUser(flask.request)


def connectUser(request):
	global appRooms

	# TODO placeholder room assignment
	if len(appRooms) == 0:
		room = Room()
		appRooms[room.id] = room
	else:
		room = appRooms[list(appRooms.keys())[0]]

	user = User(request.sid)
	room.addUser(user)


@socketio.on('disconnect')
def on_disconnect():
	disconnectUser(flask.request)


def disconnectUser(request):
	global appRooms

	# TODO placeholder room assignment
	room = appRooms[list(appRooms.keys())[0]]
	room.removeUser(User(request.sid))

	if len(room) == 0:
		del appRooms[room.id]


@socketio.on('yt-load')
def on_yt_load(data):
	url = data.get('url')
	if url is None:
		return

	videoId = getYoutubeVideoId(url)
	if videoId is None:
		return

	socketio.emit('yt-load', {
		'videoId': videoId
	})


def getYoutubeVideoId(s):
	match = re.match(r'^(?:https?://)?(?:www\.)?youtu(?:\.be/|be\.com/(?:embed/|watch\?v=))([A-Za-z0-9_-]+)', s)
	if match is not None:
		return match[1]

	match = re.match(r'^([A-Za-z0-9_-]+)$', s)
	if match is not None:
		return match[1]

	return None

@socketio.on(EVENT_YT_STATE_CHANGE)
def on_yt_state_change(data):
	handleYtStateChange(flask.request, data)


@app.route('/')
def index():
	return flask.render_template("index.html")


def handleYtStateChange(request, data):
	user = User(request.sid)

	# TODO placeholder room assignment
	room = appRooms[list(appRooms.keys())[0]]
	#if not room.isCreator(user):
	#	return

	print(json.dumps(data).encode("ascii", errors="backslashreplace").decode("ascii"))

	offset = data.get('offset', 0)
	if type(offset) != float:
		try:
			offset = abs(float(offset))
		except:
			offset = 0

	runAt = data.get('runAt', 0)
	if type(runAt) != int:
		try:
			runAt = max(0, int(runAt))
		except:
			runAt = 0

	rate = data.get('rate', 1)
	if type(rate) != int:
		try:
			rate = int(rate)
		except:
			rate = 1

	tsnow = unixTimestamp()
	timestamp = data.get('timestamp', 0)
	if type(timestamp) != int:
		try:
			timestamp = int(timestamp)
		except:
			timestamp = tsnow

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

	socketio.emit(EVENT_YT_STATE_CHANGE, {
		'state': data['state'],
		'sender': user.id,
		'offset': offset,
		'rate': rate,
		'runAt': runAt,
		'timestamp': timestamp
	}, include_self=False)


def unixTimestamp(ts=None):
	if ts is None:
		ts = datetime.datetime.utcnow()
	return int((ts - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


if __name__ == '__main__':
	socketio.run(
		app,
		host=os.getenv('IP', '0.0.0.0'),
		port=int(os.getenv('PORT', 8080)),
		debug=True
	)
