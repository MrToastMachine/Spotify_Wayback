import json
import pandas as pd

intermediate_files = False

def remove_duplicates(input_df, key='spotify_track_uri'):
    # Create list of bools representing duplicate songs
    # True for all entries with duplicates
    duplicates_mask = input_df.duplicated(keep="first", subset=[key])

    # Trim list of duplicate entries
    all_duplicates_removed = input_df[duplicates_mask==False]

    return all_duplicates_removed

def get_songs_by_min_plays(song_list, min_plays):
    print(song_list)
    id_counts = song_list['spotify_track_uri'].value_counts()

    # Create a new DataFrame ordered by id counts
    sorted_df = pd.DataFrame({'spotify_track_uri': id_counts.index, 'count': id_counts.values})

    # Merge with the original DataFrame to include the corresponding names
    result_df = pd.merge(sorted_df, song_list, on='spotify_track_uri')

    no_duplicates = remove_duplicates(result_df)

    min_plays_cutoff = no_duplicates[no_duplicates['count'] >= min_plays]

    return min_plays_cutoff

def get_top_artists(song_list, num_top_artists):
    artist_playcount = song_list['master_metadata_album_artist_name'].value_counts()

    # Create a new DataFrame ordered by id counts
    sorted_df = pd.DataFrame({'master_metadata_album_artist_name': artist_playcount.index, 'count': artist_playcount.values})

    # Merge with the original DataFrame to include the corresponding names
    result_df = pd.merge(sorted_df, song_list, on='master_metadata_album_artist_name')

    no_duplicates = remove_duplicates(result_df, key='master_metadata_album_artist_name')

    return no_duplicates[:num_top_artists]


def get_filtered_song_list(filtered_songs, min_plays=2):

    ordered_songs_by_count = get_songs_by_min_plays(filtered_songs, min_plays)
    # print(ordered_songs_by_count)

    # removed_dupes = remove_duplicates(ordered_songs_by_count)

    if intermediate_files:
        output_file = "FINAL_PLAYLIST.xlsx"
        ordered_songs_by_count.to_excel(output_file)

    return ordered_songs_by_count

if __name__=="__main__":
    filtered_data = pd.read_json('filtered_output.json')
    print("Num songs total: " + str(len(filtered_data)))

    ordered_songs_by_count = get_songs_by_min_plays(filtered_data, 5)
    # print(ordered_songs_by_count)

    removed_dupes = remove_duplicates(ordered_songs_by_count)

    print(removed_dupes)
