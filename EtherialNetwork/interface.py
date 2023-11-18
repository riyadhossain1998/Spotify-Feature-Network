from os import environ
from spotipy_connection import authenticate, connectSpotify
from artist_controller import getArtistInfo, searchArtistImage
from playlist_controller import graphDataGenerator

import json
# Home Menu
def runInterfaceMock1(spotifyObject):
    print("Hey you've connected to Spotify! What kind of data are you looking for?")
    print("A. Get artist information. (Default: Lil Uzi Vert")
    print("B. Get songs in a playlist. (Default: Lil Uzi Vert Playlist")
    print("C. Get song information.")
    print("D. Get album information.")
    print("E. Get label information.")
    print("F. Get artwork information.") 
       
    #pl_id = 'spotify:playlist:65lXmIYylmYIHrcy5PKQjY' #saduzisongs
    pl_id = 'spotify:playlist:2aBcEWYEVC6Ixrq6LplhBa' #Weeknd all
    #songs = extract_songlist(spotifyObject, pl_id)

    new = []
    
    prompt = input("Letter: ")
    if prompt == 'A':
        print(getArtistInfo(spotifyObject, '4O15NlyKLIASxsJ0PrXPfz'))
    elif prompt == 'B':
        graphDataGenerator(spotifyObject, pl_id, 'kidlaroi')
                    
          
    elif prompt == "C":
        spotifyObject.start_playback('67nepsnrcZkowTxMWigSbb')

    #   This was made to reorganize playlist data for UI purposes 
    elif prompt == "D":
                          
        # Opening JSON file
        f = open('./static/data/playlist-information.json')
        
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list
        print(data['artists'][0])
        updatedData = []
        for artist in data['artists']:
            #print(searchArtistImage(spotifyObject, artist['name'])['artists']['items'][0]['images'][0]['url'])
            
            info = searchArtistImage(spotifyObject, artist['name'])['artists']['items'][0]
            aName = info['name']
            aID = info['id']
            aImgUrl = info['images'][0]['url']
            
            
            newJSON = {
                "name" : artist['name'],
                "aName": aName,
                "id": aID,
                "imgUrl": aImgUrl,
                "pl_id": artist['pl_id']
            }
            updatedData.append(newJSON)
            
        with open('playlist-info-updated.json', 'w') as new_file:
            json.dump({"artists": updatedData}, new_file, indent=2)  # Indent for better readability (optional)
            
            
            
            
            

        
        
        #print(searchArtistImage(spotifyObject, 'weeknd')['artists']['items'][0]['images'][0]['url'])
    
    #   Using this to extract more information on the songs for displaying
    elif prompt == "E":
        
        # Opening JSON file
        f = open('./static/data/drake.json')
        
        
        # returns JSON object as 
        # a dictionary
        data = json.load(f)
        
        
        
        for track in data["links"]:
            try:
                track_info = spotifyObject.track(track["track_id"])
                track["album_art_url"] = track_info['album']['images'][0]['url']
                track["release_date"] = track_info['album']['release_date']
                track["duration_ms"] = track_info['duration_ms']
                track["explicit"] = track_info['explicit']
                print(f"Updated information for track {track['track_id']}")
            except Exception as e:
                print(f"Error updating information for track {track['track_id']}: {e}")
                
        

        
        with open('./static/data/drake.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

           
        
def main(spotifyObject):
    runInterfaceMock1(spotifyObject)
    
if __name__ == "__main__":
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    # Get a Spotify authenticated instance
    sp_instance = authenticate(CLIENT_ID, CLIENT_SECRET)
    spotifyObject = connectSpotify()
    main(spotifyObject)