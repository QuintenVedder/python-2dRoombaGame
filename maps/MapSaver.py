import os
from tkinter import Tk, filedialog

def save_map(map_content):

    root = Tk()
    root.title("MapSaver")
    root.withdraw()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Open file dialog for saving, set initial directory
    file_path = filedialog.asksaveasfilename(
        initialdir=current_dir,
        defaultextension=".npy",
        filetypes=[("gamemaps", "*.npy")],
        title="MapSaver"
    )

    # Save map file
    if file_path:
        with open(file_path, "w") as file:
            file.write(map_content)
            print("File saved successfully!")
    else:
        print("File save canceled.")