from pathlib import Path
from datetime import datetime
import shutil
import sys
import time
import json

# Create a global variable for the main directory.
main_dir = Path.cwd()


def get_dir(folder_name, parent_dir=main_dir):
    # Creates a directory if it doesn't exist.Returns full path.
    dir = parent_dir / folder_name
    if not dir.is_dir():
        dir.mkdir()
    return dir


def move_to_dir(dir_name, file):
    # Create the directory if it doesn't exist.
    dir = get_dir(dir_name)

    # If the file is not in the directory, move it there.
    if not (dir / file.name).exists():
        shutil.move(file, dir)
    # Else rename it by adding an increment in brackets at the end.
    else:
        renamed_file = rename_file(file, dir)
        shutil.move(file, (dir / renamed_file))


def rename_file(file, parent_dir):
    # The format will look like this - script(i).py
    # Where (i) is the increment, representing the next unique number.
    i = 1
    incremented_file = file.stem + "(" + str(i) + ")" + file.suffix

    while (parent_dir / incremented_file).exists():
        i += 1
        incremented_file = file.stem + "(" + str(i) + ")" + file.suffix

    return incremented_file


def handle_test_dir():
    # Moves files from test directory, if present, to the main directory, deletes it when done.
    test_dir = main_dir / "test"
    if test_dir.exists():
        for file in test_dir.iterdir():
            shutil.move(file, main_dir)
        test_dir.rmdir()


def get_map():
    # Load the data from a JSON file.
    with open("extention_to_dir_map.json", "r") as f:
        return json.load(f)


def main(map):
    # Creates the directory where files will be sorted in folders.
    sorted_files_dir = get_dir("sorted_files")

    for file in main_dir.iterdir():
        if file.is_file():
            if file.name in (sys.argv[0], "README.md", "extention_to_dir_map.json"):
                continue

            # Get the file extention of each file.
            file_extention = file.suffix

            # Get the destination's folder name mapped to the file's extention.
            folder_name = map.get(file_extention)
            # If the extention is not present, move it in another folder.
            if not folder_name:
                move_to_dir("not_assigned", file)
                continue

            destination_dir = get_dir(folder_name, sorted_files_dir)

            # Move the file if it's not in the directory.
            if not (destination_dir / file.name).exists():
                shutil.move(file, destination_dir)
            # If it is already there, move it to '/duplicates' directory.
            else:
                move_to_dir("duplicates", file)


if __name__ == "__main__":
    handle_test_dir()
    map = get_map()

    while True:
        main(map)

        now = datetime.now().isoformat(sep="@", timespec="seconds")
        time_sorted = (
            f"Last sort was performed at {now.split('@')[1]} {now.split('@')[0]}."
        )
        print(time_sorted)
        time.sleep(5)
