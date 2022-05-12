from flask import Blueprint, render_template, request, flash

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
    else:
        return render_template('register.html')


@auth.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('login.html')