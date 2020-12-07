from db_models.base import Base


COOKIE_SESSION_ID = 'session_id'
COOKIE_SESSION_TOKEN = 'session_token'


class User(Base):
    def __init__(self,
        user_id,
        username=None,
        email=None,
        profile_url=None,
        settings=None,
        oauth_id=None,
        oauth_type=None,
        sid=None,
        session_id=None,
        session_token=None
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.profile_url = profile_url
        self.settings = settings
        self.oauth_id = oauth_id
        self.oauth_type = oauth_type

        self.sid = sid
        self.session_id = session_id
        self.session_token = session_token

        self.password = None

        self.socket_connected = False
        self.last_socket_connect = None

        self.room = None

    def get_session_id(self):
        if self.session_id is not None:
            return self.session_id
        return self.sid

    def authenticate(self, token):
        if self.session_token is None:
            return True
        return token == self.session_token

    def insert_to_db(self, cur):
        cur.execute("""
            INSERT INTO account VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (oauth_id, oauth_type) DO UPDATE SET username = %s, email = %s, profile_url = %s
            RETURNING user_id;
        """, (
            self.username,
            self.password,
            self.email,
            self.profile_url,
            self.settings,
            self.oauth_id,
            self.oauth_type,

            self.username,
            self.email,
            self.profile_url
        ))

        result = cur.fetchone()
        self.user_id = result['user_id']

    def is_authenticated(self):
        return self.user_id is not None

    def serialize(self):
        obj = {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'profile_url': self.profile_url,
            'settings': self.settings,
            'oauth_id': self.oauth_id,
            'oauth_type': self.oauth_type,

            'sid': self.sid,
            'session_id': self.session_id,

            'socket_connected': self.socket_connected
        }

        if self.last_socket_connect is not None:
            obj['last_socket_connect'] = self.last_socket_connect.strftime('%Y-%m-%d %H:%M:%S')
        else:
            obj['last_socket_connect'] = None

        return obj

    @staticmethod
    def from_request(req):
        user = User(
            None,
            sid=req.sid,
            session_id=req.cookies.get(COOKIE_SESSION_ID),
            session_token=req.cookies.get(COOKIE_SESSION_TOKEN),
        )
        return user

    @staticmethod
    def get_from_db(cur, user, username=None, email=None, oauth=None):
        query = 'SELECT * FROM account WHERE '
        values = None

        if username is not None:
            query += 'account.username = %s'
            values = (username)
        elif email is not None:
            query += 'account.email = %s'
            values = (email)
        elif oauth is not None:
            query += 'account.oauth_id = %s AND account.oauth_type = %s'
            values = (oauth['id'], oauth['type'])

        if values is None:
            return None

        query += ';'
        cur.execute(query, values)

        result = cur.fetchone()
        if result is None:
            return None

        user.user_id = result['user_id']
        user.username = result['username']
        user.password = result['password']
        user.email = result['email']
        user.profile_url = result['profile_url']
        user.settings = result['settings']
        user.oauth_id = result['oauth_id']
        user.oauth_type = result['oauth_type']

        return user

    @staticmethod
    def create_table(cur):
        cur.execute("""
            CREATE TABLE IF NOT EXISTS account (
                user_id BIGSERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT,
                email TEXT,
                profile_url TEXT,
                settings TEXT,
                oauth_id TEXT,
                oauth_type TEXT,
                UNIQUE(email),
                UNIQUE(oauth_id, oauth_type)
            );
        """)
