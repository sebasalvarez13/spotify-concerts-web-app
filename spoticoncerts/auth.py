from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

#Set up blueprint for Flask application
auth = Blueprint('auth', __name__)

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        #Create a new user
        new_user = User(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
            password = generate_password_hash(password, method = 'sha256')
        )
        db.session.add(new_user)
        db.session.commit
        return redirect(url_for('views.home'))
    else:
        return render_template('register.html')


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')