# ConsoleBuddy

> A better way to use Windows Command Prompt.

## Features
Always displays current directory and all files and folders in that directory

cd, del, start, copy, move - (Change) Added fuzzy search support

unzipper - (New) Unzips every zip file in the current directory

startwith - (New) Open file with specified program \[startwith \<program\> \<file\>\]

locations - (New) Lists all locations that are saved by the script (Currently only finds Sublime Text and Notepad++)

generate - (New) Runs Benjamin’s rubric generator \[generate \<input file\> \<file to copy\>\] (Leave parameters blank if file names are left default and only 1 rubric file is present)

set - (New) Save the current location as a location needed to be used by other commands \[set rubrics\] (Only supports setting the location of rubrics)

rubric - (New) Using the saved location, opens the rubric of the student you request to open \[rubric \<name\>\] (Name is based on file name)

pretty - (New) Pretty prints the files of the current directory (Only works on correctly named files)


## Support
✔️ Windows

❌ MacOS

❌ Linux


## Self Compilation
- Install Python [https://www.python.org/]
- Install PyInstaller [https://pyinstaller.org/en/stable/]
- (Optional) Download UPX [https://upx.github.io/]
- Run `pyinstaller --onefile consoleBuddy.py`
- Grab exe from the "dist" folder
- Discard everything else it creates
