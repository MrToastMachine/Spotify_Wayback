import json
import tkinter as tk
from tkinter import messagebox
import pandas as pd


def tk_setup():
    def get_user_input():
        num_top_songs = num_entry.get()
        show_top_artists = show_artists_var.get()

        # You can do something with the user input here, like print or display a message box
        message = f"Num Top Songs: {num_top_songs}\nShow Top Artists: {show_top_artists}"
        messagebox.showinfo("User Input", message)
        print(f"User chose:\n\tNum Top Songs: {num_top_songs}\n\tShow Top Artists: {show_top_artists}")

        window.quit()

    # Create the main window
    window = tk.Tk()
    window.title("User Input Form")

    # Number input box
    num_label = tk.Label(window, text="Num Plays")
    num_label.pack(pady=5)
    num_entry = tk.Entry(window)
    num_entry.pack(pady=5)

    # Toggle button for showing top artists
    show_artists_var = tk.BooleanVar()
    show_artists_button = tk.Checkbutton(window, text="Show Top Artists", variable=show_artists_var)
    show_artists_button.pack(pady=5)

    # Confirm button
    confirm_button = tk.Button(window, text="Confirm", command=get_user_input)
    confirm_button.pack(pady=10)

    window.mainloop()

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

    for i in range(15):
        
        # This line is great - I love this line
        # creates a dataframe of all songs with count > i
        filtered_df = result_df[result_df['count'] >= i]

        print(f"Num songs with at least {i:2} plays: {len(filtered_df)}")
    
    output_file = "MIN_PLAYS.xlsx"
    result_df.to_excel(output_file)

    min_plays_cutoff = result_df[result_df['count'] >= min_plays]

    print(min_plays_cutoff)
    return min_plays_cutoff

def get_num_songs_at_least_m_plays(song_list, m):
    id_counts = song_list['spotify_track_uri'].value_counts()

    # Create a new DataFrame ordered by id counts
    sorted_df = pd.DataFrame({'spotify_track_uri': id_counts.index, 'count': id_counts.values})

    # Merge with the original DataFrame to include the corresponding names
    result_df = pd.merge(sorted_df, song_list, on='spotify_track_uri')
        
    # This line is great - I love this line
    # creates a dataframe of all songs with count > i
    filtered_df = result_df[result_df['count'] >= m]

    num_songs = len(filtered_data)

    print(f"Num songs with at least {m:2} plays: {num_songs}")

    return num_songs

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