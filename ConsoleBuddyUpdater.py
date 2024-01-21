import os
from time import sleep
from urllib.request import urlretrieve

def launch(filename):
    if os.name == "nt":
        os.startfile(filename)
    else:
        os.system("x-terminal-emulator -e ./" + filename)

sleep(1)
dirs = os.listdir()
if os.name == "nt":
	if "ConsoleBuddy.exe" in dirs:
		os.remove("ConsoleBuddy.exe")
	urlretrieve("https://github.com/Nexumi/ConsoleBuddy/releases/latest/download/ConsoleBuddy.exe", "ConsoleBuddy.exe")
	launch("ConsoleBuddy.exe")
else:
	if "ConsoleBuddy" in dirs:
		os.remove("ConsoleBuddy")
	urlretrieve("https://github.com/Nexumi/ConsoleBuddy/releases/latest/download/ConsoleBuddy", "ConsoleBuddy")
	os.system("chmod +x ConsoleBuddy")
	launch("ConsoleBuddy")
