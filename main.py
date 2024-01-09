import json
import os
from datetime import datetime
import pandas as pd

import tkWindowManager
from pandas_json import *
from create_playlist import *
from tk_load_file import *

debug = False

debug_msg_on = " DEBUG MODE ON "
debug_msg_off = " DEBUG MODE OFF "

if debug:
    print(f"{debug_msg_on:#^50}")
else:
    print(f"{debug_msg_off:#^50}")



if __name__ == "__main__":

    tkWindowManager.prompt_for_dates()

    """

    # write trimmed list to intermediate json file
    output_file = "filtered_output.json"
    with open(output_file, "w") as file:
        json.dump(filtered_data, file, indent=4)
    print(f"Filtered data saved to '{output_file}'.")

    # remove songs with less than 'num_song_plays' plays
    final_playlist = get_filtered_song_list(pd_filtered_data, min_plays=num_song_plays)
    print(f"Successfully removed songs with less than {num_song_plays} plays...")

    if debug:
        print(f"Num songs to add to playlist: {len(final_playlist)}")

    final_playlist.to_excel("final_list.xlsx")

    if not debug:
        create_new_playlist(final_playlist, playlist_title)

    """
