import datetime

import flask
import flask_socketio

from db_models.message import Message


class ChatNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_chat_loaded(self):
        user = self.flaskserver.get_user_by_request(flask.request)
        self.flaskserver.emit_all_messages(user.room)

    def add_to_db(self, msg):
        if not self.flaskserver.db_connected():
            return

        cur = self.flaskserver.db.cursor()
        msg.insert_to_db(cur)
        self.flaskserver.db.commit()
        cur.close()

        print(msg.serialize())

        self.flaskserver.emit_all_messages(self.flaskserver.rooms[msg.room_id])

    def on_message_send(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)

        print(user.serialize())

        text = data['text']
        user_id = user.user_id
        timestamp = datetime.datetime.now()
        room_id = user.room.room_id

        msg = Message(None, text, timestamp, room_id, user_id)
        return self.add_to_db(msg)
