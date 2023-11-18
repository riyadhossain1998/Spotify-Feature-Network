import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from json.decoder import JSONDecodeError

def authenticate(client_id: str, client_secret: str) -> spotipy.client.Spotify:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='your_redirect_uri',
            scope='user-modify-playback-state',
        )
    )
    return sp

def connectSpotify():
    username = os.environ.get('SPOTIPY_USER_ID')
    
    try:
        # Note: This will open a browser window for the user to log in and grant permissions.
        # After successful login, the user will be redirected to the specified redirect_uri.
        token_info = spotipy.util.prompt_for_user_token(username, scope='user-modify-playback-state')
    except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token_info = spotipy.util.prompt_for_user_token(username, scope='user-modify-playback-state')

    # Create Spotify object
    spotifyObject = spotipy.Spotify(auth=token_info['access_token'])
    user = spotifyObject.current_user()
    return spotifyObject

# Your client ID and secret
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# Authenticate and connect to Spotify
sp = authenticate(client_id, client_secret)
spotifyObject = connectSpotify()

# Now you can use `spotifyObject` to interact with the Spotify API on behalf of the authenticated user.
