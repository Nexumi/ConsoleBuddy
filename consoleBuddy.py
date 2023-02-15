import os
import shutil
import subprocess
from zipfile import ZipFile

def find(directory, folder, program):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.lower() == folder.lower():
                if program in os.listdir(directory + "\\" + file):
                    return directory + "\\" + file + "\\" + program

def locate(folder, program):
    drives = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for letter in drives:
        directory = letter + ":\\Program Files"
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

def display(name):
    for letter in name:
        char = ord(letter)
        if char >= 65 and char <= 90:
            print(" " + letter, end = "")
        else:
            print(letter, end = "")
    print()

def grader(done):
    os.system("cls")
    print(("\033[4m" + os.getcwd() + "\033[0m"))
    for idir in os.listdir():
        xdir = idir.split("_")
        if xdir not in done and len(xdir) == 4:
            name = xdir[3].split("-")[0]
            display(name)

def fuzzy(file, path = "."):
    dirs = []
    listdir = os.listdir(path)
    for idir in listdir:
        if idir.lower() == file.lower():
            return idir

        if idir.lower().find(file.lower()) != -1:
            dirs.append(idir)

    ld = len(dirs)
    if ld == 0:
        return file
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
            return file

def getRubric():
    listdir = os.listdir()
    results = []
    for idir in listdir:
        found = idir.find("-Rubric.xlsx")
        if found != -1:
            results.append(idir[11:found])
            results.append(idir)
            return results

def command(cmd):
    global rubrics
    try:
        cmd = cmd.split(" ", 1)
        cmd[0] = cmd[0].lower()
        if cmd[0] == "help":
            pass
        elif cmd[0] == "cd":
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
        elif cmd[0] == "start":
            if len(cmd) == 1:
                os.system(cmd[0])
                return
            os.startfile(fuzzy(cmd[1]))
            header()
        elif cmd[0] == "copy":
            if len(cmd) == 1:
                os.system(cmd[0])
                return
            parm = cmd[1].split(" ")
            shutil.copy2(fuzzy(parm[0]), fuzzy(parm[1]))
            header()
        elif cmd[0] == "move":
            if len(cmd) == 1:
                os.system(cmd[0])
                return
            parm = cmd[1].split(" ")
            os.system(cmd[0] + " \"" + fuzzy(parm[0]) + "\" \"" + fuzzy(parm[1] + "\""))
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
        elif cmd[0] == "locations":
            if notepad_plus_plus:
                print(notepad_plus_plus)
            if sublime_text:
                print(sublime_text)
            if rubrics:
                print(rubrics)
        elif cmd[0] == "generate":
            if len(cmd) == 1:
                result = getRubric()
                os.system("generateStudentRubrics.exe --assignment=\"" + result[0] + "\" --inputFile=studentNames.txt --fileToCopy=" + result[1])
                return
            files = cmd[1].split()
            os.system("generateStudentRubrics.exe --assignment=\"" + files[1][11:files[1].find("-Rubric.xlsx")] + "\" --inputFile=" + files[0] + " --fileToCopy=" + files[1])
        elif cmd[0] == "set":
            if cmd[1].lower() == "rubrics":
                rubrics = os.getcwd()
                print("rubics = " + rubrics)
        elif cmd[0] == "rubric":
            if len(cmd) != 1 and rubrics:
                os.startfile(rubrics + "\\" + fuzzy(cmd[1], rubrics))
                header()
        elif cmd[0] == "pretty":
            os.system("cls")
            print(("\033[4mCurrent Directory: " + os.getcwd().split("\\")[-1] + "\033[0m").center(os.get_terminal_size().columns))
            for idir in os.listdir():
                xdir = idir.split("_")
                if len(xdir) == 4:
                    name = xdir[3].split("-")[0]
                    display(name)
                elif len(xdir) == 5:
                    name = xdir[4].split("-")[0]
                    display(name)
                else:
                    print(" * " + idir)
        else:
            os.system(" ".join(cmd))
    except Exception as e:
        print(e)

cmd = ""
notepad_plus_plus = locate("Notepad++", "notepad++.exe")
sublime_text = locate("Sublime Text", "sublime_text.exe")
rubrics = None

header("\n")
while cmd.lower().strip() != "exit":
    if cmd.strip() != "":
        print()
    cmd = " ".join(input("Console> ").split())
    header("\n")
    command(cmd)

os.system("cls")