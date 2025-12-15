## Automatic Files Sorter

### The script works in the following way:
###### - When ran from a folder containing different files
###### - Creates a subfolder '/sorted_files'
###### - Moves all the files into subfolders within the '/sorted_files' folder
###### - Sorting them by extentions - eg. '.jpeg', '.png' will go to '/sorted_files/Images', '.csv', '.xlsx' will go to '/sorted_files/Data'
###### The dictionary 'files_to_dirs' represents key(file extention): value(destination folder) pairs
###### Files that already exist in the destination folder will be moved to '/sorted_files/duplicates'
###### 'script.py' will not move
### ---
###### Script will run until stopped manually, default setting is set to every 5 seconds for easier testing purposes.
###### To change it, replace 'time.sleep(5)' with the desired behaviour,
###### where 5 represents the interval in seconds in which the script runs itself.
###### 1800 would be every 30 minutes and 3600 each hour.
###### ---
###### The test folder is included for testing purposes.
###### It contains files with different extentions and gets deleted after moving the files to the main directory.