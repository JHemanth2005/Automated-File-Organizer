import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

FILE_CATEGORIES = {
    "Pictures": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".css"],
    "Database": [".sql", ".db"],
    "Compressed": [".zip", ".rar", ".7z"],
    "Apps": [".exe", ".msi"]
}


def categorize_file(filename):
    _, extension = os.path.splitext(filename)

    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category

    return "Other"


def create_folders(target_directory):
    for category in FILE_CATEGORIES.keys():
        os.makedirs(
            os.path.join(target_directory, category),
            exist_ok=True
        )

    os.makedirs(
        os.path.join(target_directory, "Other"),
        exist_ok=True
    )


def organize_files():

    source_directory = source_entry.get()
    target_directory = target_entry.get()

    if not os.path.exists(source_directory):
        messagebox.showerror(
            "Error",
            "Invalid Source Folder!"
        )
        return

    create_folders(target_directory)

    total_files = 0

    for root, _, files in os.walk(source_directory):

        for filename in files:

            filepath = os.path.join(root, filename)

            category = categorize_file(filename)

            target_folder = os.path.join(
                target_directory,
                category
            )

            try:

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d_%H-%M-%S"
                )

                new_filename = (
                    f"{timestamp}_{filename}"
                )

                destination = os.path.join(
                    target_folder,
                    new_filename
                )

                shutil.copy2(
                    filepath,
                    destination
                )

                total_files += 1

            except Exception as e:
                print(e)

    messagebox.showinfo(
        "Success",
        f"{total_files} files organized successfully!"
    )


def browse_source():
    folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder)


def browse_target():
    folder = filedialog.askdirectory()
    target_entry.delete(0, tk.END)
    target_entry.insert(0, folder)


# GUI Window
root = tk.Tk()

root.title("Automated File Organizer")
root.geometry("600x250")

tk.Label(
    root,
    text="Source Folder"
).pack(pady=5)

source_entry = tk.Entry(
    root,
    width=60
)
source_entry.pack()

tk.Button(
    root,
    text="Browse Source",
    command=browse_source
).pack(pady=5)

tk.Label(
    root,
    text="Destination Folder"
).pack(pady=5)

target_entry = tk.Entry(
    root,
    width=60
)
target_entry.pack()

tk.Button(
    root,
    text="Browse Destination",
    command=browse_target
).pack(pady=5)

tk.Button(
    root,
    text="Organize Files",
    command=organize_files
).pack(pady=20)

root.mainloop()
