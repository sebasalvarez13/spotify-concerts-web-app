from datetime import datetime
import pandas
import requests
import re
import datetime
from datetime import timezone

class Track():
    def __init__(self, spotify_token):
        self.spotify_token = spotify_token

    def get_tracks(self):
        '''Connects to Spotify API and obtains the recently played songs. Returns the parsed data'''
        #max number of items that can be returned
        limit = 50

        query = "https://api.spotify.com/v1/me/player/recently-played?limit={}".format(limit)
        headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
        }

        response = requests.get(query, headers = headers)

        api_data = response.json()

        return(api_data)


    def filter_tracks(self):
        '''Filters API data to obtain song, artist, album and uri'''
        #Declare empty lists to store the track name, artist, album, played_at and uri
        songs_list = []
        artist_list = []
        album_list = []
        played_at_list = []
        song_uri_list = []

        #Iterate through API results and populate lists
        api_tracks = self.get_tracks()

        for track in api_tracks['items']:
            songs_list.append(track['track']['name'])
            artist_list.append(track['track']['album']['artists'][0]['name'])
            album_list.append(track['track']['album']['name'])
            played_at_list.append(self.format_played_at(track['played_at']))
            song_uri_list.append(track['track']['uri'])

        #Create a dictionary and add the lists (values) to their respective key
        track_dict = {
            'song': songs_list,
            'artist': artist_list,
            'album': album_list,
            'played_at': played_at_list,
            'song_uri': song_uri_list
        }

        #Create a dataframe using the track dictionary
        df = pandas.DataFrame(track_dict, columns = track_dict.keys())

        return(df)


    def format_played_at(self, spotify_time):
        '''Changes format for 'played_at' so it can be inserted into mysql database and converts time from UTC to local time.'''
        '''Returns df with correct datetime format'''

        #Spotify returns time as a string in UTC. Filter string from  ".xxxZ" element
        time_fltrd = re.search('[0-9]+\-[0-9]+\-[0-9]+T[0-9]+\:[0-9]+\:[0-9]+', spotify_time)

        #Convert time string to datetime object
        spotify_time_obj = datetime.datetime.strptime(time_fltrd.group(), '%Y-%m-%dT%H:%M:%S') 

        #Convert datetime object in UTC to local time
        local_time_obj = spotify_time_obj.replace(tzinfo=timezone.utc).astimezone(tz=None)

        #Convert time object to string in correct sql datetime format
        sql_time_str = local_time_obj.strftime('%Y-%m-%d %H:%M:%S')

        return sql_time_str


    def display_tracks(self):
        #Converts dataframe to html table
        recent_tracks_html = self.filter_tracks().to_html(classes = "table table-dark table-striped", justify = 'left')

        return(recent_tracks_html)







