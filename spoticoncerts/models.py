'''Here is where we create our database models'''

from . import db
#UserMixin is a custom class that will give our user object specific things for our login
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    #Define the columns for our table
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    songs = db.relationship('Song')

class Song(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    song = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    played_at = db.Column(db.DateTime(timezone = True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
