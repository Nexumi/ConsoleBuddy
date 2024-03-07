from time import sleep
from sys import argv, platform
from urllib.request import urlretrieve
from os import startfile, system, listdir, remove

def launch(filename):
    if platform.startswith("win32"):
        startfile(filename)
    else:
        system("x-terminal-emulator -e ./" + filename)

sleep(1)
dirs = listdir()
if platform.startswith("win32"):
	filename = "ConsoleBuddy.exe"
	if len(argv) > 1:
		filename = argv[1]
	if filename in dirs:
		remove(filename)
	urlretrieve("https://github.com/Nexumi/ConsoleBuddy/releases/latest/download/ConsoleBuddy.exe", filename)
	launch(filename)
elif platform.startswith("linux"):
	filename = "ConsoleBuddyLinux"
	if len(argv) > 1:
		filename = argv[1]
	if filename in dirs:
		remove(filename)
	urlretrieve("https://github.com/Nexumi/ConsoleBuddy/releases/latest/download/ConsoleBuddyLinux", filename)
	system("chmod +x " + filename)
	launch(filename)