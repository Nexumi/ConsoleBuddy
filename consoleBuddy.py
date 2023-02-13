import os
import shutil
import subprocess
from zipfile import ZipFile

def find(directory, folder, program):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.lower() == folder.lower():
                if program in os.listdir(directory + "/" + file):
                    return directory + "/" + file + "/" + program

def locate(folder, program):
    drives = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in drives:
        directory = letter + ":/Program Files"
        found = find(directory, folder, program)
        if found:
            return found
        directory += " (x86)"
        found = find(directory, folder, program)
        if found:
            return found

def header(line = ""):
    os.system("cls")
    print(("\033[4mCurrent Directory: " + os.getcwd().split("\\")[-1] + "\033[0m").center(os.get_terminal_size().columns))
    print("    ".join(os.listdir()) + line)

def fuzzy(path):
    dirs = []
    listdir = os.listdir()
    for idir in listdir:
        if idir.lower() == path.lower():
            return idir

        if idir.lower().find(path.lower()) != -1:
            dirs.append(idir)

    ld = len(dirs)
    if ld == 0:
        return path
    elif ld == 1:
        return dirs[0]
    else:
        for i in range(ld):
            print(str(i + 1) + ") " + dirs[i])
        print()

        try:
            opt = int(input("Option> ")) - 1
            return dirs[opt]
        except:
            header("\n")
            return path

def command(cmd):
    try:
        cmd = cmd.split(" ", 1)
        cmd[0] = cmd[0].lower()
        if cmd[0] == "cd":
            if len(cmd) == 1:
                os.system(cmd[0])
                return

            os.chdir(fuzzy(cmd[1]))
            header()
        elif cmd[0] == "del":
            path = fuzzy(cmd[1])
            if path == ".":
                header("\n")
                print("WARNING: del . is disabled as it deletes everything in the current directory.")
                print("If you want to delete everything, delete the folder: cd .. > del folder_name")
                return
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            header()
        elif cmd[0] == "copy":
            if len(cmd) == 1:
                os.system(cmd[0])
                return
            parm = cmd[1].split(" ")
            shutil.copy2(parm[0], parm[1])
            header()
        elif cmd[0] == "start":
            if len(cmd) == 1:
                os.system(cmd[0])
                return
            os.startfile(fuzzy(cmd[1]))
            header()
        elif cmd[0] == "startwith":
            program = cmd[1].split()
            if program[0].lower() == "notepad++":
                subprocess.Popen([notepad_plus_plus, fuzzy(" ".join(program[1:]))])
            elif program[0].lower() == "sublime":
                subprocess.Popen([sublime_text, fuzzy(" ".join(program[1:]))])
            elif " ".join(program[:2]).lower() == "sublime text":
                subprocess.Popen([sublime_text, fuzzy(" ".join(program[2:]))])
        elif cmd[0] == "eval":
            eval(cmd[1])
        elif cmd[0] == "programs":
            print(notepad_plus_plus)
            print(sublime_text)
        elif cmd[0] == "unzipper":
            zips = os.listdir()
            i = 0
            while i < len(zips):
                if zips[i][-4:].lower() != ".zip":
                    zips.pop(i)
                else:
                    i += 1
                    
            for izip in zips:
                os.mkdir(izip[:-4])
                with ZipFile(izip, 'r') as zipObj:
                    zipObj.extractall(path=izip[:-4])
                os.remove(izip)
            
            header()
        else:
            os.system(" ".join(cmd))
    except Exception as e:
        print(e)

cmd = ""
notepad_plus_plus = locate("Notepad++", "notepad++.exe")
sublime_text = locate("Sublime Text", "sublime_text.exe")

header("\n")
while cmd.lower() != "exit":
    if cmd != "":
        print()
    cmd = " ".join(input("Console> ").split())
    header("\n")
    command(cmd)

os.system("cls")