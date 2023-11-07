import json
import os
import sys
from datetime import datetime
import pandas as pd

import tkCalendar
from pandas_json import remove_single_occurrences
from create_playlist import *
from tk_load_file import *

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

def getTitleFromDates(dates):
    start_date_old = datetime.strptime(dates[0], "%d/%m/%Y")
    start_date = start_date_old.strftime("%d/%m/%y")
    
    end_date_old = datetime.strptime(dates[0], "%d/%m/%Y")
    end_date = end_date_old.strftime("%d/%m/%y")

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

    json_data = get_json_data()

    dates = tkCalendar.launch_date_picker()

    start_date_str = dates[0] + " 00:00:01"
    end_date_str = dates[1] + " 23:59:59"
    print(start_date_str, end_date_str)

    start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M:%S")
    end_date = datetime.strptime(end_date_str, "%d/%m/%Y %H:%M:%S")

    playlist_title = getTitleFromDates(dates)

    print(start_date, end_date)


    # filtered_data is of type 'list'
    filtered_data = filter_data_by_date_range(json_data, start_date, end_date)
    pd_filtered_data = pd.DataFrame(filtered_data)


    output_file = "filtered_output.json"
    with open(output_file, "w") as file:
        json.dump(filtered_data, file, indent=4)

    print(f"Filtered data saved to '{output_file}'.")

    print("Removing songs that were only played once...")

    final_playlist = remove_single_occurrences(pd_filtered_data)

    print("Successfully trimmed...")

    create_new_playlist(final_playlist, playlist_title)


