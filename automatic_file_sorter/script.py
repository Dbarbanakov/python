from pathlib import Path
from datetime import datetime
import shutil
import sys
import time


def create_dir(directory):
    # Creates a directory if it doesn't exist.
    if not directory.is_dir():
        directory.mkdir()


def move_to_Duplicates(file, parent_dir):
    # Create a 'duplicates' directory if it doesn't exist.
    duplicates_dir = parent_dir / "duplicates"
    create_dir(duplicates_dir)

    # If the file is not in the 'duplicates' directory, move it there.
    if not (duplicates_dir / file.name).exists():
        shutil.move(file, duplicates_dir)

    # Else rename it by adding an increment at the end.
    else:
        # Split by name and extention.
        split = file.name.split(".")
        i = 1
        # Add an increment after name, then a '.' dot and finally the extention.
        # Name format will look like - 'script_1.py'.
        incremented_file = f"{split[0]}_{i}.{split[1]}"
        # While loop that keeps incrementing the number, until the filename is unique.
        while (duplicates_dir / incremented_file).exists():
            i += 1
            incremented_file = f"{split[0]}_{i}.{split[1]}"

        # Reset the increment back to 1 and move the file.
        i = 1
        shutil.move(file, (duplicates_dir / incremented_file))


def main(current_dir):
    # Creates the directory where files will be sorted in folders.
    sorted_files_dir = current_dir / "sorted_files"
    create_dir(sorted_files_dir)

    for file in current_dir.iterdir():
        if file.is_file():
            # If the file's name is the same as the script's name or "README.md" skip it.
            if file.name in (sys.argv[0], "README.md"):
                continue

            # Get the file extention of each file.
            file_extention = file.suffix
            # Get the destination's folder name mapped to the file's extention.
            folder_name = files_to_dirs.get(file_extention)
            if not folder_name:
                # Creates a directory for files which do not match any of the extentions,
                # matching the sorting criteria.
                missing_dir = sorted_files_dir / "missing"
                create_dir(missing_dir)
                if not (missing_dir / file.name).exists():
                    shutil.move(file, missing_dir)
                else:
                    print("hehe")
                continue
            # Create the full path by adding the destination folder to the current directory.
            destination_dir = sorted_files_dir / folder_name

            # Create the directory if it's not present.
            create_dir(destination_dir)

            # Move the file if it's not in the directory.
            if not (destination_dir / file.name).exists():
                shutil.move(file, destination_dir)
            # If it is already there, move it to '/duplicates' directory.
            else:
                move_to_Duplicates(file, sorted_files_dir)


if __name__ == "__main__":
    current_dir = Path.cwd()

    test_dir = current_dir / "test"
    if test_dir.exists():
        for file in test_dir.iterdir():
            shutil.move(file, current_dir)
        Path(test_dir).rmdir()

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
        main(current_dir)

        now = datetime.now().isoformat(sep="@", timespec="seconds")
        time_sorted = (
            f"Last sort was performed at {now.split('@')[1]} {now.split('@')[0]}."
        )
        print(time_sorted)
        time.sleep(5)
