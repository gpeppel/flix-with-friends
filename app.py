# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 

ADDRESSES_RECEIVED_CHANNEL = 'addresses received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


db.create_all()
db.session.commit()

def emit_all_addresses(channel):
    # TODO
    print("TODO")

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })


@socketio.on('new_temp_user')
def on_new_temp_user(data):
    # db.session.add(tables.Users(data['name'], data['email'], data['username']))
    # db.session.commit()
    print("Got an event for new temp user input with data:", data)

@socketio.on('new_facebook_user')
def on_new_facebook_user(data):
    # db.session.add(tables.Users(data['name'], data['email'], data['email'],data['accessToken']))
    # db.session.commit()
    print("Got an event for new google user input with data:", data)
    
@socketio.on('new_user')
def newUserHandler(data):
    # db.session.add(tables.Users(data['username'], data['password']))
    # db.session.commit()
    socketio.emit('new_user_recieved')

# TODO - GET ACCESSS TOKEN FROM USER

@socketio.on('user_status')
def handleUserStatus(data):
    # TODO
    # for user in db.session.query(tables.Users).all():
    #     if user.username == data['username'] and user.password == data['password']:
    #         print('existing_user')
    #         socketio.emit('existing_user', {'status' : True , 'username': data['username']} )
    #         socketio.emit
    #         db.session.commit()
    #         break
    #     else:
    #         if user.username == data['username'] and user.password != data['password']:
    #             print('wrong_password')
    #             socketio.emit('wrong_password', { 'status' : False })
    #             break
    #         if user.username != data['username'] and user.password != data['password']:
    #             print('new_user')
    #             newUserHandler(data)
    #             socketio.emit('existing_user',  { 'status' : True })
    #             break
    db.session.commit()

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

@socketio.on('new address input')
def on_new_address(data):
    print("Got an event for new address input with data:", data)
    
    db.session.add(models.Usps(data["address"]));
    db.session.commit();
    
    emit_all_addresses(ADDRESSES_RECEIVED_CHANNEL)

@app.route('/')
def index():
    emit_all_addresses(ADDRESSES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
