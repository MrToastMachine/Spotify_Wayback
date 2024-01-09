"""
selection = combo.get()
messagebox.showinfo(
    title="New Selection",
    message=f"Selected option: {selection}"
)

"""
import pandas as pd
from pandas_json import *

input_file = "Full_Streaming_History.json"
"""
with open(input_file, "r", encoding="utf8") as file:
    # json_data = json.load(file)
    json_data = pd.read_json(input_file)

top_ten_artists = get_top_artists(json_data, 10)
print("Top Artists")
print(top_ten_artists['master_metadata_album_artist_name'])

print("Done")
"""


x = 5

print(x)
def goop():
    x = 6
    print("changed x")

print(x)

