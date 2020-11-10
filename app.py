from dotenv import load_dotenv
import os
import flask
import flask_socketio
import flask_sqlalchemy

from message import Message

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins='*')


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
    print('RECEIVED NEW MESSAGE: %s' % text)
    if len(text) > 0:
        user = flask.request.sid

        # self.id = messageId
		# self.text = messageText
		# self.timestamp = messageTimestamp
		# self.roomId = messageRoomId
		# self.userId = messageUserId

        message_data = ()
        message = Message(



@socketio.on('yt-load')
def on_yt_load(data):
	pass


@socketio.on('yt-state-change')
def on_yt_load(data):
	pass


@app.route('/')
def index():
	return flask.render_template("index.html")


if __name__ == '__main__':
	socketio.run(
		app,
		host=os.getenv('IP', '0.0.0.0'),
		port=int(os.getenv('PORT', 8080)),
		debug=True
	)
