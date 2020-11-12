import flask_sqlalchemy
from app import db

class User:
	def __init__(self, userId):
		self.id = userId

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    settings = db.Column(db.String(120))
    
    def __init__(self, i, n, e, s):
        self.address = i
        self.address = n
        self.address = e
        self.address = s