from asyncore import loop
import os
from os import environ
import spotipy
import re
import webbrowser
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from typing import List, Dict
from json.decoder import JSONDecodeError


#   ------------------------------    Read before running     ------------------------------
#   Be sure to set up the following environments in command line
#   export SPOTIPY_CLIENT_ID=''
#   export SPOTIPY_CLIENT_SECRET=''
#   export SPOTIPY_REDIRECT_URI=''
#   export SPOTIPY_USER_ID=''
#   Run program with userID as Command Line Argument


# Authenticate to Spotify (functions: authenticate, connectSpotify)
def authenticate(cliend_id: str, client_secret: str) -> spotipy.client.Spotify:
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=cliend_id,
            client_secret=client_secret
        )
    )

    return sp

def connectSpotify():
    # Get username from terminal
    #username = sys.argv[1]
    username = os.environ.get('SPOTIPY_USER_ID')

    scope = 'user-modify-playback-state'
    # Erase cache and prompt for user permission
    try:
        token = util.prompt_for_user_token(username, scope=scope)
    except(AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(username, scope=scope)

    # Create Spotify object
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    return spotifyObject

