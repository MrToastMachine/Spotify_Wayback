# This App creates a tk window to allow selection of two dates
# From this we can select songs listened to within the date range

import tkinter as tk
from tkcalendar import Calendar
from pandas_json import *
from create_playlist import *
from tkLoadFile import *
from datetime import datetime


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

        playlist_curation(pd_filtered_data, playlist_title)
    
    #Get JSON data from source file
    json_data = get_json_data()    

    earliest_date, latest_date = get_available_data_range(pd.DataFrame(json_data))

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

    def getCount():

        top_5_song_names = get_top_x_songs(song_list, 5, names_only=True)

        song_listbox.delete(0,END)
        # Insert each song into the listbox
        for i, song in enumerate(top_5_song_names):
            song_listbox.insert(tk.END, f"{i+1:2}.\t" + song)

        top_5_artist_names = get_top_artists(song_list, 5)

        artist_listbox.delete(0,END)
        # Insert each song into the listbox
        for i, artist in enumerate(top_5_artist_names):
            artist_listbox.insert(tk.END, f"{i+1:2}.\t" + artist)

    def returnToDateSelection():
        app.destroy()

        prompt_for_dates()

    def createSpotifyPlaylist():
        try:
            num_songs = int(num_entry.get())
        except:
            tk.messagebox.showinfo(
                title="Not a number bud",
                message=f"Please input a positive number"
            )

        final_song_list = get_filtered_song_list(song_list, num_songs)

        if not isinstance(final_song_list, pd.DataFrame):
            print("No songs selected!")
            print(type(final_song_list))
            return
        
    
        create_new_playlist(final_song_list, playlist_title)
        app.quit()
    
    def showAllSongs():
        pass


    row_num = 0

    # ------------ ROW 0 ----------------

    #APP STRUCTURE SETUP - PLAYLIST INFO
    app = tk.Tk()
    app.title("Playlist information")
    app.geometry("625x350")

    # Number input box
    num_label = tk.Label(app, text="Number of Top Songs")
    num_label.grid(row=row_num, column=0, padx=5, pady=5)

    num_entry = tk.Entry(app)
    num_entry.grid(row=row_num, column=2, padx=5, pady=5)

    select_button = tk.Button(app, text="Confirm", command=getCount)
    select_button.grid(row=row_num, column=3, padx=5, pady=5)

    # ------------ NEW ROW ----------------
    row_num += 1

    # Create a label for the heading
    top_songs_label = tk.Label(app, text="Top Songs", font=("Helvetica", 14, "bold"))
    top_songs_label.grid(row=row_num, column=0, columnspan=2, padx=20, pady=5)

    # Create a label for the heading
    top_artists_label = tk.Label(app, text="Top Artists", font=("Helvetica", 14, "bold"))
    top_artists_label.grid(row=row_num, column=2, columnspan=2, pady=5)

    # ------------ NEW ROW ----------------
    row_num += 1

    # Create a listbox to display the songs
    song_listbox = tk.Listbox(app, selectmode=tk.SINGLE, font=("Helvetica", 14))

    # Configure the Listbox widget to set the width to its content
    song_listbox.configure(background="black", foreground="white", font=('Aerial 13'), width=26, height=10)
    song_listbox.grid(row=row_num, column=0, columnspan=2, padx=40, pady=5)

    # Create a listbox to display the artists
    artist_listbox = tk.Listbox(app, selectmode=tk.SINGLE, font=("Helvetica", 14))

    # Configure the Listbox widget to set the width to its content
    artist_listbox.configure(background="black", foreground="white", font=('Aerial 13'), width=26, height=10)
    artist_listbox.grid(row=row_num, column=2, columnspan=2, padx=20, pady=10)

    # ------------ NEW ROW ----------------
    row_num += 1

    select_button = tk.Button(app, text="Create Playlist", command=createSpotifyPlaylist)
    select_button.grid(row=row_num, columnspan=4, padx=0, pady=5)

    # ------------ NEW ROW ----------------
    row_num += 1

    select_button = tk.Button(app, text="Date Selection", command=returnToDateSelection)
    select_button.grid(row=row_num, column=0, columnspan=2, padx=0, pady=5)


    show_all_songs_button = tk.Button(app, text="Show all songs", command=showAllSongs)
    show_all_songs_button.grid(row=row_num, column=2, columnspan=2, padx=0, pady=5)



    app.mainloop()

# Jumps straight to playlist modification window
def playlist_info_debugging():
    song_list = pd.read_json('filtered_output.json')

    playlist_curation(song_list, "TEST PLAYLIST")

if __name__ == "__main__":

    prompt_for_dates()

    # playlist_info_debugging()

