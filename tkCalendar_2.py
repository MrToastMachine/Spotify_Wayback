import tkinter as tk
from tkcalendar import Calendar

start_date = ""
end_date = ""

def us_to_uk_date(us_date):
    parts = us_date.split('/')
    uk_date = f"{parts[1]}/{parts[0]}/{parts[2]}"
    return uk_date

def on_date_select():
    selected_date_us = cal.get_date()
    selected_date_uk = us_to_uk_date(selected_date_us)
    result_label.config(text=f"Selected Date (UK format): {selected_date_uk}")

app = tk.Tk()
app.title("Date Picker")

cal = Calendar(app, selectmode="day")
cal.pack(padx=10, pady=10)

select_button = tk.Button(app, text="Select Start Date", command=on_date_select)
select_button.pack(padx=10, pady=5)

result_label = tk.Label(app, text="", font=("Helvetica", 12))
result_label.pack(padx=10, pady=5)

app.mainloop()
