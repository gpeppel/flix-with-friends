import datetime
import json
import os
import re
import random
import sys
import time

from dotenv import load_dotenv
import flask
import flask_socketio
import flask_sqlalchemy

import message
from socketns.youtube import YoutubeNamespace
import sqldb


EVENT_YT_STATE_CHANGE = 'yt-state-change'
MESSAGES_EMIT_CHANNEL = 'messages received'


class FlaskServer:
	def __init__(self, app, db=None):
		dotenv_path = os.path.join(os.path.dirname(__file__), 'sql.env')
		load_dotenv(dotenv_path)

		self.app = app
		self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
		self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

		self.app.add_url_rule('/', 'index', self.index)

		self.socketio = flask_socketio.SocketIO(self.app)
		self.socketio.init_app(self.app, cors_allowed_origins='*')

		self.db = db

		self.socketio.on_namespace(YoutubeNamespace('/', self))

		self.rooms = {}
		self.users = {}


	def run(self, debug=False):
		self.socketio.run(
			self.app,
			host=self.host,
			port=self.port,
			debug=debug
		)


	def index(self):
		self.db.create_all()
		self.db.session.commit()
		return flask.render_template('index.html')


	def emit_all_messages(self, channel):
		all_messages = [
			(db_message.id, db_message.text, str(db_message.timestamp), db_message.userId) # TODO decide if userId should even be sent to clients
			for db_message in self.db.session.query(message.Message).all()
		]
		socketio.emit(MESSAGES_EMIT_CHANNEL, all_messages)
