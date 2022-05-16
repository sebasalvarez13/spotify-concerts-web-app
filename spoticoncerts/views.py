from flask import Blueprint, render_template
from flask_login import login_required, current_user

#Set up blueprint for Flask application
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html')