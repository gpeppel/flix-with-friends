import datetime

import flask
import flask_socketio

from db_models.message import Message


class ChatNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def add_to_db(self, msg):
        if msg.user_id < 0:
            return

        cur = self.flaskserver.db.cursor()
        msg.insert_to_db(cur)
        self.flaskserver.db.commit()
        cur.close()

    def on_message_send(self, data):
        user = self.flaskserver.get_user_by_request(flask.request, flask.session)
        if user.room is None:
            return

        text = data['text']
        user_id = user.user_id
        timestamp = datetime.datetime.now()
        room_id = user.room.room_id

        msg = Message(None, text, timestamp, room_id, user_id, {
            'username': user.username,
            'profile_url': user.profile_url
        })
        self.flaskserver.add_message(msg)
        if self.flaskserver.db_connected():
            self.add_to_db(msg)
        self.flaskserver.emit_all_messages(user.room)
