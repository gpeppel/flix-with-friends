import flask
import flask_socketio


class LoginNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_new_temp_user(self, data):
        # db.session.add(tables.Users(data['name'], data['email'], data['username']))
        # db.session.commit()
        print("Got an event for new temp user input with data:", data)

    def on_new_facebook_user(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)

        key = 'status'
        if key in data['response'].keys():
            self.flaskserver.socketio.emit('unverified_user')
        else:
            self.flaskserver.socketio.emit('verified_user')

            """
            if self.flaskserver.db_connected():
                self.flaskserver.db.session.add(user)
                self.flaskserver.db.session.commit()
            """

            user.user_id = 0
            user.username = data['response']['name']
            user.profile_url = data['response']['picture']['data']['url']
            user.oauth_id = data['response']['id']
            user.oauth_type = 'FACEBOOK'

    # def handle_user_status(self, data):
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
        # self.flaskserver.db.session.commit()
