from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_required, current_user
from .tracks import Track
from .spotify_auth import get_token
from .models import Song
from . import db
import pandas as pd


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


@views.route('/recentsongs')
@login_required
def recentsongs():
    tracks = Track(session['access_token'])
    #Store tracks dataframe as json file and added to session
    recent_songs_df = tracks.filter_tracks()
    recent_songs_df = df.to_json()
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

    recent_songs_html = tracks.display_tracks()
    return render_template('dashboard.html', table = recent_songs_html)    


@views.route('/topartists')
@login_required
def top_artists():
    #Open sql script. Script limit sets to 5
    with open('spoticoncerts/db_queries/user_top_artists.sql', 'r') as sql_file:
        query = sql_file.read()
    result = db.session.execute(query, {'val':current_user.get_id()})
    
    artists_list = []
    reproductions_list = []

    for artist in result.fetchall():
        artists_list.append(artist[0])
        reproductions_list.append(artist[1])

    top_artists_dict = {'artist': artists_list, 'reproductions': reproductions_list}

    #Create dataframe with artist name and reproductions
    top_artists_df = pd.DataFrame(top_artists_dict, columns = top_artists_dict.keys())
    
    #Converts dataframe to html table
    top_artists_html = top_artists_df.to_html(classes = "table table-dark table-striped", justify = 'left')

    return render_template('dashboard.html', table = top_artists_html) 