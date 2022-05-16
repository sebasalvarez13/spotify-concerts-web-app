from flask import Blueprint, render_template, request, flash, url_for, redirect
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .spotify_auth import get_authorization

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

        #Query database to check user does not exist previously
        user = User.query.filter_by(username = username).first() #returns first result
        if user:
            flash('Username already exists', category = 'error')
        else:
            #Create a new user
            new_user = User(
                first_name = first_name,
                last_name = last_name,
                email = email,
                username = username,
                password = generate_password_hash(password, method = 'sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            #Remember user who logged in
            login_user(user, remember = True)
            return redirect(url_for('views.dashboard'))
    
    return render_template('register.html')


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #Query database to confirm username and password exist
        user = User.query.filter_by(username = username).first() #returns first result
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfuly', category = 'success')
                #Remember user who logged in
                login_user(user, remember = True)

                #Get authorization code from Spotify server
                response = get_authorization()
                url = response.url
                return redirect(url)

            else:
                flash('Incorrect password. Try again', category = 'error')
        else:
            flash('Username does not exist', category = 'error')

    return render_template('login.html')


@auth.route('/logout', methods = ['GET', 'POST'])
#Decorator makes sure we can't access this route unles user is logged in
@login_required 
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


