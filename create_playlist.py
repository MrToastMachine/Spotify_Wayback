import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import pandas as pd

CLIENT_ID = "1f9f93179a6243cd8e6e7c18881c5afb"
CLIENT_SECRET = "6e9fc1642c714dfc9a962349706a18b8"
REDIRECT_URI = "https://localhost/callback"

# INPUT FILE
file_path = 'single_duplicates_only.xlsx'
df = pd.read_excel(file_path)
song_uri_list = df['spotify_track_uri'].tolist()

# Get current date
current_date = datetime.now()

# Format the date as DD-MM-YYYY
formatted_date = current_date.strftime("%d-%m-%Y")

print(f"Current Date: {formatted_date}")

scope = "playlist-modify-public"

credentials_manager = SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, open_browser=False)

# sp = spotipy.Spotify(auth_manager=credentials_manager)
sp = spotipy.Spotify(client_credentials_manager=credentials_manager)


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