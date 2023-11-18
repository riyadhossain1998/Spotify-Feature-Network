
from typing import List

import json

import pandas as pd

from artist_controller import createNodes


#   1.  Playlist Controller retrieves playlist information
#       -   Playlist Length
#       -   Total number of songs in playlist
#       -   Extract Songlist retrieves a dictionary of data called "items" which include tracks
#       -   Tracks includes artists info, duration, link to song, song ID, name, popularity & preview url
#       -   Can create links and get other variables about the song
#       -   Gets list of artists from links


#   =================       Spotify Object Controls     =====================


#   This function retrieves length of the playlist
def get_pl_length(spotifyObject, pl_uri: str) -> int:
    return spotifyObject.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"

    )["total"]

#   This function retrieves total number of songs in a playlist
def get_count_of_songs_in_playlist(spotifyObject, pl_uri: str) -> int:
    return spotifyObject.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"
    )["total"]

#   This function retrieves list of all songs (+ preview url, release date, artists info, popularity)
def get_tracks(spotifyObject, pl_uri: str) -> List:
       
    tracks = {"items":[]}
    pl_length = get_pl_length(spotifyObject, pl_uri)
    offset = 0
    count = 0
    total = 0
    while offset != pl_length:
        total = get_count_of_songs_in_playlist(spotifyObject, pl_uri)
        tracks_batch = spotifyObject.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track.name,items.track.id,items.track.popularity,items.track.duration_ms,items.track.external_urls,items.track.preview_url,items.track.artists(total,name,id)"
        )
        for track_item in tracks_batch['items']:
            track = track_item['track']
            organized_track_info = {
                'id': track['id'],
                'name': track['name'],
                'artists': [{'name': artist['name'], 'id': artist['id']} for artist in track['artists']],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'external_urls': track['external_urls'],
                'preview_url': track['preview_url'],
                
            }
            tracks['items'].append(organized_track_info)

        offset += len(tracks_batch['items'])
    #print(len(tracks['items']))
    #print(json.dumps(tracks, indent=4))
    return tracks


#   =================       Graph Data Controls     =====================


#   Creating the graph data
def graphDataGenerator(spotifyObject, pl_uri, artistName):
    tracks = get_tracks(spotifyObject, pl_uri)
    print(artistName + ' playlist loading')
    print('a. tracks retrieved.')
    #print(json.dumps(tracks, sort_keys=True, indent=4))
    links = createConnection(tracks)    #---------------------------------> LINKS VARIABLE (In DataFrame)
    print("b. links created")
    artist_list = getArtistList(links['source'], links['target'])
    print("c. artist list created post-merge")
        
    

    
    #print(merged_list)  #   Artists for Nodes
    nodes = createNodes(spotifyObject, artist_list) #---------------------------------> NODES VARIABLE (In JSON)
    print("d. nodes created")
    links_dict = {"links": links.to_dict('records')} #---------------------------------> LINKS VARIABLE (In JSON)
    print("e. links created")
    #print(nodes)
    #nodes_2 = getArtistSongList(tracks, artist_list, nodes)
    
    for artist in artist_list:
        tracklist = getArtistSongList(tracks, artist)
        #print(tracklist)
        for node in nodes['nodes']:
            if(node['artist_id'] == artist):
                node['tracklist'] = tracklist
                
    print("f. tracklist added to nodes")
                
    graph_data = {"nodes": [], "links": []} 
    
    
    for link in links_dict["links"]:
        graph_data["links"].append(link)
    
    
    for node in nodes['nodes']:
        graph_data["nodes"].append(node)
    
    print("g. graph data created for " + artistName)
        
        

    #graph_data = nodes, links_dict
    #a=json.dumps(graph_data, sort_keys=True, indent=4)

    filename = "static/data/" + artistName + ".json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=4)
    
    #print(a)    
    return graph_data




#   Looks for artist in tracks and creates a list of song IDs by that artist on that playlist    
def getArtistSongList(tracks, artist_id):
    songlist = []
    
    
    for eachTrack in tracks['items']:
        for artist in eachTrack['artists']:
            if artist['id'] == artist_id:
                song_id = eachTrack['id']
                songlist.append(song_id)
    
    return songlist
    


#   Gets list of all artists from links dictionary (LINKS FUNCTION)
def getArtistList(sourceList, targetList):
    merged_list = list(set(sourceList.tolist() + targetList.tolist()))
    return(merged_list)
    
    

#   Algorithm for creating connections (LINKS FUNCTION)
def createConnection(tracks):
    link = {"source": "", "target": "", "connection_id": "", "track_id":"", "collab_count": "", "name": "", "popularity": "","preview_url": "", "spotify_link": ""}
    links = {"links": []}

    for eachTrack in tracks['items']:
        track_id = eachTrack['id']
        #print(eachTrack['artists'])
        # Get a list of all artists for the track
        artists = [artist['id'] for artist in eachTrack['artists']]    #   Toggle id to name to see name of artist for clarity
        artists.sort() # sort the artist IDs in ascending order
        
        # Create connections between all possible pair of artists (On^2)
        for i in range(len(artists)):
            for j in range(i+1, len(artists)):
                source = artists[i]
                target = artists[j]
                connection_id = f"{source}_{target}_{track_id}"
                name = eachTrack['name']
                popularity = eachTrack['popularity']
                preview_url = eachTrack['preview_url']
                spotify_link = eachTrack['external_urls']['spotify']

                
                link = {
                    "source": source,
                    "target": target,
                    "connection_id": connection_id,
                    "track_id": track_id,
                    "collab_count": 0,
                    "name": name,
                    "popularity": popularity,
                    "preview_url": preview_url,
                    "spotify_link": spotify_link
                }
                

                links["links"].append(link)

    #print(json.dumps(links, sort_keys=True, indent=4))
    count_collab_links = countCollabs(links)
    #print(count_collab_links)
        
    #result = count_collab_links.to_dict('records')      #   In Dataframe
    #print(json.dumps(result, sort_keys=True, indent=4))     #   In JSON
    return count_collab_links
    


#   Collaboration Counter Function - part of createConnection (LINKS FUNCTION)
def countCollabs(links):
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(links['links'])

    # Group the DataFrame by 'source' and 'target', and count the number of occurrences
    collab_counts = df.groupby(['source', 'target']).size().reset_index(name='collab_count')

    # Sort the DataFrame by 'source', 'target', and 'collab_count' in descending order
    collab_counts = collab_counts.sort_values(by=['source', 'target', 'collab_count'], ascending=[False, False, False])
    
    # Merge the collab_counts DataFrame with the original df DataFrame
    df = pd.merge(df, collab_counts[['source', 'target', 'collab_count']], on=['source', 'target'], how='left', suffixes=('_left', ''))


    # Convert the DataFrame to a list of dictionaries
    result = collab_counts.to_dict('records')
    df = df.drop('collab_count_left', axis=1)



    # Return the result
    return df
    #print(collab_counts)
    
    
    





