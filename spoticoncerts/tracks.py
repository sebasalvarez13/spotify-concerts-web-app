import pandas
import requests


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
        api_data = self.get_tracks()

        for track in api_data['items']:
            songs_list.append(track['track']['name'])
            artist_list.append(track['track']['album']['artists'][0]['name'])
            album_list.append(track['track']['album']['name'])
            played_at_list.append(track['played_at'])
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

    def display_tracks(self):
        #Converts dataframe to html table
        recent_tracks_html = self.filter_tracks().to_html(classes = "table table-dark table-striped", justify = 'left')

        return(recent_tracks_html)







