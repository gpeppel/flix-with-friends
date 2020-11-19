import os
import sys

import flask

import sqldb


db = sqldb.SQLAlchemy()


def create_flask_server(db_obj, db_uri=None):
    from flaskserver import FlaskServer

    app = flask.Flask(__name__)
    if db_uri is None:
        db_uri = sqldb.get_database_uri()

    if db_uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        db_obj.init_app(app)
    else:
        db_obj = None

    return FlaskServer(app, db_obj)


if __name__ == '__main__':
    flaskserver = create_flask_server(db)

    if flaskserver.db_enabled():
        flaskserver.db.create_all()
        flaskserver.db.session.commit()
    else:
        print('WARNING: database not connected!', file=sys.stderr)

    flaskserver.run(
        os.environ.get('IP', '0.0.0.0'),
        int(os.environ.get('PORT', 8080)),
        debug=True
    )
