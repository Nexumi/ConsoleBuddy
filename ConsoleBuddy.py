v = "v0.3"

import os
import shutil
import subprocess
from validators import url
from zipfile import ZipFile
from urllib.request import urlopen, urlretrieve

def reload():
    global cmd
    os.startfile(__file__)
    cmd = "exit"

def update(download = False):
    global cmd
    url = "https://raw.githubusercontent.com/Nexumi/ConsoleBuddy/main/ConsoleBuddy.py"
    for line in urlopen(url):
        r = str(line)[7:-6]
        break
    if v != r:
        if download:
            urlretrieve(url, __file__)
            print("[\033[34mnotice\033[0m] Successfully installed ConsoleBuddy \033[32m" + r + "\033[0m")
            input("Press enter to relaunch...")
            reload()
        else:
            print("[\033[34mnotice\033[0m] A new release of ConsoleBuddy is available: \033[31m" + v + "\033[0m -> \033[32m" + r + "\033[0m")
            print("[\033[34mnotice\033[0m] To update, run: \033[32mupdate\033[0m")
            cmd = "update"
    else:
        if download:
            print("[\033[34mnotice\033[0m] ConsoleBuddy is up-to-date")

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
            header("\n")
            return dirs[opt]
        except:
            header("\n")
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
    return students

def generate(cmd, refresh = True):
    global rubrics
    rubric = "Assignment-" + cmd[0] + "-Rubric.xlsx"
    folder = rubric[:-5] + "s"
    names = namelist(cmd[1])
    if not url("https://jpweb.ml/grader-rubrics/" + rubric):
        missing = "rubric"
        if not names:
            missing += " and grader"
        print("404 " + missing + " not found")
        return False
    if not names:
        print("404 grader not found")
        return False
    os.mkdir(folder)
    os.chdir(folder)
    urlretrieve("https://jpweb.ml/grader-rubrics/" + rubric, rubric)
    for name in names:
        shutil.copy2(rubric, name + "-" + rubric)
    os.remove(rubric)
    rubrics = os.getcwd()
    os.chdir("..")
    if refresh:
        header()
    return True

def command(cmd):
    global rubrics
    global top
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
            if len(cmd) == 1:
                os.system(cmd[0])
                return
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
        elif cmd[0] == "java":
            if len(cmd) == 1:
                os.system(cmd[0])
                return
            os.system("java " + fuzzy(cmd[1]).replace(".class", ""))
        elif cmd[0] == "unzipper":
            unzipper()
            header()
        elif cmd[0] == "startwith":
            program = cmd[1].split()
            if notepad_plus_plus and program[0].lower() == "notepad++":
                java = fuzzy(" ".join(program[1:]))
                subprocess.Popen([notepad_plus_plus, java])
                print("Opening " + java)
            elif sublime_text and " ".join(program[:2]).lower() == "sublime text":
                java = fuzzy(" ".join(program[2:]))
                subprocess.Popen([sublime_text, java])
                print("Opening " + java)
            elif sublime_text and program[0].lower() == "sublime":
                java = fuzzy(" ".join(program[1:]))
                subprocess.Popen([sublime_text, java])
                print("Opening " + java)
            else:
                print("Program not found or not defined")
        elif cmd[0] == "eval":
            eval(cmd[1])
        elif cmd[0] == "programs":
            if notepad_plus_plus:
                print(notepad_plus_plus)
            if sublime_text:
                print(sublime_text)
        elif cmd[0] == "generate":
            if len(cmd) == 1:
                print("The syntax of the command is incorrect.")
                return
            cmd[1] = cmd[1].split(" ", 1)
            if len(cmd[1]) == 1:
                print("The syntax of the command is incorrect.")
                return
            generate(cmd[1])
        elif cmd[0] == "set":
            if cmd[1].lower() == "rubrics":
                rubrics = os.getcwd()
                print("rubrics = " + rubrics)
            elif cmd[1].lower() == "top":
                top = os.getcwd()
                print("top = " + top)
        elif cmd[0] == "rubric":
            if not rubrics:
                print("Location not set")
            else:
                if len(cmd) == 1:
                    print("rubrics = " + rubrics)
                else:
                    rubric = fuzzy(cmd[1], rubrics)
                    os.startfile(rubrics + "\\" + rubric)
                    print("Opening " + rubric)
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
        elif cmd[0] == "top":
            os.chdir(top)
            header()
        elif cmd[0] == "update":
            update(True)
        elif cmd[0] == "version":
            print("ConsoleBuddy " + v)
            update()
        elif cmd[0] == "setup":
            if len(cmd) == 1:
                print("The syntax of the command is incorrect.")
                return
            cmd[1] = cmd[1].split(" ", 1)
            if len(cmd[1]) == 1:
                print("The syntax of the command is incorrect.")
                return
            if "submissions.zip" in os.listdir():
                assignment = "Assignment-" + cmd[0]
                with ZipFile("submissions.zip", 'r') as zipObj:
                    zipObj.extractall(path = "Assignment-" + cmd[1][0])
                os.remove("submissions.zip")
                os.chdir("Assignment-" + cmd[1][0])
                unzipper()
                generate(cmd[1], False)
                os.chdir("..")
                header()
            else:
                print("submissions.zip not found")
        else:
            os.system(" ".join(cmd))
        return True
    except Exception as e:
        print(e)
        return False

notepad_plus_plus = locate("Notepad++", "notepad++.exe")
sublime_text = locate("Sublime Text", "sublime_text.exe")
rubrics = None
top = os.getcwd()

header("\n")
cmd = ""
update()
while cmd.lower().strip() != "exit":
    if cmd.strip() != "":
        print()
    cmd = " ".join(input("Console> ").split())
    header("\n")
    command(cmd)

os.system("cls")