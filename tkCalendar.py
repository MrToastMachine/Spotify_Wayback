# This App creates a tk window to allow selection of two dates
# From this we can select songs listened to within the date range

import tkinter as tk
from tkcalendar import Calendar

start_date = ""
end_date = ""

def us_to_uk_date(us_date):
    parts = us_date.split('/')
    uk_date = f"{parts[1]}/{parts[0]}/20{parts[2]}"
    return uk_date

def on_date_select():
    global start_date
    global end_date
    start_date_us = cal_start.get_date()
    end_date_us = cal_end.get_date()
    start_date = us_to_uk_date(start_date_us)
    end_date = us_to_uk_date(end_date_us)
    # result_label.config(text=f"Start Date (UK format): {start_date_uk}\nEnd Date (UK format): {end_date_uk}")

    app.quit()
    

#APP STRUCTURE SETUP
app = tk.Tk()
app.title("Date Picker")

cal_start = Calendar(app, selectmode="day")
cal_start.grid(row=0, column=0, padx=10, pady=5)

cal_end = Calendar(app, selectmode="day")
cal_end.grid(row=0, column=1, padx=10, pady=5)

# select_button = tk.Button(app, text="Select Dates", command=return )
select_button = tk.Button(app, text="Select Dates", command=on_date_select)
select_button.grid(row=1, columnspan=2, padx=10, pady=5)

# result_label = tk.Label(app, text="", font=("Helvetica", 12))
# result_label.grid(row=2, columnspan=2, padx=10, pady=5)


def launch_date_picker():
    app.mainloop()
    return [start_date, end_date]

if __name__ == "__main__":
    dates = launch_date_picker()
