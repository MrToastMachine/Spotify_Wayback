# This App creates a tk window to allow selection of two dates
# From this we can select songs listened to within the date range

import tkinter as tk
from tkcalendar import Calendar
from pandas_json import *
from create_playlist import *
from main import *
import time

debug = True

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

def get_available_data_range(dataset):
    earliest_date_ts = dataset.iloc[0].get("ts")
    if earliest_date_ts:

        iso_datetime = datetime.strptime(earliest_date_ts.split("T")[0], "%Y-%m-%d")
        earliest_date = iso_datetime.strftime("%d %b %Y")
    
        latest_date_ts = dataset.iloc[-1].get("ts")
        if latest_date_ts:

            iso_datetime = datetime.strptime(latest_date_ts.split("T")[0], "%Y-%m-%d")
            latest_date = iso_datetime.strftime("%d %b %Y")
            return (earliest_date, latest_date)


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

def prompt_for_dates():

    def us_to_uk_date(us_date):
        parts = us_date.split('/')
        uk_date = f"{parts[1]}/{parts[0]}/20{parts[2]}"
        return uk_date

    def on_date_select():
        # Doing this isnt great - should find better way
        # global start_date
        # global end_date

        start_date_us = cal_start.get_date()
        end_date_us = cal_end.get_date()
        start_date_str = us_to_uk_date(start_date_us)
        end_date_str = us_to_uk_date(end_date_us)

        start_date = datetime.strptime(start_date_str + " 00:00:01", "%d/%m/%Y %H:%M:%S")
        end_date = datetime.strptime(end_date_str + " 23:59:59", "%d/%m/%Y %H:%M:%S")

        # Create playlist title for spotify
        playlist_title = get_title_from_dates([start_date_str, end_date_str])

        ##### PLAYLIST CURATION #####
        # trim data to chosen date range
        filtered_data = filter_data_by_date_range(json_data, start_date, end_date)
        pd_filtered_data = pd.DataFrame(filtered_data)

        date_app.destroy()

        print(pd_filtered_data)
        playlist_curation(pd_filtered_data, playlist_title)
    
    #Get JSON data from source file
    json_data = get_json_data()    

    earliest_date, latest_date = get_available_data_range(pd.DataFrame(json_data))
    print(earliest_date, latest_date)

    #APP STRUCTURE SETUP - DATE PICKER
    date_app = tk.Tk()
    date_app.title("Date Picker")

    CURRENT_ROW = 0

    song_count_label = tk.Label(date_app, text=f"Date Range Available: {earliest_date} to {latest_date}")
    song_count_label.grid(row=CURRENT_ROW, columnspan=3, padx=10, pady=5)

    CURRENT_ROW += 1

    cal_start = Calendar(date_app, selectmode="day")
    cal_start.grid(row=CURRENT_ROW, column=0, padx=10, pady=5)

    cal_end = Calendar(date_app, selectmode="day")
    cal_end.grid(row=CURRENT_ROW, column=1, padx=10, pady=5)

    CURRENT_ROW += 1

    # select_button = tk.Button(date_app, text="Select Dates", command=return )
    select_button = tk.Button(date_app, text="Confirm", command=on_date_select)
    # select_button.grid(row=1, columnspan=2, padx=10, pady=5)
    select_button.grid(row=CURRENT_ROW, columnspan=2, padx=10, pady=5)

    date_app.mainloop()


def playlist_curation(song_list, playlist_title):
    num_songs_in_list = 0

    def getCount():
        global songs_with_min_plays
        global num_songs_in_list

        try:
            min_plays = int(num_entry.get())
        except:
            tk.messagebox.showinfo(
                title="Not a number bud",
                message=f"Please input a positive number"
            )

        print(f"Number chosen: {min_plays}")

        songs_with_min_plays = get_filtered_song_list(song_list, min_plays)

        num_songs_in_list = len(songs_with_min_plays)

        song_count_label.config(text=f"Number of songs in list: {num_songs_in_list}")

        print(f"Number of songs in playlist: {num_songs_in_list}")
        top_artists = get_top_artists(songs_with_min_plays, 5)

        print("Top Artists:")
        print(top_artists)

    def returnToDateSelection():
        app.destroy()

        prompt_for_dates()

    def createSpotifyPlaylist():
        if not isinstance(songs_with_min_plays, pd.DataFrame):
            print("No songs selected!")
            print(songs_with_min_plays)
            return
        
    
        create_new_playlist(songs_with_min_plays, playlist_title)
        app.quit()


    row_num = 0

    # ------------ ROW 0 ----------------

    #APP STRUCTURE SETUP - PLAYLIST INFO
    app = tk.Tk()
    app.title("Playlist information")
    # app.geometry("500x600")

    # Number input box
    num_label = tk.Label(app, text="Num Plays")
    num_label.grid(row=row_num, column=0, padx=10, pady=5)

    num_entry = tk.Entry(app)
    num_entry.grid(row=row_num, column=1, padx=10, pady=5)

    # ------------ NEW ROW ----------------
    row_num += 1

    song_count_label = tk.Label(app, text=f"Number of songs in list: {num_songs_in_list}")
    song_count_label.grid(row=row_num, columnspan=3, padx=10, pady=5)

    # ------------ NEW ROW ----------------
    row_num += 1

    select_button = tk.Button(app, text="Confirm", command=getCount)
    select_button.grid(row=row_num, columnspan=3, padx=10, pady=5)

    # ------------ NEW ROW ----------------
    row_num += 1

    select_button = tk.Button(app, text="Date Selection", command=returnToDateSelection)
    select_button.grid(row=row_num, column=0, padx=10, pady=5)

    select_button = tk.Button(app, text="Create Playlist", command=createSpotifyPlaylist)
    select_button.grid(row=row_num, column=2, padx=10, pady=5)



    app.mainloop()

# Jumps straight to playlist modification window
def playlist_info_debugging():
    song_list = pd.read_json('filtered_output.json')

    playlist_curation(song_list, "TEST PLAYLIST")

if __name__ == "__main__":

    prompt_for_dates()

