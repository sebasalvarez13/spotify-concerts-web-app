from flask import Flask

def creat_app():
    app = Flask(__name__)
    #Define secret key to encrypt/secure cookies and session data
    app.config['SECRET_KEY'] = "asdfghjkl"

    return app