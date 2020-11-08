from dotenv import load_dotenv
import os

import flask
import flask_socketio


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
	print('Someone disconnected!')


@socketio.on('yt-load')
def on_yt_load(data):
	pass


@socketio.on('yt-state-change')
def on_yt_load(data):
	handleYtStateChange(flask.request, data)


@app.route('/')
def index():
	return flask.render_template("index.html")


def handleYtStateChange(request, data):
	if data['state'] == 'play':
		socketio.emit('yt-state-change', data, room=request.sid)
	elif data['state'] == 'pause':
		socketio.emit('yt-state-change', data, room=request.sid)
	elif data['state'] == 'seek':
		socketio.emit('yt-state-change', data, room=request.sid)
	else:
		raise Exception()


if __name__ == '__main__':
	socketio.run(
		app,
		host=os.getenv('IP', '0.0.0.0'),
		port=int(os.getenv('PORT', 8080)),
		debug=True
	)
