import json
import os

def printSongs(fileName):
    with open(fileName, 'r', encoding="utf8") as f:
        data = json.load(f)

    for song in data[0:100]:
        print(song["master_metadata_track_name"], "------", song["master_metadata_album_artist_name"])
        

# assign directory
directory = '.'

allFiles = []

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f) and (".json" in f):
        allFiles.append(f)

numSongs = 0

for file in allFiles:
    with open(file, 'r', encoding="utf8") as file:
        data = json.load(file)
        numSongs += len(data)

printSongs(allFiles[0])