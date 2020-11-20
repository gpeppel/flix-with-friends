import os
import sys

import flask
from dotenv import load_dotenv

from flaskserver import FlaskServer
from sqldb import SqlDb


dotenv_path = os.path.join(os.path.dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

db = SqlDb()
db.connect(SqlDb.uri_to_dsn(os.environ['DATABASE_URL']))

def create_flask_server(db_obj):
    return FlaskServer(
        flask.Flask(__name__),
        db_obj
    )


if __name__ == '__main__':
    flaskserver = create_flask_server(db)

    if flaskserver.db_connected():
        #flaskserver.db.create_all()
        #flaskserver.db.session.commit()
        pass
    else:
        print('WARNING: database not connected!', file=sys.stderr)

    flaskserver.run(
        os.environ.get('IP', '0.0.0.0'),
        int(os.environ.get('PORT', 8080)),
        debug=True
    )
