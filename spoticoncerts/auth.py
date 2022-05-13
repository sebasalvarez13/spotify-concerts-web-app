from unicodedata import category
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
            return redirect(url_for('views.home'))
    
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
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password. Try again', category = 'error')
        else:
            flash('Username does not exist', category = 'error')

    return render_template('login.html')