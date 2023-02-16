# ConsoleBuddy

> A better way to use Windows Command Prompt.

## Features
Always displays current directory and all files and folders in that directory

- cd, del, start, copy, move, java - (Change) Added fuzzy search support
- unzipper - (New) Unzips every zip file in the current directory
- startwith - (New) Open file with specified program \[startwith \<program\> \<file\>\]
- programs - (New) Lists programs that were found by the script (Currently only finds Sublime Text and Notepad++)
- generate - (New) Runs Benjamin’s rubric generator \[generate \<input file\> \<file to copy\>\] (Leave parameters blank if file names are left default and only 1 rubric file is present)
- set - (New) Save the current location needed to be used by other commands [set <rubrics/top>]
- rubric - (New) Finds and opens rubric found from saved location [rubric <name>] (Name is based on file name)
- pretty - (New) Pretty prints the files of the current directory (Only works on correctly named files)
- top - (New) Jumps back to the saved location


## Support
✔️ Windows

❌ MacOS

❌ Linux


## Self Compilation
- Install [Python](https://www.python.org/)
- Install [PyInstaller](https://pyinstaller.org/en/stable/)
- (Optional) [Download UPX](https://upx.github.io/)
- Run `pyinstaller --onefile consoleBuddy.py`
- Grab exe from the "dist" folder
- Discard everything else it creates
