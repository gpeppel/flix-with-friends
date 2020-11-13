import os

import flask

import sqldb

db = sqldb.SQLAlchemy()

def createFlaskServer(db):
	from flaskserver import FlaskServer

	app = flask.Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.app = app
	db.init_app(app)

	return FlaskServer(app, db)


if __name__ == '__main__':
	db.create_all()
	db.session.commit()

	flaskserver = createFlaskServer(db)
	flaskserver.run(os.environ.get('IP', '0.0.0.0'), int(os.environ.get('PORT', 8080)), debug=True)
