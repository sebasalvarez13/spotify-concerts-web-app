'''Here is where we create our database models'''

from . import db
#UserMixin is a custom class that will give our user object specific things for our login
from flask_login import UserMixin

class User(db.model, UserMixin):
    #Define the columns for our table
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))

