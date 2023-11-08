import json
import pandas as pd

input_file = "Full_Streaming_History.json"

pd_dataframe = pd.read_json(input_file)

pd_dataframe.to_excel('Full_History.xlsx')

print("Done")