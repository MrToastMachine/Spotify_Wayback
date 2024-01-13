import pandas as pd
from pandas_json import *

if __name__=="__main__":
    filtered_data = pd.read_json('filtered_output.json')
    print("Num songs total: " + str(len(filtered_data)))

    ordered_songs_by_count = get_songs_by_min_plays(filtered_data, 5)
    # print(ordered_songs_by_count)

    df = remove_duplicates(ordered_songs_by_count)

    top_5_song_names = get_top_x_songs(df, 5)
    for song in top_5_song_names:
        print(song)
    