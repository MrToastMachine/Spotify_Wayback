import os
from tkinter import *
from tkinter import filedialog
from zipfile import ZipFile 
from combine_json import *

# root = Tk()
# root.title("Load file from given location")

# NOTE: The initialdir will probably need to be changed for windows
#       because path has lower case "users/.../..."

# Returns full path of file selected as string

def unzip_spotify_data(output_filename):
    filename = filedialog.askopenfilename(initialdir="Users/%USERPROFILE%/Downloads")
    # loading the temp.zip and creating a zip object 
    with ZipFile(filename, 'r') as zipSongs:
        # Extracting all of the zip files into a specific location.
        zipSongs.extractall(path=".") 
        print("Unzip please")
    
    if os.path.exists("MyData"):
        print("Unzip Successfull!")
        combine_json_files("MyData", output_filename)

if __name__=="__main__":
    # root.mainloop()
    unzip_spotify_data("Full_Streaming_History.json")
    # root.quit()


