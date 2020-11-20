class User:
    def __init__(self,
        user_id,
        username=None,
        email=None,
        profile_url=None,
        settings=None,
        oauth_id=None,
        oauth_type=None,
        sid=None
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.profile_url = profile_url
        self.settings = settings
        self.oauth_id = oauth_id
        self.oauth_type = oauth_type
        self.sid = sid

        self.room = None

    @staticmethod
    def from_request(req):
        user = User(None, sid=req.sid)
        return user
