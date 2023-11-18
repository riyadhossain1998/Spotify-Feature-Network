
#   For Spotify
from spotipy_connection import authenticate, connectSpotify
from artist_controller import getArtistInfo
from playlist_controller import graphDataGenerator

#   For Flask
from flask import Flask,render_template,url_for, jsonify, request

#   Python libs
from os import environ
import json


app = Flask(__name__)


@app.route('/playlist')
def playlist():
    return 'spotify:playlist:2aBcEWYEVC6Ixrq6LplhBa'


def musicControls(input, spotifyObject):
    if(input == 'play'):
        spotifyObject.start_playback()
    if(input == 'pause'):
        spotifyObject.pause_playback()
    #if(input == 'queue'):
     #   add_track_to_queue()

def add_track_to_queue(access_token, track_uri):
    endpoint = 'https://api.spotify.com/v1/me/player/queue'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'uri': track_uri}

    response = requests.post(endpoint, headers=headers, params=params)

    if response.status_code == 204:
        print(f'Track {track_uri} added to the queue successfully.')
    else:
        print(f'Failed to add track to the queue. Status code: {response.status_code}, Response: {response.json()}')




@app.route('/changeSong', methods=['GET'])
def changeSong():
    songUri = request.args.get('trackId')
    
    # Get the 'spotifyObject' from the Flask global context
    spotifyObject = getattr(app, 'spotifyObject', None)

    spotifyObject.start_playback(uris=['spotify:track:'+ songUri])
    
    # Return a response (you can customize this based on your needs)
    return jsonify({'status': 'success', 'trackId': songUri})

def generateJSONFilesFromPlaylists():
    #   Connect to spotify
    spotifyObject = connectSpotify()
    
    static_path = app.static_folder

    #   Read JSON file
    file = open(static_path + '/data/playlist-information.json')
    
    artistData = json.load(file)
    
    
    #for artist in artistData['artists']:
    #    graphDataGenerator(spotifyObject, artist['pl_id'], artist['name'])
    
    for i in range(20, len(artistData['artists'])):
        artist = artistData['artists'][i]
        graphDataGenerator(spotifyObject, artist['pl_id'], artist['name'])
    



@app.route('/')
def index():
    spotifyObject = connectSpotify()

    #pl_id = 'spotify:playlist:1A7gd8Yrfpuw5C6VHQmOA3'
    #static_path = app.static_folder
    #graphDataGenerator(spotifyObject, pl_id, 'gunna')    #return b
    return render_template('index.html')





if __name__ == "__main__":
    #CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    #CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    # Get a Spotify authenticated instance
    #sp_instance = authenticate(CLIENT_ID, CLIENT_SECRET)
    #generateJSONFilesFromPlaylists()
    app.spotifyObject = connectSpotify()

    app.run(debug=True)
