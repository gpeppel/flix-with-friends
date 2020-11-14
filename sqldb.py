import os

from dotenv import load_dotenv
import flask_sqlalchemy


dotenv_path = os.path.join(os.path.dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)


def get_database_uri():
    uri = os.environ.get('DATABASE_URI')
    if uri is not None and len(uri) != 0:
        return uri

    try:
        sql_user = os.environ['SQL_USER']
        sql_pwd = os.environ['SQL_PASSWORD']
        sql_db = os.environ['SQL_DATABASE']
    except KeyError:
        return None

    return 'postgresql://%s:%s@localhost/%s' % (sql_user, sql_pwd, sql_db)


db_singleton = None

def SQLAlchemy():
    global db_singleton
    if db_singleton is None:
        db_singleton = flask_sqlalchemy.SQLAlchemy()

    return db_singleton
