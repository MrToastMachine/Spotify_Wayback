# USE python 3.11.5

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Get current date
current_date = datetime.now()

# Format the date as DD-MM-YYYY
formatted_date = current_date.strftime("%d-%m-%Y")

# print(f"Current Date: {formatted_date}")

scope = "playlist-modify-public"

credentials_manager = SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, open_browser=False)

# sp = spotipy.Spotify(auth_manager=credentials_manager)
sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

user_id = sp.me()['id']  # Get the user's Spotify ID

def create_new_playlist(song_list, playlist_name=None, playlist_desc=None):

    # Instead of this:
    #   while nextSong in list exists, add it until no more songs
    print(f"Num songs to add: {len(song_list)}")

    if playlist_name == None:
        playlist_name = "Wayback_" + formatted_date
    if playlist_desc == None:
        playlist_desc = "Wayback playlist created on " + formatted_date
    
    song_uri_list = song_list['spotify_track_uri'].tolist()

    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_desc)
    print(f"Created new playlist: {new_playlist['name']}")

    # sp.playlist_add_items(new_playlist['id'], song_uri_list)
    # print("Added tracks to the playlist.")
    print("Adding songs...")
    for i in range(len(song_uri_list)):
        # print(song_uri_list[i])
        try:
            sp.playlist_add_items(new_playlist['id'], [song_uri_list[i]])
        except:
            print(f"Error adding track {song_uri_list[i]}")

    print("Complete!")

run = False
if run:
    # INPUT FILE
    file_path = 'single_duplicates_only.xlsx'
    df = pd.read_excel(file_path)
    song_uri_list = df['spotify_track_uri'].tolist()

    # Create a new playlist
    playlist_name = "Wayback_" + formatted_date
    playlist_description = "A playlist created using Spotipy on " + formatted_date
    user_id = sp.me()['id']  # Get the user's Spotify ID

    new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)
    print(f"Created new playlist: {new_playlist['name']}")

    # Add tracks to the playlist
    track_uris = ['spotify:track:1gAPybZsQhhr7L8WgDneyj', 'spotify:track:6KfikoQae8sV8N0DaiLxRm']  # Replace with actual track URIs

    sp.playlist_add_items(new_playlist['id'], song_uri_list)
    print("Added tracks to the playlist.")
    