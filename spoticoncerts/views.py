from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_required, current_user
from .tracks import Track
from .spotify_auth import get_token
from .models import Song
from . import db


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
    #Store tracks dataframe as json file and added to session
    df = tracks.filter_tracks()
    tracks_json = df.to_json()
    session['tracks'] = tracks_json

    for index, row in df.iterrows():
        new_song = Song(
            song = row['song'],
            artist = row['artist'],
            album = row['album'],
            played_at = row['played_at'],
            user_id = current_user.get_id()
        )
        db.session.add(new_song)
        db.session.commit()

    return render_template('dashboard.html', table = tracks.display_tracks())    


@views.route('/top_artists')
@login_required
def top_artists():
    #Open sql script. Script limit sets to 5
    with open('db_queries/user_top_artists.sql', 'r') as sql_file:
        query = sql_file.read()
    db.session.query(query)
    
    return render_template('dashboard.html', table = tracks.display_tracks()) 