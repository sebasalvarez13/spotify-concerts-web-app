from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .tracks import Track

#Set up blueprint for Flask application
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/dashboard')
@login_required
def dashboard():
    tracks = Track()
    return render_template('dashboard.html', table = tracks.display_tracks() )    