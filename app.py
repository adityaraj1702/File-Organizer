import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar


# Define file types and their folders
file_types = {
    "docx": "Docs",
    "docs": "Docs",
    "doc": "Docs",
    "pdf": "Docs",
    "pptx": "PPTs",
    "jpeg": "Images",
    "jpg": "Images",
    "png": "Images",
    "mp3": "Audio",
    "mp4": "Video",
    "exe": "Apps",
    "Others": "Others",
}


# Function to check path validity and get specific file extensions
def get_destination_folder(file_path):
    try:
        file_extension = Path(file_path).suffix[1:]  # Extract extension without leading dot
    except Exception as e:
        messagebox.showerror(f"Error extracting extension for file: {e}")
        return None
    if file_extension not in file_types:
        # messagebox.showerror(f"{file_extension} not in file types")
        return Path(os.path.join(download_folder_path, file_types["Others"]))
    return Path(os.path.join(download_folder_path, file_types[file_extension]))

# Function to move file to its category folder
def handle_file(file_path):
    destination_folder = get_destination_folder(file_path)
    if not destination_folder:
        print(f"Skipping unknown file: {file_path.name}")
        return
    try:
        destination_folder.mkdir(parents=True, exist_ok=True)  # Create folder if needed
        shutil.move(file_path, destination_folder / file_path.name)
        print("Success!", f"Moved {file_path.name} to {destination_folder}")
        progress_bar['value'] += 1
        progress_label['text'] = f"Organising files: {progress_bar['value']}/{total_files} ({int(progress_bar['value']/total_files*100)}%) complete"
        root.update_idletasks() # Update UI without blocking execution
        
    except Exception as e:
        messagebox.showerror(
            "Error!", f"Error moving file '{file_path.name}': {e}"
        )

# Function to monitor the download folder
def watch_downloads_folder():
    for file in download_folder_path.glob("*"):
        try:
            if not file.is_dir():
                handle_file(file)
        except Exception as e:
            print(f"Error in file loop: {e}")
    finish_monitoring()

# Function to start/stop monitoring
def start_monitoring():
    global monitoring_running, total_files
    if not monitoring_running:
        progress_bar['value'] = 0
        total_files = len(list(Path(download_folder_path).glob("*.*")))
        progress_label['text'] = f"Organizing files: 0/{total_files} (0%) complete"
        watch_downloads_folder()
        monitoring_running = True
        start_button.config(text="Stop Monitoring", command=stop_monitoring)
    else:
        messagebox.showinfo("Already monitoring", "File organization is already in progress.")

# Function to stop monitoring
def stop_monitoring():
    global monitoring_running
    monitoring_running = False
    progress_bar['value'] = 0
    progress_label['text'] = "Monitoring stopped"
    start_button.config(text="Start Monitoring", command=start_monitoring)

def finish_monitoring():
    global monitoring_running
    monitoring_running = False
    start_button.config(text="Start Monitoring", command=start_monitoring)
    root.update_idletasks()

# Function to choose download folder
def choose_folder():
    global download_folder_path, total_files
    download_folder_path = Path(filedialog.askdirectory(title="Select Download Folder"))

    if str(download_folder_path)!=".":
        messagebox.showinfo("Folder Selection", f"Downloads will be organized in '{download_folder_path}'.")
        total_files = len(list(Path(download_folder_path).glob("*.*")))
        progress_label['text'] = f"Total files found: {total_files}"
        enable_start_button()
        
    else:
        messagebox.showinfo("Folder Selection", "No folder selected.")
        return

def enable_start_button():
    global start_button
    start_button.config(state=tk.NORMAL)

# Main application logic
if __name__ == "__main__":
    # Set initial monitoring state
    monitoring_running = False

    # Create main window
    root = tk.Tk()
    root.title("File Organizer")

    # Instructions label
    instructions_label = tk.Label(
        root, text="Choose your downloads folder and start organizing files!", font=("Arial", 12)
    )
    instructions_label.pack(pady=10)

    # Button to choose download folder
    choose_folder_button = tk.Button(root, text="Choose Download Folder", command=choose_folder)
    choose_folder_button.pack(pady=5)

    
    # Start monitoring button
    start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring, state=tk.DISABLED)
    start_button.pack(pady=5)

    #ProgressBar
    total_files = 0
    progress_bar = Progressbar(root,max = total_files)
    progress_bar.pack(fill="both",expand=True)

    progress_label = tk.Label(root,text ="Organising files: 0/0 (0%) complete")
    progress_label.pack()

    # Quit button
    quit_button = tk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(pady=5)

    # Enter main event loop
    root.mainloop()