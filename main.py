import json
import os
import sys
from datetime import datetime
import pandas as pd

import tkCalendar
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



def get_json_data():
    input_file = "Full_Streaming_History.json"  # Change this to the path of your JSON input file

    if os.path.exists(input_file):
        print("Json exists: no need for zip file!")
        
        with open(input_file, "r", encoding="utf8") as file:
            json_data = json.load(file)

    else:
        print("Unzipping data and creating JSON database")
        json_data = unzip_spotify_data(input_file)

    return json_data

def get_title_from_dates(dates):
    start_date_old = datetime.strptime(dates[0], "%d/%m/%Y")
    start_date = start_date_old.strftime("%d/%m/%y")
    
    end_date_old = datetime.strptime(dates[1], "%d/%m/%Y")
    end_date = end_date_old.strftime("%d/%m/%y")

    if debug:
        print(f"Start Date Chosen: {start_date}")
        print(f"End Date Chosen: {end_date}")

    return f"Wayback [{start_date} - {end_date}]"

def filter_data_by_date_range(data, start_date, end_date):
    filtered_data = []

    for item in data:
        timestamp_str = item.get("ts")
        if timestamp_str:

            iso_datetime = datetime.strptime(timestamp_str.split("T")[0], "%Y-%m-%d")

            if start_date <= iso_datetime <= end_date:
                filtered_data.append(item)

    return filtered_data

if __name__ == "__main__":

    #Get JSON data from source file
    json_data = get_json_data()

    # Launch tkinter window to get playlist info. Options:
    #   - Start and End Date
    #   - Num plays cutoff
    playlist_specs = tkCalendar.get_playlist_info()
    print(f"playlist_specs : {playlist_specs}")

    # excessive but makes it clearer
    # playlist specs returns tuple (start date, end date, num plays)
    dates = [x for x in playlist_specs[:2]]
    num_song_plays = playlist_specs[2] if playlist_specs[2] else 2

    if debug:
        print(f"num_song_plays : {num_song_plays}")


    # Format dates to usable format
    start_date_str = dates[0] + " 00:00:01"
    end_date_str = dates[1] + " 23:59:59"
    start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%d/%m/%Y %H:%M:%S")

    # Create playlist title for spotify
    playlist_title = get_title_from_dates(dates)


    ##### PLAYLIST CURATION #####

    # trim data to chosen date range
    filtered_data = filter_data_by_date_range(json_data, start_date, end_date)
    pd_filtered_data = pd.DataFrame(filtered_data)

    if debug:
        print(f"Total songs in given date range: {len(filtered_data)}")

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

