# This App creates a tk window to allow selection of two dates
# From this we can select songs listened to within the date range

import tkinter as tk
from tkcalendar import Calendar

start_date = ""
end_date = ""
num_song_plays = 0

def us_to_uk_date(us_date):
    parts = us_date.split('/')
    uk_date = f"{parts[1]}/{parts[0]}/20{parts[2]}"
    return uk_date

def on_date_select():
    # Doing this isnt great - should find better way
    global start_date
    global end_date
    global num_song_plays

    start_date_us = cal_start.get_date()
    end_date_us = cal_end.get_date()
    start_date = us_to_uk_date(start_date_us)
    end_date = us_to_uk_date(end_date_us)
    # result_label.config(text=f"Start Date (UK format): {start_date_uk}\nEnd Date (UK format): {end_date_uk}")

    try:
        num_song_plays = int(num_entry.get())
        app.quit()

    except:
        print("Num entries inputted is not a number")

    

#APP STRUCTURE SETUP
app = tk.Tk()
app.title("Date Picker")

cal_start = Calendar(app, selectmode="day")
cal_start.grid(row=0, column=0, padx=10, pady=5)

cal_end = Calendar(app, selectmode="day")
cal_end.grid(row=0, column=1, padx=10, pady=5)

# Number input box
num_label = tk.Label(app, text="Other Options")
num_label.grid(row=1, columnspan=2, padx=10, pady=5)

# Number input box
num_label = tk.Label(app, text="Num Plays")
num_label.grid(row=2, column=0, padx=10, pady=5)

num_entry = tk.Entry(app)
num_entry.grid(row=2,column=1, padx=10, pady=5)

# select_button = tk.Button(app, text="Select Dates", command=return )
select_button = tk.Button(app, text="Confirm", command=on_date_select)
# select_button.grid(row=1, columnspan=2, padx=10, pady=5)
select_button.grid(row=3, columnspan=2)

# # Toggle button for showing top artists
# show_artists_var = tk.BooleanVar()
# show_artists_button = tk.Checkbutton(app, text="Show Top Artists", variable=show_artists_var)
# show_artists_button.pack(pady=5)

# # Confirm button
# confirm_button = tk.Button(app, text="Confirm", command=get_user_input)
# confirm_button.pack(pady=10)

# result_label = tk.Label(app, text="", font=("Helvetica", 12))
# result_label.grid(row=2, columnspan=2, padx=10, pady=5)


def get_playlist_info():
    app.mainloop()
    return [start_date, end_date, num_song_plays]

if __name__ == "__main__":
    dates = get_playlist_info()
    print(dates)
