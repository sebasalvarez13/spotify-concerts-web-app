from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

#Define new database
db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    #Define secret key to encrypt/secure cookies and session data
    app.config['SECRET_KEY'] = 'asdfghjkl'

    #Define database: 'my sqlalchemy database is stored at this location'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #Initialize database: tells database which app we are going to use with it
    db.init_app(app)
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Song

    #Create database
    create_database(app)

    return app

def create_database(app):
    #Check if db exists. If not create it
    if not path.exists('spoticoncerts' + DB_NAME):
        db.create_all(app = app)
        print('Databse created')

