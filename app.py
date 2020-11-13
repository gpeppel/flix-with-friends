import os

import flask

import sqldb

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = sqldb.SQLAlchemy(app)


if __name__ == '__main__':
	from flaskserver import FlaskServer
	flaskserver = FlaskServer(app, db)
	flaskserver.run(os.environ.get('IP', '0.0.0.0'), int(os.environ.get('PORT', 8080)), debug=True)
