from flask import Blueprint, render_template

#Set up blueprint for Flask application
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')