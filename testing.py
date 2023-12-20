import tkinter as tk
from tkinter import ttk
import pandas as pd

# Assuming you have a DataFrame named df
# Replace this with your actual DataFrame or data source
data = {'id': [1, 2, 1, 3, 2, 1, 3, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Henry', 'Ivy']}
df = pd.DataFrame(data)

input_list = "final_list.xlsx"
df = pd.read_excel(input_list)

def display_dataframe_as_table(dataframe):
    # Create the main window
    window = tk.Tk()
    window.title("DataFrame Table")

    # Create Treeview widget
    tree = ttk.Treeview(window)
    
    # Configure Treeview columns
    tree["columns"] = tuple(dataframe.columns)

    # Add columns to Treeview
    for col in dataframe.columns:
        tree.column(col, anchor="center", width=100)
        tree.heading(col, text=col)

    # Insert data into Treeview
    for index, row in dataframe.iterrows():
        tree.insert("", index, values=tuple(row))

    # Display Treeview
    tree.pack(expand=True, fill="both")

    # Run the Tkinter event loop
    window.mainloop()

# Display the DataFrame as a table
display_dataframe_as_table(df)