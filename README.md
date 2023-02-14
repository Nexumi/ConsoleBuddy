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
programs - (New) Lists all programs that the program found install on the computer (Currently only finds Sublime Text and Notepad++)
<br>
generate - (New) Runs Benjamin’s rubric generator \[generate \<input file\> \<file to copy\>\] (Leave parameters blank if file names are left default and only 1 rubric file is present)
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
  <li>(Optional) Install UPX [https://upx.github.io/]</li>
  <li>Run "pyinstaller --onefile consoleBuddy.py"</li>
  <li>Grab exe from the "dist" folder</li>
  <li>Discard everything else it creates</li>
</ul>
