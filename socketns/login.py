import os

from dotenv import load_dotenv
import flask
import flask_socketio
import google.oauth2.id_token
import google.auth.transport.requests

from db_models.user import User


dotenv_path = os.path.join(os.path.dirname(__file__), "../react.env")
load_dotenv(dotenv_path)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class LoginNamespace(flask_socketio.Namespace):
    def __init__(self, namespace, server):
        super().__init__(namespace)
        self.namespace = namespace
        self.flaskserver = server

    def on_login_temporary(self, data):
        print("Got an event for new temp user input with data:", data)

    def on_login_oauth_facebook(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)

        key = "status"
        if key in data["response"].keys():
            self.flaskserver.socketio.emit(
                "login_response", {"status": "fail", "userId": None}, room=user.sid
            )
        else:
            # TODO verify access token

            cur = self.flaskserver.db.cursor()
            User.get_from_db(
                cur, user, oauth={"id": data["response"]["id"], "type": "FACEBOOK"}
            )

            user.username = data["response"]["name"]
            user.email = data["response"]["email"]
            user.profile_url = data["response"]["picture"]["data"]["url"]
            user.oauth_id = data["response"]["id"]
            user.oauth_type = "FACEBOOK"

            User.insert_to_db(cur, user, password=None)
            self.flaskserver.db.commit()
            cur.close()

            self.flaskserver.socketio.emit(
                "login_response",
                {"status": "ok", "userId": user.user_id},
                room=user.sid,
            )

    def on_logout_oauth_facebook(self, data):
        user = self.flaskserver.get_user_by_request(flask.request)

        cur = self.flaskserver.db.cursor()
        User.get_from_db(cur, user, oauth={"id": user.sid, "type": "FACEBOOK"})

        print("\nNew Logout:")
        print("sid: " + user.sid)
        print("oauth_id: " + user.oauth_id)
        print("name: " + user.username)

        removed_user = User.remove_from_db(cur, user, password=None)
        self.flaskserver.db.commit()
        cur.close()

        print('\nRemoved user:')
        print(removed_user.username)

    def on_login_oauth_google(self, data):
        print(data)

        user = self.flaskserver.get_user_by_request(flask.request)

        token = data.get("tokenId")
        failed = False
        req = None

        # https://developers.google.com/identity/sign-in/web/backend-auth
        try:
            req = google.auth.transport.requests.Request()
            idinfo = google.oauth2.id_token.verify_oauth2_token(
                token, req, GOOGLE_CLIENT_ID
            )
        except Exception as exc:
            print(exc)
            failed = True
        finally:
            if req is not None:
                req.session.close()

        if failed:
            self.flaskserver.socketio.emit(
                "login_response", {"status": "fail", "userId": None}, room=user.sid
            )
            return

        cur = self.flaskserver.db.cursor()
        result = User.get_from_db(
            cur, user, oauth={"id": data["googleId"], "type": "GOOGLE"}
        )

        user.username = data["name"]
        user.email = data["email"]
        user.profile_url = data["profileUrl"]
        user.oauth_id = data["googleId"]
        user.oauth_type = "GOOGLE"

        User.insert_to_db(cur, user, password=None)
        self.flaskserver.db.commit()
        cur.close()

        self.flaskserver.socketio.emit(
            "login_response", {"status": "ok", "userId": user.user_id}, room=user.sid
        )
