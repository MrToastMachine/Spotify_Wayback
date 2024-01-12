"""
selection = combo.get()
messagebox.showinfo(
    title="New Selection",
    message=f"Selected option: {selection}"
)

"""
import pandas as pd
from pandas_json import *
import time
from datetime import datetime

input_file = "Full_Streaming_History.json"

def get_available_data_range(dataset):
    earliest_date_ts = dataset.iloc[0].get("ts")
    if earliest_date_ts:

        iso_datetime = datetime.strptime(earliest_date_ts.split("T")[0], "%Y-%m-%d")
        earliest_date = iso_datetime.strftime("%d %B %Y")
    
        latest_date_ts = dataset.iloc[-1].get("ts")
        if latest_date_ts:

            iso_datetime = datetime.strptime(latest_date_ts.split("T")[0], "%Y-%m-%d")
            latest_date = iso_datetime.strftime("%d %B %Y")
            return (earliest_date, latest_date)

    

    
    

with open(input_file, "r", encoding="utf8") as file:
    # json_data = json.load(file)
    json_data = pd.read_json(input_file)

get_available_data_range(json_data)

