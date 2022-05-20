from flask import Blueprint, render_template, session, request, redirect, url_for
from flask_login import login_required, current_user
from .tracks import Track
from .concerts import Concert
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

    return redirect(url_for('views.recentsongs'))


@views.route('/recentsongs')
@login_required
def recentsongs():
    if session['tracks']:
        recent_songs_df = pd.read_json(session['tracks'])
        recent_songs_html = recent_songs_df.to_html(classes = "table table-dark table-striped", justify = 'left')
    else:    
        tracks = Track(session['access_token'])
        recent_songs_df = tracks.filter_tracks()
        
        #Iterate through dataframe and upload rows to Song db model
        for index, row in recent_songs_df.iterrows():
            new_song = Song(
                song = row['song'],
                artist = row['artist'],
                album = row['album'],
                played_at = row['played_at'],
                user_id = current_user.get_id()
            )
            db.session.add(new_song)
            db.session.commit()

        #Store tracks dataframe as json file and added to session
        recent_songs_json = recent_songs_df.to_json()
        session['tracks'] = recent_songs_json
        
        #Converts dataframe to html table    
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

    #Save top artists list as a session key to use as parameter for Concert() object
    session['top_artists'] = artists_list

    #Create dataframe with artist name and reproductions
    top_artists_df = pd.DataFrame(top_artists_dict, columns = top_artists_dict.keys())
    
    #Converts dataframe to html table
    top_artists_html = top_artists_df.to_html(classes = "table table-dark table-striped", justify = 'left')

    return render_template('dashboard.html', table = top_artists_html) 


@views.route('/concerts')
@login_required
def concerts():
    concert = Concert(session['top_artists'])
    concerts_df = concert.filter_concert_data()

    #Converts dataframe to html. Drop Id column before displaying on html 
    concerts_df = concerts_df.drop(['id'], axis=1)
    concerts_html = concerts_df.to_html(classes = "table table-dark table-striped", justify = 'left')

    return render_template('dashboard.html', table = concerts_html)


