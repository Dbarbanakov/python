## Automatic Files Sorter

### The script works in the following way:
###### - When ran from a folder containing different files,
###### - it will create a subfolder '/sorted_files',
###### - move all the files into subfolders within the '/sorted_files' folder,
###### - sorting them by extentions - eg. '.jpeg', '.png' will go to '/sorted_files/Images', '.csv', '.xlsx' will go to '/sorted_files/Data'.
###### The dictionary files_to_dirs represents key(file extention): value(destination folder) pairs.
###### Files that already exist in the destination folder will be moved to '/sorted_files/duplicates'.
###### 'script.py' will not move.
### ---
###### Script will run until stopped manually, default setting is set to every 5 seconds
###### for easier testing purposes.
###### To change it, replace 'time.sleep(5)' with the desired behaviour,
###### where 5 represents the interval in seconds in which the script runs itself.
###### 1800 would be every 30 minutes and 3600 each hour.