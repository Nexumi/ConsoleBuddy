# ConsoleBuddy

> A better way to use Windows Command Prompt.

## Features
Always displays current directory and all files and folders in that directory

All commands support fuzzy search (You do not have to spell out the full file name)

- cd, start, copy, move, java - (Change) Added fuzzy search support
- del, rm - (Change) Added fuzzy search support and force recursive delete
- unzipper - (New) Unzips every zip file in the current directory
- startwith - (New) Open file with specified program
  - Supports using * to opening multiple files
  - Usage: startwith \<program\> \<file\>
- programs - (New) Lists programs that were found by the script
  - Currently only finds Sublime Text and Notepad++
- ~~generate - (New) Generates rubrics for all students~~
  - ~~Usage: generate \<assignment\>~~
- set - (New) Save the current location needed to be used by other commands
  - Usage: set \<rubrics/top\>
- rubric - (New) Finds and opens rubric from the saved location
  - rubric \<file\>
- pretty - (New) Pretty prints the files of the current directory
  - Only works on correctly named files
- top - (New) Jumps back to the saved location
- download - (New) Opens the download page for ConsoleBuddy
- version - (New) Shows the current version of ConsoleBuddy that you are using and also checks for updates
- ~~setup - (New) Unzips and generates the rubrics for the current submissions~~
  - ~~Usage: setup \<assignment\>~~
- assignment - (New) Opens up the assignment pdf
  - Usage: assignment \<assignment\>
- update - (New) Updates ConsoleBuddy to the latest version
- run - (New) compiles, runs, cleanup
- canvas - (New) Download student assignments

## Support
✔️ Windows

❌ MacOS

❌ Linux

## Direct Run
- Install [Python](https://www.python.org/)
- Open terminal in folder containing the program
- Run `pip install canvasapi` (Only needs to be run once)
- Run `python studentAssignmentDownloader.py`
- Profit

## Self Compilation
- Install [Python](https://www.python.org/)
- Install [PyInstaller](https://pyinstaller.org/en/stable/)
- (Optional) Download [UPX](https://upx.github.io/)
- Run `pyinstaller --onefile ConsoleBuddy.py`
- Grab the file from the `dist` folder
- Discard everything else it creates
