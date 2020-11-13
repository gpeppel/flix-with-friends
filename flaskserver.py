import os

from dotenv import load_dotenv
import flask
import flask_socketio
import flask_sqlalchemy

from db_models.message import Message

from db_models.user import User

from socketns.youtube import YoutubeNamespace
import sqldb

MESSAGES_EMIT_CHANNEL = 'messages_received'


class FlaskServer:
	def __init__(self, app, db):
		dotenv_path = os.path.join(os.path.dirname(__file__), 'sql.env')
		load_dotenv(dotenv_path)

		self.app = app
		self.app.add_url_rule('/', 'index', self.index)

		self.socketio = flask_socketio.SocketIO(self.app)
		self.socketio.init_app(self.app, cors_allowed_origins='*')

		self.db = db
		
		self.socketio.on_namespace(YoutubeNamespace('/', self))

		self.rooms = {}
		self.users = {}


	def run(self, host, port, debug=False):
		self.socketio.run(
			self.app,
			host=host,
			port=port,
			debug=debug
		)


	def index(self):
		return flask.render_template('index.html')

	def get_facebook_tuple(self, user_id):
		for user in db.session.query(db_models.User).all():
			if user.oauth_id == user_id:
				return (user.name, user.image_url)

	def emit_all_messages(self, channel):
		all_messages = [
			(db_message.id, db_message.text, str(db_message.timestamp), db_message.userId, self.get_facebook_tuple(db_message.userId)) # TODO decide if userId should even be sent to clients
			for db_message in self.db.session.query(Message).all()
		]
		self.socketio.emit(MESSAGES_EMIT_CHANNEL, all_messages)


	def createUserFromRequest(self, request):
		user = User(request.sid)
		self.users[user.id] = user

		return user


	def deleteUser(self, user):
		del self.users[user.id]


	def getUserByRequest(self, request):
		return self.users[request.sid]


	def createRoom(self, roomId=None):
		room = Room(roomId)
		self.rooms[room.id] = room

		return room


	def deleteRoom(self, room):
		for user in room.users.values():
			room.removeUser(user)

		del self.rooms[room.id]
