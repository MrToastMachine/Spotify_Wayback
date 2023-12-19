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

def get_top_played(song_list, num_plays):
    sorted_songs = sorted(song_list, key=song_list.count)
    song_data  = [(song_list["master_metadata_track_name"][x], song_list["spotify_track_uri"][x]) for x in range(len(song_list))]
    sorted_songs = sorted_songs.reverse()

    no_dupes = sorted_songs.drop_duplicates(subset=['spotify_track_uri'])
    for song in no_dupes:
        print(song.count, song[0])

def remove_single_occurrences(filtered_songs):
    print("here bud")
    # tk_setup()

    # get_top_played(filtered_songs, 5)

    duplicates_mask = filtered_songs.duplicated(keep=False, subset=['spotify_track_uri'])
    # Convert boolean list to excel
    # duplicates_mask.to_excel('duplicates_mask.xlsx')

    all_duplicates = filtered_songs[duplicates_mask]
    # all_duplicates.to_excel('all_duplicates.xlsx')

    single_duplicates_only = all_duplicates.drop_duplicates(subset=['spotify_track_uri'])

    # single_duplicates_only.to_excel('single_duplicates_only.xlsx')

    gooas
    return single_duplicates_only


if __name__=="__main__":
    filtered_data = pd.read_json('filtered_output.json')
    print("Num songs total: " + str(len(filtered_data)))

    id_counts = filtered_data['spotify_track_uri'].value_counts()

    # Create a new DataFrame ordered by id counts
    sorted_df = pd.DataFrame({'spotify_track_uri': id_counts.index, 'count': id_counts.values})


    # Merge with the original DataFrame to include the corresponding names
    result_df = pd.merge(sorted_df, filtered_data, on='spotify_track_uri')

    for i in range(15):
        
        # This line is great - I love this line
        # creates a dataframe of all songs with count > i
        filtered_df = result_df[result_df['count'] > i]

        print(f"Num songs with {i:2} plays: {len(filtered_df)}")

    # print(filtered_df["master_metadata_track_name"])

    # print(result_df["master_metadata_track_name"])

    # for song in filtered_data["master_metadata_track_name"]:
    #     print(song)

    # filtered_data = pd.DataFrame(songs)

    # remove_single_occurrences(filtered_data)



# TODO
# Include count of each song as new data column in dataframe - figure out how