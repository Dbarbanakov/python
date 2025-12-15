from pathlib import Path
from datetime import datetime
import shutil
import sys
import time

# Create a global variable for the main directory.
main_dir = Path.cwd()


def test_dir():
    # Moves files from test directory, if present, to the main directory, deletes it when done.
    test_dir = main_dir / "test"
    if test_dir.exists():
        for file in test_dir.iterdir():
            shutil.move(file, main_dir)
        test_dir.rmdir()


def create_dir(directory):
    # Creates a directory if it doesn't exist.
    if not directory.is_dir():
        directory.mkdir()


def move_to_dir(dir_name, file):
    # Create the directory if it doesn't exist.
    dir = main_dir / f"{dir_name}"
    create_dir(dir)

    # If the file is not in the directory, move it there.
    if not (dir / file.name).exists():
        shutil.move(file, dir)

    # Else rename it by adding an increment in brackets at the end.
    else:
        # The format will look like this - script(i).py
        # Where (i) is the increment, representing the next unique number.
        i = 1
        incremented_file = f"{file.stem}({i}){file.suffix}"
        # While loop that keeps incrementing the number, until the filename is unique.
        while (dir / incremented_file).exists():
            i += 1
            incremented_file = f"{file.stem}({i}){file.suffix}"

        # Reset the increment back to 1 and move the file.
        i = 1
        shutil.move(file, (dir / incremented_file))


def main():
    # Creates the directory where files will be sorted in folders.
    sorted_files_dir = main_dir / "sorted_files"
    create_dir(sorted_files_dir)

    for file in main_dir.iterdir():
        if file.is_file():
            # If the file's name is the same as the script's name or "README.md" skip it.
            if file.name in (sys.argv[0], "README.md"):
                continue

            # Get the file extention of each file.
            file_extention = file.suffix

            # Get the destination's folder name mapped to the file's extention.
            folder_name = files_to_dirs.get(file_extention)
            # If the extention is not present, move it in another folder.
            if not folder_name:
                move_to_dir("not_assigned", file)
                continue

            # Create the full path of the destination folder.
            destination_dir = sorted_files_dir / folder_name

            # Create the directory if it's not present.
            create_dir(destination_dir)

            # Move the file if it's not in the directory.
            if not (destination_dir / file.name).exists():
                shutil.move(file, destination_dir)
            # If it is already there, move it to '/duplicates' directory.
            else:
                move_to_dir("duplicates", file)


if __name__ == "__main__":
    test_dir()

    # A map of file extention to the destination folder.
    files_to_dirs = {
        ".py": "Python",
        ".html": "Web",
        ".jpeg": "Images",
        ".png": "Images",
        ".csv": "Data",
        ".xlsx": "Data",
    }

    while True:
        main()

        now = datetime.now().isoformat(sep="@", timespec="seconds")
        time_sorted = (
            f"Last sort was performed at {now.split('@')[1]} {now.split('@')[0]}."
        )
        print(time_sorted)
        time.sleep(5)
