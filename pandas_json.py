import json
import pandas as pd

def remove_duplicates(input_df):
    # Create list of bools representing duplicate songs
    # True for all entries with duplicates
    duplicates_mask = input_df.duplicated(keep="first", subset=['spotify_track_uri'])
    # Convert boolean list to excel
    # duplicates_mask.to_excel('duplicates_mask.xlsx')

    # Trim list of duplicate entries
    all_duplicates_removed = input_df[duplicates_mask==False]
    # all_duplicates.to_excel('all_duplicates.xlsx')

    return all_duplicates_removed

def get_songs_by_min_plays(song_list, min_plays):
    id_counts = song_list['spotify_track_uri'].value_counts()

    # Create a new DataFrame ordered by id counts
    sorted_df = pd.DataFrame({'spotify_track_uri': id_counts.index, 'count': id_counts.values})

    # Merge with the original DataFrame to include the corresponding names
    result_df = pd.merge(sorted_df, song_list, on='spotify_track_uri')

    # this was the original code: it just listed how many songs with
    # given number of plays. Doesnt account for duplicates AFAIK
    # for i in range(15):
        
    #     # This line is great - I love this line
    #     # creates a dataframe of all songs with count > i
    #     filtered_df = result_df[result_df['count'] >= i]

    #     print(f"Num songs with at least {i:2} plays: {len(filtered_df)}")
    
    output_file = "MIN_PLAYS.xlsx"
    result_df.to_excel(output_file)

    min_plays_cutoff = result_df[result_df['count'] >= min_plays]

    return min_plays_cutoff

def get_filtered_song_list(filtered_songs, min_plays=2):

    ordered_songs_by_count = get_songs_by_min_plays(filtered_songs, min_plays)
    # print(ordered_songs_by_count)

    removed_dupes = remove_duplicates(ordered_songs_by_count)

    return removed_dupes

if __name__=="__main__":
    filtered_data = pd.read_json('filtered_output.json')
    print("Num songs total: " + str(len(filtered_data)))

    ordered_songs_by_count = get_songs_by_min_plays(filtered_data, 5)
    # print(ordered_songs_by_count)

    removed_dupes = remove_duplicates(ordered_songs_by_count)

    print(removed_dupes)



# TODO
# Include count of each song as new data column in dataframe - figure out how