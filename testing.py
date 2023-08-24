import tkCalendar
import pandas as pd

dates = tkCalendar.launch_date_picker()

print("Start Date: " + dates[0])
print("End Date: " + dates[1])