# ConsoleBuddy
About:
A better way to use Windows Command Prompt.
<br><br>
Features:
<br>
Always displays current directory and all files and folders in that directory
<br>
cd, del, start, copy, move - (Change) Added fuzzy search support
<br>
unzipper - (New) Unzips every zip file in the current directory
<br>
startwith - (New) Open file with specified program \[startwith \<program\> \<file\>\]
<br>
locations - (New) Lists all locations that are saved by the script (Currently only finds Sublime Text and Notepad++)
<br>
generate - (New) Runs Benjamin’s rubric generator \[generate \<input file\> \<file to copy\>\] (Leave parameters blank if file names are left default and only 1 rubric file is present)
<br>
set - (New) Save the current location as a location needed to be used by other commands [set rubrics] (Only supports setting the location of rubrics)
<br>
rubric - (New) Using the saved location, opens the rubric of the student you request to open [rubric <name>] (Name is based on file name)
<br>
pretty - (New) Pretty prints the files of the current directory (Only works on correctly named files)
<br><br>
Support:
<br>
✔️ Windows
<br>
❌ MacOS
<br>
❌ Linux
<br><br>
# Self Compilation
<ul>
  <li>Install Python [https://www.python.org/]</li>
  <li>Install PyInstaller [https://pyinstaller.org/en/stable/]</li>
  <li>(Optional) Download UPX [https://upx.github.io/]</li>
  <li>Run `pyinstaller --onefile consoleBuddy.py`</li>
  <li>Grab exe from the "dist" folder</li>
  <li>Discard everything else it creates</li>
</ul>
