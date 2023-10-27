import pandas as pd

# Replace 'your_file.xlsx' with the actual path to your Excel file
file_path = 'single_duplicates_only.xlsx'

# Read the Excel file
df = pd.read_excel(file_path)

# Extract the "uri" column as a Python array
uri_array = df['spotify_track_uri'].tolist()

# Print or use the uri_array as needed
print(uri_array)
