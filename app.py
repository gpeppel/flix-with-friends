from os.path import join, dirname
from dotenv import load_dotenv
import os
import sys
import flask
import flask_socketio
import flask_sqlalchemy
from datetime import datetime
import time
import random

from user import User

app = flask.Flask(__name__)


socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')

dotenv_path = join(dirname(__file__), "sql.env")
load_dotenv(dotenv_path)

database_uri = os.environ["DATABASE_URI"]
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.app = app

import message

@socketio.on('connect')
def on_connect():
	print('Someone connected!')
	socketio.emit('connected', {

	})

@socketio.on('disconnect')
def on_disconnect():
	print ('Someone disconnected!')

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
	message.db.session.add(message_to_add)
	message.db.session.commit()
	
	# message init model:
	# self.id = messageId
	# self.text = messageText
	# self.timestamp = messageTimestamp
	# self.roomId = messageRoomId
	# self.userId = messageUserId

@socketio.on('yt-load')
def on_yt_load(data):
	pass


@socketio.on('yt-state-change')
def on_yt_load(data):
	pass


@app.route('/')
def index():
	message.db.create_all()
	message.db.session.commit()
	return flask.render_template("index.html")


if __name__ == '__main__':
	socketio.run(
		app,
		host=os.getenv('IP', '0.0.0.0'),
		port=int(os.getenv('PORT', 8080)),
		debug=True
	)
