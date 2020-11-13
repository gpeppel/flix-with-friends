import os

from dotenv import load_dotenv
import flask_sqlalchemy


dotenv_path = os.path.join(os.path.dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

def getDatabaseUri():
	uri = os.environ.get('DATABASE_URI')
	if uri is not None and len(uri) != 0:
		return uri

	sql_user = os.environ['SQL_USER']
	sql_pwd = os.environ['SQL_PASSWORD']
	sql_db = os.environ['SQL_DATABASE']
	return 'postgresql://%s:%s@localhost/%s' % (sql_user, sql_pwd, sql_db)


def SQLAlchemy():
	return flask_sqlalchemy.SQLAlchemy()
