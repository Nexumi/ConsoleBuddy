v = "v0.5.0"

import os
import ssl
from sys import argv
from time import sleep
from zipfile import ZipFile
from subprocess import Popen
from shutil import copy2, rmtree
from webbrowser import open as web
from urllib.request import urlopen, urlretrieve

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def reload():
    global cmd
    os.startfile(__file__)
    cmd = "exit"

def update():
    def dev(local, remote):
        local = local.split(".")
        remote = remote.split(".")
        if int(local[0][1:]) < int(remote[0][1:]):
            return True
        elif int(local[0][1:]) > int(remote[0][1:]):
            return False
        elif int(local[1]) < int(remote[1]):
            return True
        elif int(local[1]) > int(remote[1]):
            return False
        else:
            try:
                if int(local[2][:len(remote[2])]) < int(remote[2]):
                    return True
            except:
                pass
        return False

    global cmd
    url = "https://raw.githubusercontent.com/Nexumi/ConsoleBuddy/main/ConsoleBuddy.py"
    data = urlopen(url)
    for line in data:
        r = str(line)[7:-6]
        data.close()
    if dev(v, r):
        output.append("[\033[34mnotice\033[0m] A new release of ConsoleBuddy is available: \033[31m" + v + "\033[0m -> \033[32m" + r + "\033[0m")
        output.append("[\033[34mnotice\033[0m] To update, run: \033[32mupdate\033[0m")
        cmd = "update"

def updating():
    global cmd
    os.chdir(os.path.sep.join(argv[0].split(os.path.sep)[:-1]))
    urlretrieve("https://raw.githubusercontent.com/Nexumi/ConsoleBuddy/main/ConsoleBuddyUpdater.exe", "ConsoleBuddyUpdater.exe")
    os.startfile("ConsoleBuddyUpdater.exe")
    cmd = "exit"

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

def header():
    global skip
    if skip:
        skip = False
        return
    global output
    clear()
    print(("\033[4mCurrent Directory: " + os.getcwd().split("\\")[-1] + "\033[0m").center(os.get_terminal_size().columns))
    print("  |  ".join(os.listdir()) + "\n")
    if cmd.strip() != "" and output:
        for i in range(len(output)):
            if type(output[i]) == type(b""):
                output[i] = output[i].decode("utf-8")
            else:
                output[i] = str(output[i])
        if len(output) != 0:
            print("\n".join(output) + "\n")
    output.clear()

def build(name):
    n = ""
    for letter in name:
        char = ord(letter)
        if char >= 65 and char <= 90:
            n += " " + letter
        else:
            n += letter
    output.append(n)

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
            output.append(str(i + 1) + ") " + dirs[i])
        header()
        try:
            opt = int(input("Option> ")) - 1
            return dirs[opt]
        except:
            return file

def unzipper():
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

def namelist(person):
    # http://gradersections.ducta.net/
    data = urlopen("https://docs.google.com/spreadsheets/d/17PrxZS_BnBqAsFfVVP6oL08TvymFIFqbIXijq63r9LI/gviz/tq?tqx=out:csv&sheet=Student-Grader-GraderSection")
    students = []
    for info in data:
        info = info.decode("utf-8").replace("\n", "").split(",")
        if info[0].find("Grader SECTION") == 1 and len(info[0]) == 19:
            grader = info[1].replace("\"", "")
            if grader.lower().find(person.lower()) == -1:
                continue
            info[4] = [i.capitalize() for i in info[4].replace("\"", "").replace("-", "").split()]
            info[5] = [i.capitalize() for i in info[5].replace("\"", "").replace("-", "").split()]
            student = "".join(info[5]) + "".join(info[4])
            if student:
                students.append(student)
    data.close()
    return students

def generate(cmd):
    global rubrics
    rubric = "Assignment-" + cmd[0] + "-Rubric.xlsx"
    folder = rubric[:-5] + "s"
    names = namelist(cmd[1])
    try:
        data = urlopen("https://web.jpkit.us/grader-rubrics/" + rubric)
    except:
        missing = "rubric"
        if not names:
            missing += " and grader"
        output.append("404 " + missing + " not found")
        return False
    data.close()
    if not names:
        output.append("404 grader not found")
        return False
    os.mkdir(folder)
    os.chdir(folder)
    urlretrieve("https://web.jpkit.us/grader-rubrics/" + rubric, rubric)
    for name in names:
        copy2(rubric, name + "-" + rubric)
    os.remove(rubric)
    rubrics = os.getcwd()
    os.chdir("..")
    return True

def native(cmd):
    global skip
    header()
    os.system(cmd)
    if cmd.strip() != "":
        print()
    skip = True

def opener(program, file, path = "."):
    file = file.split("*")
    listdir = os.listdir(path)
    for idir in listdir:
        marker = 0
        finds = 0
        for part in file:
            mark = idir.find(part, marker)
            if mark != -1:
                marker = mark + len(part)
                finds += 1
            else:
                break
        if finds == len(file):
            Popen([programs.get(program), idir])
            output.append("Opening " + idir)


