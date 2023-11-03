from tkinter import *
from tkinter import filedialog
from zipfile import ZipFile 

root = Tk()
root.title("Load file from given location")

# NOTE: The initialdir will probably need to be changed for windows
#       because path has lower case "users/.../..."

# Returns full path of file selected as string
filename = filedialog.askopenfilename(initialdir="Users/%USERPROFILE%/Downloads")

# my_label = Label(root, text=filename).pack()



# loading the temp.zip and creating a zip object 
with ZipFile(filename, 'r') as zipSongs: 

	# Extracting all the members of the zip 
	# into a specific location. 
    zipSongs.extractall(path=".") 
    print("Unzip please")


root.mainloop()
root.quit()

