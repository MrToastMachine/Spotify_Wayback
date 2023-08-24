import pandas as pd

songs = pd.read_json('filtered_output.json')
songs.to_excel('filtered_songs.xlsx')