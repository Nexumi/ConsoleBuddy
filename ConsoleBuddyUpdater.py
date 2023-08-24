import os
from time import sleep
from urllib.request import urlretrieve

sleep(1)
if "ConsoleBuddy.exe" in os.listdir():
	os.remove("ConsoleBuddy.exe")
urlretrieve("https://github.com/Nexumi/ConsoleBuddy/releases/latest/download/ConsoleBuddy.exe", "ConsoleBuddy.exe")
os.startfile("ConsoleBuddy.exe")