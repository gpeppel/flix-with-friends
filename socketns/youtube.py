import flask
import flask_socketio

import flaskserver
from db_models.room import Room
from db_models.user import User


class YoutubeNamespace(flask_socketio.Namespace):
	def __init__(self, ns, server):
		super().__init__(ns)
		self.ns = ns
		self.flaskserver = server


	def on_connect(self):
		self.connectUser(flask.request)
		self.flaskserver.emit_all_messages(flaskserver.MESSAGES_EMIT_CHANNEL)


	def connectUser(self, request):
		global appRooms

		# TODO room assignment
		"""
		if len(appRooms) == 0:
			room = Room()
			appRooms[room.id] = room
			roomIDs.append(room.id)
			socketio.emit('new room id', roomIDs[0])
		else:
			room = appRooms[list(appRooms.keys())[0]]
			print("big list " + str(roomIDs))
		"""


		user = User(request.sid)
		#room.addUser(user)
		#print("Hello " + room.id)
		#print(roomIDs[0])


	def on_disconnect(self):
		self.disconnectUser(flask.request)


	def disconnectUser(self, request):
		"""
		global appRooms
		room = appRooms[list(appRooms.keys())[0]]
		room.removeUser(User(request.sid))

		if len(room) == 0:
			del appRooms[room.id]
		"""


	def on_new_temp_user(self, data):
		# db.session.add(tables.Users(data['name'], data['email'], data['username']))
		# db.session.commit()
		print("Got an event for new temp user input with data:", data)


	def on_new_facebook_user(self, data):
		# db.session.add(tables.Users(data['name'], data['email'], data['email'],data['accessToken']))
		# db.session.commit()
		print("Got an event for new google user input with data:", data)


	def newUserHandler(self, data):
		# db.session.add(tables.Users(data['username'], data['password']))
		# db.session.commit()
		socketio.emit('new_user_recieved')

	# TODO - GET ACCESSS TOKEN FROM USER


	def handleUserStatus(self, data):
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



	def add_to_db(self, message_to_add):
		message.db.session.add(message_to_add)
		message.db.session.commit()
		emit_all_messages(MESSAGES_EMIT_CHANNEL)


	def new_message_received(self, data):
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


	def on_yt_load(self, data):
		url = data.get('url')
		if url is None:
			return

		videoId = self.getYoutubeVideoId(url)
		if videoId is None:
			return

		socketio.emit('yt-load', {
			'videoId': videoId
		})


	def getYoutubeVideoId(self, s):
		match = re.match(r'^(?:https?://)?(?:www\.)?youtu(?:\.be/|be\.com/(?:embed/|watch\?v=))([A-Za-z0-9_-]+)', s)
		if match is not None:
			return match[1]

		match = re.match(r'^([A-Za-z0-9_-]+)$', s)
		if match is not None:
			return match[1]

		return None


	def on_yt_state_change(self, data):
		self.handleYtStateChange(flask.request, data)


	def handleYtStateChange(self, request, data):
		user = User(request.sid)

		print(json.dumps(data).encode("ascii", errors="backslashreplace").decode("ascii"))

		# TODO room assignment

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


	def unixTimestamp(self, ts=None):
		if ts is None:
			ts = datetime.datetime.utcnow()
		return int((ts - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
