import pandas as pd

songs = pd.read_json('filtered_output.json')

"""
print(type(songs))
q = songs.drop_duplicates(subset=['spotify_track_uri'])
print(len(q))
"""

# Returns list equal in length to input dataframe but with data replaced 
# with True or False denoting if song is repeated
duplicates_mask = songs.duplicated(keep=False, subset=['spotify_track_uri'])
# Convert boolean list to excel
duplicates_mask.to_excel('duplicates_mask.xlsx')


# All duplicate songs from filtered_output. includes multiple entries per song
# Equal to 'songs' list AND 'duplicates_mask' per entry
# Note: Still contains multiple entries per song
all_duplicates = songs[duplicates_mask]
all_duplicates.to_excel('all_duplicates.xlsx')
print(len(all_duplicates))

# Remove excess entries of each song, only one of each song should remain
single_duplicates_only = all_duplicates.drop_duplicates(subset=['spotify_track_uri'])

single_duplicates_only.to_excel('single_duplicates_only.xlsx')
print(len(single_duplicates_only))

# TODO
# Include count of each song as new data column in dataframe - figure out how