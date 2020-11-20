import flask
import flask_socketio

from db_models.user import User


class LoginNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_login_temporary(self, data):
        print("Got an event for new temp user input with data:", data)

    def on_login_oauth_facebook(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)

        key = 'status'
        if key in data['response'].keys():
            self.flaskserver.socketio.emit('unverified_user', user.json())
        else:
            # TODO verify access token

            cur = self.flaskserver.db.cursor()
            result = User.get_from_db(cur, user, oauth={
                'id': data['response']['id'],
                'type': 'FACEBOOK'
            })

            user.username = data['response']['name']
            user.email = data['response']['email']
            user.profile_url = data['response']['picture']['data']['url']
            user.oauth_id = data['response']['id']
            user.oauth_type = 'FACEBOOK'

            if result is None:
                User.insert_to_db(cur, user, password=None)
                self.flaskserver.db.commit()

            cur.close()

            self.flaskserver.socketio.emit('verified_user', user.json())
