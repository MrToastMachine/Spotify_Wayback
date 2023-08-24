import json

song_names = []

with open("filtered_output.json", "r", encoding="utf8") as file:
    json_data = json.load(file)

    song_names = [x["master_metadata_track_name"] for x in json_data]

most = max(song_names, key=song_names.count)
sorted_songs = sorted(song_names, key=song_names.count)

goop = sorted_songs.reverse()

print(most)
print(sorted_songs[:20])