import datetime
import random
import sys

import flask
import flask_socketio

from db_models.message import Message


class ChatNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server
        
    def on_chat_loaded(self):
        print('\n\n\nCHAT_LOADED\n\n\n')
        self.flaskserver.emit_all_messages()

    def add_to_db(self, message_to_add):
        if not self.flaskserver.db_enabled():
            return

        self.flaskserver.db.session.add(message_to_add)
        self.flaskserver.db.session.commit()
        self.flaskserver.emit_all_messages()

    def on_message_send(self, data):
        user_request = flask.request
        user_from_request = \
        self.flaskserver.get_user_by_request(user_request)

        if self.flaskserver.db_enabled():
            self.flaskserver.db.session.add(user_from_request)

        user_oauth_id = user_from_request.oauth_id
        text = data['text']
        message_id = \
        random.randint(1 - sys.maxsize, sys.maxsize) # TODO use an agreed upon id scheme
        user_id = user_oauth_id
        timestamp = \
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        room_id = 'room_id_here' # TODO use actual room id
        message_to_add = \
        Message(message_id, text, timestamp, room_id, user_id)
        return self.add_to_db(message_to_add)
