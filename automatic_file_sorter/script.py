import shutil
from pathlib import Path
import sys
import time
from datetime import datetime


def main():
    current_dir = Path.cwd()
    sorted_files_dir = current_dir / "sorted_files"

    if not Path(sorted_files_dir).exists():
        Path.mkdir(sorted_files_dir)

    for file in current_dir.iterdir():
        if Path.is_file(file):
            # Split the full path by '/' and take the last part, which is the name of the file.
            file_name = f"{str(file).split('/')[-1]}"

            # If the name of the file is same as the script, skip it.
            if file_name == sys.argv[0] or file_name == "README.md":
                continue

            # Get the file extention of each file.
            file_extention = file.suffix.strip(".")
            # Get the destination's folder name mapped to the file's extention.
            folder_name = files_to_dirs[file_extention]
            # Create the full path by adding the destination folder to the current directory.
            destination_dir = sorted_files_dir / folder_name

            # Create the directory if it's not present.
            if not Path.is_dir(destination_dir):
                Path.mkdir(destination_dir)

            # Move the file if it's not in the directory.
            if not Path(destination_dir / file_name).exists():
                shutil.move(file, destination_dir)
            # If it is already there, move it to 'duplicates' directory.
            else:
                # Create a 'duplicates' directory if it doesn't exist.
                duplicates_dir = Path(sorted_files_dir / "duplicates")
                if not Path.is_dir(duplicates_dir):
                    Path.mkdir(duplicates_dir)

                # If the file is not in the 'duplicates' directory, move it there.
                if not Path(duplicates_dir / file_name).exists():
                    shutil.move(file, duplicates_dir)

                # Else rename it by adding an increment at the end.
                else:
                    # Split by name and extention.
                    split = file_name.split(".")
                    increment = 1
                    # Add an increment after name, then a '.' dot and finally the extention.
                    # Name format will look like - 'script_1.py'.
                    incremented_file = f"{split[0]}_{increment}.{split[1]}"

                    # While loop that keeps incrementing the number, until the filename is unique.
                    while Path(duplicates_dir / incremented_file).exists():
                        increment += 1
                        incremented_file = f"{split[0]}_{increment}.{split[1]}"

                    # Reset the increment back to 1 and move the file.
                    increment = 1
                    shutil.move(file, Path(duplicates_dir / incremented_file))


if __name__ == "__main__":
    test_dir = Path.cwd() / "test"
    if test_dir.exists():
        for file in test_dir.iterdir():
            shutil.move(file, Path.cwd())
        Path(test_dir).rmdir()

    # A map of file extention to the destination folder.
    files_to_dirs = {
        "py": "Python",
        "html": "Web",
        "jpeg": "Images",
        "png": "Images",
        "csv": "Data",
        "xlsx": "Data",
    }

    while True:
        main()

        now = datetime.now().isoformat(sep="@", timespec="seconds")
        time_sorted = (
            f"Last sort was performed at {now.split('@')[1]} {now.split('@')[0]}."
        )
        print(time_sorted)
        time.sleep(5)
