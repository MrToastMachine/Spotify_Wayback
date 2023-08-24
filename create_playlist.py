import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id="1f9f93179a6243cd8e6e7c18881c5afb", client_secret="6e9fc1642c714dfc9a962349706a18b8", redirect_uri="https://127.0.0.1/callback" ))


# Create a new playlist
playlist_name = "My New Playlist"
playlist_description = "A playlist created using Spotipy"
user_id = sp.me()['id']  # Get the user's Spotify ID

new_playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)
print(f"Created new playlist: {new_playlist['name']}")

# Add tracks to the playlist
track_uris = ['spotify:track:1gAPybZsQhhr7L8WgDneyj', 'spotify:track:6KfikoQae8sV8N0DaiLxRm']  # Replace with actual track URIs
sp.playlist_add_items(new_playlist['id'], track_uris)
print("Added tracks to the playlist.")