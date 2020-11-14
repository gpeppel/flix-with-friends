import os

import flask

import sqldb

db = sqldb.SQLAlchemy()


def create_flask_server(dbobj):
    from flaskserver import FlaskServer

    app = flask.Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = sqldb.get_database_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    dbobj.app = app
    dbobj.init_app(app)

    return FlaskServer(app, dbobj)


if __name__ == '__main__':
    flaskserver = create_flask_server(db)

    db.create_all()
    db.session.commit()

    flaskserver.run(
        os.environ.get('IP', '0.0.0.0'),
        int(os.environ.get('PORT', 8080)),
        debug=True
    )
