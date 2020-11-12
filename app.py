from os.path import join, dirname
from dotenv import load_dotenv
import sys
import datetime
import json
import os
import re

import flask
import flask_socketio
import flask_sqlalchemy
from datetime import datetime
import time
import random

from room import Room
from user import User

EVENT_YT_STATE_CHANGE = 'yt-state-change'

app = flask.Flask(__name__)

MESSAGES_EMIT_CHANNEL = 'messages received'

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URI"]
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

import message
def emit_all_messages(channel):
	all_messages = [
		(db_message.id, db_message.text, str(db_message.timestamp), db_message.userId) # TODO decide if userId should even be sent to clients 
		for db_message in db.session.query(message.Message).all()
	]
	socketio.emit(MESSAGES_EMIT_CHANNEL, all_messages)
  
appRooms = {}

@socketio.on('connect')
def on_connect():
	connectUser(flask.request)
  emit_all_messages(MESSAGES_EMIT_CHANNEL)



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

@socketio.on('new_temp_user')
def on_new_temp_user(data):
    # db.session.add(tables.Users(data['name'], data['email'], data['username']))
    # db.session.commit()
    print("Got an event for new temp user input with data:", data)

@socketio.on('new_facebook_user')
def on_new_facebook_user(data):
    # db.session.add(tables.Users(data['name'], data['email'], data['email'],data['accessToken']))
    # db.session.commit()
    print("Got an event for new google user input with data:", data)
    
@socketio.on('new_user')
def newUserHandler(data):
    # db.session.add(tables.Users(data['username'], data['password']))
    # db.session.commit()
    socketio.emit('new_user_recieved')

# TODO - GET ACCESSS TOKEN FROM USER

@socketio.on('user_status')
def handleUserStatus(data):
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
    db.session.commit()


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

def add_to_db(message_to_add):
	message.db.session.add(message_to_add)
	message.db.session.commit()
	emit_all_messages(MESSAGES_EMIT_CHANNEL)


@socketio.on('message-send')
def new_message_received(data):
	text = data['text']
	print('\nReceived New Message: %s' % text)
	message_id = random.randint(1 - sys.maxsize, sys.maxsize) # TODO use an agreed upon id scheme
	user_id = random.randint(1 - sys.maxsize, sys.maxsize) # TODO use actual user id
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
	room_id = 'room_id_here' # TODO use actual room id


	print('\nAdding message to database:')
	print('messageId:%s' % message_id)
	print('text: %s' % text)
	print('timestamp: %s' % timestamp)
	print('roomId: %s' % room_id)
	print('userId: %s\n' % user_id)


	message_to_add = message.Message(message_id, text, timestamp, room_id, user_id)
	return add_to_db(message_to_add)
	
	# message init model:
	# self.id = messageId
	# self.text = messageText
	# self.timestamp = messageTimestamp
	# self.roomId = messageRoomId
	# self.userId = messageUserId

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
	message.db.create_all()
	message.db.session.commit()
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
