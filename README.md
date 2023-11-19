# Spotify-Feature-Network


##  Introduction

This is a music visualization application built with Flask, D3.js & SpotiPy. 

##  Features

1. Explore music through artist-artist connections in the industry through features. The network is generated when the user clicks on an artist in the main menu, it reads through the playlist data of that artist and renders the graph.
   <br><br>
2. The application uses D3.js to render the network graph based on custom data that has been cleaned and condensed using Spotipy, Pandas in Python. The graph is interactable through drag & onclick. For now, onclick reveals a list of tracks of the artist clicked on.
   <br><br>
3. The data was once again modified with a custom function to retrieve and add more datatypes to display for increased usability. For example, giving users the ability to filter by release date, duration or popularity. [__IN PROGRESS__] -> Front-End Implementation 
   <br><br>
4. Once the list of song appears for the artist, the user can click on any song and it will play in the user's Spotify.
   <br><br>


##  Ongoing Tasks
1. Gather more data about more artists to visualize, fix the artist data that haven't been fetched yet.
   <br><br>
2. Create more user-friendly graph interactions.
   <br><br>
3. Expand on the artist modal displayed below.
   <br><br>
4. Queue, Play, Pause is also in progress, however integration with Siri is a challenge I might take on.
   <br><br>
