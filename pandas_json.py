import pandas as pd

songs = pd.read_json('filtered_output.json')

print(len(songs))
q = songs.drop_duplicates(subset=['spotify_track_uri'])
print(len(q))

duplicates_mask = songs.duplicated(keep=False, subset=['spotify_track_uri'])
duplicates_mask.to_excel('duplicates_mask.xlsx')


# All duplicate songs from filtered_output. includes multiple entries per song
all_duplicates = songs[duplicates_mask]

all_duplicates.to_excel('all_duplicates.xlsx')
print(len(all_duplicates))

single_duplicates_only = all_duplicates.drop_duplicates(subset=['spotify_track_uri'])


# TODO
# Include count of each song as new data column in dataframe - figure out how

single_duplicates_only.to_excel('single_duplicates_only.xlsx')
print(len(single_duplicates_only))


# songs.to_excel('filtered_songs.xlsx')