def command(cmd):
    global output
    global rubrics
    global top
    try:
        cmd = cmd.split(" ", 1)
        cmd[0] = cmd[0].lower()
        if cmd[0] == "cd":
            if len(cmd) == 1:
                native(cmd[0])
                return
            os.chdir(fuzzy(cmd[1]))
        elif cmd[0] == "del":
            if len(cmd) == 1:
                native(cmd[0])
                return
            path = fuzzy(cmd[1])
            if path == ".":
                header("\n")
                output.append("WARNING: del . is disabled as it deletes everything in the current directory.")
                output.append("If you want to delete everything, delete the folder: cd .. > del folder_name")
                return
            if os.path.isfile(path):
                os.remove(path)
            else:
                rmtree(path)
        elif cmd[0] == "start":
            if len(cmd) == 1:
                native(cmd[0])
                return
            os.startfile(fuzzy(cmd[1]))
        elif cmd[0] == "copy":
            if len(cmd) == 1:
                native(cmd[0])
                return
            parm = cmd[1].split(" ")
            copy2(fuzzy(parm[0]), fuzzy(parm[1]))
        elif cmd[0] == "move":
            if len(cmd) == 1:
                native(cmd[0])
                return
            parm = cmd[1].split(" ")
            native(cmd[0] + " \"" + fuzzy(parm[0]) + "\" \"" + fuzzy(parm[1] + "\""))
        elif cmd[0] == "java":
            if len(cmd) == 1:
                native(cmd[0])
                return
            native("java " + fuzzy(cmd[1]).replace(".class", ""))
        elif cmd[0] == "javam":
            if len(cmd) == 1:
                native("javac")
                return
            native("javac -encoding ISO-8859-1 " + cmd[1])
        elif cmd[0] == "unzipper":
            unzipper()
        elif cmd[0] == "startwith":
            def openPath(program, file):
                if file.find("*") != -1:
                    opener(program, file)
                else:
                    file = fuzzy(file)
                    Popen([programs.get(program), file])
                    output.append("Opening " + file)

            program = cmd[1].split()
            if programs.get("Notepad++") and program[0].lower() == "notepad++":
                file = " ".join(program[1:])
                program = "Notepad++"
                openPath(program, file)
            elif programs.get("Sublime Text") and " ".join(program[:2]).lower() == "sublime text":
                file = " ".join(program[2:])
                program = "Sublime Text"
                openPath(program, file)
            elif programs.get("Sublime Text") and program[0].lower() == "sublime":
                file = " ".join(program[1:])
                program = "Sublime Text"
                openPath(program, file)
            else:
                output.append("Program not found or unsupported")
        elif cmd[0] == "eval":
            eval(cmd[1])
        elif cmd[0] == "programs":
            for program in programs.values():
                output.append(program)
        elif cmd[0] == "generate":
            if len(cmd) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            cmd[1] = cmd[1].split(" ", 1)
            if len(cmd[1]) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            generate(cmd[1])
        elif cmd[0] == "set":
            if cmd[1].lower() == "rubrics":
                rubrics = os.getcwd()
                output.append("rubrics = " + rubrics)
            elif cmd[1].lower() == "top":
                top = os.getcwd()
                output.append("top = " + top)
        elif cmd[0] == "rubric":
            if not rubrics:
                output.append("Location not set")
            else:
                if len(cmd) == 1:
                    output.append("rubrics = " + rubrics)
                else:
                    rubric = fuzzy(cmd[1], rubrics)
                    os.startfile(rubrics + "\\" + rubric)
                    output.append("Opening " + rubric)
        elif cmd[0] == "pretty":
            for idir in os.listdir():
                xdir = idir.split("_")
                if len(xdir) == 4:
                    name = xdir[3].split("-")[0]
                    build(name)
                elif len(xdir) == 5:
                    name = xdir[4].split("-")[0]
                    build(name)
                else:
                    output.append(" * " + idir)
        elif cmd[0] == "top":
            os.chdir(top)
        elif cmd[0] == "download":
            web("https://github.com/Nexumi/ConsoleBuddy/releases")
        elif cmd[0] == "update":
            updating()
        elif cmd[0] == "version":
            output.append("ConsoleBuddy " + v)
            update()
        elif cmd[0] == "setup":
            if len(cmd) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            cmd[1] = cmd[1].split(" ", 1)
            if len(cmd[1]) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            if "submissions.zip" in os.listdir():
                with ZipFile("submissions.zip", 'r') as zipObj:
                    zipObj.extractall(path = "Assignment-" + cmd[1][0])
                os.remove("submissions.zip")
                os.chdir("Assignment-" + cmd[1][0])
                top = os.getcwd()
                unzipper()
                generate(cmd[1])
                os.chdir("..")
            else:
                output.append("submissions.zip not found")
        elif cmd[0] == "assignment":
            if len(cmd) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            web("https://csc210.ducta.net/Assignments/Assignment-" + cmd[1] + "/" + "Assignment-" + cmd[1] + ".pdf")
        elif cmd[0] == "run":
            if len(cmd) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            java = fuzzy(cmd[1])
            native("javac -encoding ISO-8859-1 *.java")
            native("java " + java.replace(".class", ""))
            for idir in os.listdir():
                if idir[-6:] == ".class":
                    os.remove(idir)
        else:
            native(" ".join(cmd))
        return True
    except Exception as e:
        output.append(e)
        return False

if os.name == "nt":
    programs = {}
    programs["Notepad++"] = locate("Notepad++", "notepad++.exe")
    programs["Sublime Text"] = locate("Sublime Text", "sublime_text.exe")
    poppers = []
    for program in programs.keys():
        if not programs.get(program):
            poppers.append(program)
    for popper in poppers:
        programs.pop(popper)
    del poppers
else:
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        os.chdir(os.path.sep.join(argv[0].split(os.path.sep)[:-1]))
    except:
        pass

if "ConsoleBuddyUpdater.exe" in os.listdir():
    sleep(1)
    os.remove("ConsoleBuddyUpdater.exe")

rubrics = None
top = os.getcwd()

cmd = ""
skip = False
output = []
update()
header()
while cmd.lower().strip() != "exit":
    cmd = " ".join(input("Console> ").split())
    command(cmd)
    header()

clear()