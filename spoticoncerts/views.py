from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_required, current_user
from .tracks import Track
from .spotify_auth import get_token

#Set up blueprint for Flask application
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')


@views.route('callback', methods = ['GET', 'POST'])
@login_required
def callback():
    if request.method == 'GET':
        #Obtain the authorization code from the URL
        code = request.args.get("code")
        #Pass code to Spotify server to obtain access_token
        token_response = get_token(code)
        #Store accesss token in Session key
        session['access_token'] = token_response['access_token']

    return redirect(url_for('views.dashboard'))


@views.route('/dashboard')
@login_required
def dashboard():
    tracks = Track(session['access_token'])
    return render_template('dashboard.html', table = tracks.display_tracks())    