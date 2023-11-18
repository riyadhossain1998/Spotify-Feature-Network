# This file will focus on gathering everything related to the artist for the UI
from json.decoder import JSONDecodeError
import json
from typing import Dict
import pandas as pd
import numpy as np

#   Change to Artist Info Controller


def searchArtistImage(spotifyObject, name):
    results = spotifyObject.search(q='artist:' + name, type='artist')
    return results
    
def searchArtistImageFromList(spotifyObject):
    artist_list = ['akon', 'eminem', 'drake', 'lil wayne', 'kanye west', 'chris brown', 'kendrick lamar','nicki minaj', 'rihanna',
    'justin bieber','juice wrld','travis scott','ed sheeran','cardi b', 'future']
    #print(artists["Eminem"]["spotify_id"]) Get spotify artist ID
    
    for i in artist_list:
        results = spotifyObject.search(q='artist:' + i, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            artist = items[0]
            print(artist['name'], artist['images'][0]['url']) # Prints image of artists in array
    
#   Retrieving artist information
def getArtistInfo(spotifyObject, artist_id):
    try:
        #   For now retrieving names, images, id, profile_url, genres, popularity, genres, popularity
        
        #   Retreiving ARTIST DATA using artist_id:
        artist = spotifyObject.artist(artist_id)
        #print(json.dumps(artist, sort_keys=True, indent=4)) -- PRINT STATEMENT
        
        #   STRING DATA
        name = artist['name']
        
        #   INTEGER DATA
        popularity = int(artist['popularity'])
        followers = int(artist['followers']['total'])
        
        #   URL DATA
        if len(artist['images']) == 0:
            img_url = 'https://www.seekpng.com/ima/u2w7w7y3i1o0a9o0/'
        else:
            img_url = artist['images'][0]['url']
        
        profile_url = artist['external_urls']['spotify']
        
        #   LIST DATA
        genres = artist['genres']
        
        #   Creating node data bundle
        artist_dict = {
            "name": name,
            "artist_id": artist_id,
            "popularity": popularity,
            "followers": followers,
            "img_url": img_url,
            "profile_url": profile_url,
            "genres": genres,
            "tracklist":[]
        }
        #print(artist_dict)
        
        return artist_dict
    except Exception as e:
        print(f"Error occurred in getArtistInfo: {e}")
        return None
    
    
def createNodes(spotifyObject, artist_list):
    nodes = {"nodes": []}
    for artist in artist_list:
        #print(artist)
        artist_dict = getArtistInfo(spotifyObject, artist)
        nodes["nodes"].append(artist_dict)
    return nodes