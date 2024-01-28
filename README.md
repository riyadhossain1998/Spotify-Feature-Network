# Spotify-Feature-Network


##  Introduction

This is a music visualization application built with Flask, D3.js & SpotiPy. 

##  Features

1. The network is generated when the user clicks on an artist's discography renders the graph connecting all the artists who they have collaborated with.
   <br><br>
2. The application uses <b>D3.js</b> to render the network graph based on custom data that has been cleaned and organized from Spotify with <a href="https://pandas.pydata.org/">pandas</a>. The graph is a sandbox and can be interacted by dragging & clicking. 
   <br><br>
   a) Dragging: [Move artist nodes]
   b) Clicking: [Displays a table with all the tracks in the playlist with duration, release date and popularity. <b>Clicking each plays the song</b>]
   <br><br>


##  Ongoing Tasks
1. Gather more data about more artists to visualize, fix the artist data that haven't been fetched yet.
   <br><br>
2. Create more user-friendly graph interactions.
   <br><br>
3. Expand on the artist modal displayed below.
   <br><br>
4. Host in a live server with login functionalities for people to experiment and make art </mark>(Possibility of an interactive music sandbox, further smoothing and testing required)



##   How To Use

1. You will need to sign up and create a Spotify Developer Account and collect the following credentials and store it in the spotify-connection.py file.
   <br><br>
   a) SPOTIFY_USER_ID= [Can be obtained from Spotify PC App under Profile]
   b) SPOTIFY_CLIENT_ID [From Spotify Developer Account after creating an account]
   c) SPOTIFY_CLIENT_SECRET [From Spotify Developer Account after creating an account]
   b) SPOTIFY_REDIRECT_URI [From Spotify Developer Account after creating an account, you can set it yourself i used google.com/]
   <br><br>
2. [TESTING/SANDBOX] Run spotify-connection.py to set up environments and connect to Spotify. Then run interface.py to create and edit graph data to display on the web page.
3. In order to run the webpage, run app.py to run a Flask server. The code for Spotify Connection is also working for the webpage and it allows you to play whichever track you wish from the track data rendered for the artist node.

