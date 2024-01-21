v = "v0.7.0"

# TODO: make folders have '' to better indicate if they are a folder or not

import os
import ssl
from sys import argv
from time import sleep
from zipfile import ZipFile
from canvasapi import Canvas
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
    try:
        data = urlopen(url)
    except:
        return
    for line in data:
        r = str(line)[7:-6]
        data.close()
    if dev(v, r):
        output.append("[\033[34mnotice\033[0m] A new release of ConsoleBuddy is available: \033[31m" + v + "\033[0m -> \033[32m" + r + "\033[0m")
        output.append("[\033[34mnotice\033[0m] To update, run: \033[32mupdate\033[0m")
        cmd = "update"

def updating():
    global cmd
    global output
    os.chdir(os.path.sep.join(argv[0].split(os.path.sep)[:-1]))
    try:
        urlretrieve("https://raw.githubusercontent.com/Nexumi/ConsoleBuddy/main/ConsoleBuddyUpdater.exe", "ConsoleBuddyUpdater.exe")
    except:
        output.append("Something went wrong while trying to update. Maybe check your internet connection?")
        return
    os.startfile("ConsoleBuddyUpdater.exe")
    cmd = "exit"

def find(directory, folder, program):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            if file.lower() == folder.lower():
                if program in os.listdir(directory + os.path.sep + file):
                    return directory + os.path.sep + file + os.path.sep + program

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
    dirs = os.listdir()
    for i in range(len(dirs)):
        if os.path.isfile(dirs[i]):
            dirs[i] = green + dirs[i] + reset
        else:
            dirs[i] = blue + dirs[i] + reset
    print("  |  ".join(dirs) + "\n")
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
            if os.path.isfile(dirs[i]):
                color = green
            else:
                color = blue
            output.append(str(i + 1) + ") " + color + dirs[i] + reset)
        header()
        try:
            opt = int(input("Option> ")) - 1
            return dirs[opt]
        except:
            return file

def unzipper():
    dirs = os.listdir()
    for idir in dirs:
        if idir[-4:].lower() == ".zip":
            os.mkdir(idir[:-4])
            with ZipFile(idir, 'r') as zipObj:
              zipObj.extractall(path=idir[:-4])
            os.remove(idir)

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
    # rubric = "Assignment-" + cmd[0] + "-Rubric.xlsx"
    rubric = "Assignment-" + cmd + "-Rubric.xlsx"
    folder = rubric[:-5] + "s"
    # names = namelist(cmd[1])
    infile = open("../namelist.txt")
    names = infile.read().splitlines()
    infile.close()
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

def choice(values):
    x = -1
    while x < 0 or x >= i - 1:
        header()
        i = 1
        for value in values:
            print(str(i) + ": " + str(value))
            i += 1
        try:
            n = input("Number: ")
            if n == "cancel":
                return
            x = int(n) - 1
        except:
            pass
    return values[x]

def canvas():
    global top
    try:
        cfg = open("ConsoleBuddy.cfg", "x")
        output.append("First time setup!")
        header()
        cfg.write(input("Canvas Token: ") + "\n")
        cfg.write(input("Course ID: "))
        cfg.close()
    except:
        pass
    API_URL = "https://sfsu.instructure.com/"

    # Canvas API key
    file = open("ConsoleBuddy.cfg")
    cfg = file.read().splitlines()
    file.close()

    API_KEY = cfg[0]
    COURSE_ID = cfg[1]

    canvas = Canvas(API_URL, API_KEY)

    try:
        course = canvas.get_course(COURSE_ID)
    except:
        output.append("Something went wrong while trying to load assignments. Maybe check your internet connection?")
        return

    assignments = course.get_assignments()

    assignment = choice(assignments)
    if assignment == None:
        return

    submissions = assignment.get_submissions()

    print()
    print("Downloading Assignments...")

    folder = str(assignment)
    folder = folder[:folder.index(" (")]
    try:
        os.mkdir(folder)
    except:
        i = 1
        while True:
            try:
                os.mkdir(folder + " (" + str(i) + ")")
                folder += " (" + str(i) + ")"
                break
            except:
                i += 1
    os.chdir(folder)

    names = []
    for submission in submissions:
        if len(submission.attachments):
            student = str(course.get_user(submission.user_id))
            student = student[:student.index(" (")]
            print(student)
            names.append(student.replace(" ", ""))

            attachment = submission.attachments[0]
            urlretrieve(attachment.url, attachment.filename)
    unzipper()

    data = urlopen("https://web.jpkit.us/grader-rubrics/rubrics.txt")
    rubrics = []
    for info in data:
        rubrics.append(info.decode("utf-8").replace("\n", ""))
    rubric = choice(rubrics)
    if rubric == None:
        return

    print()
    print("Generating Rubrics...")

    folder = rubric[:-5] + "s"
    os.mkdir(folder)
    os.chdir(folder)
    urlretrieve("https://web.jpkit.us/grader-rubrics/" + rubric, rubric)
    for name in names:
        print(name + "-" + rubric)
        copy2(rubric, name + "-" + rubric)
    os.remove(rubric)

    os.chdir("..")

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
        elif cmd[0] == "del" or cmd[0] == "rm":
            if len(cmd) == 1:
                native(cmd[0])
                return
            path = fuzzy(cmd[1])
            if path == ".":
                header("\n")
                output.append("WARNING: " + cmd[0] + " . is disabled as it deletes everything in the current directory.")
                output.append("If you want to delete everything, delete the folder: cd .. > " + cmd[0] + " folder_name")
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
        # elif cmd[0] == "generate":
        #     if len(cmd) == 1:
        #         output.append("The syntax of the command is incorrect.")
        #         return
        #     # cmd[1] = cmd[1].split(" ", 1)
        #     # if len(cmd[1]) == 1:
        #     #     output.append("The syntax of the command is incorrect.")
        #     #     return
        #     generate(cmd[1])
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
        # elif cmd[0] == "setup":
        #     if len(cmd) == 1:
        #         output.append("The syntax of the command is incorrect.")
        #         return
        #     # cmd[1] = cmd[1].split(" ", 1)
        #     # if len(cmd[1]) == 1:
        #     #     output.append("The syntax of the command is incorrect.")
        #     #     return
        #     if "submissions.zip" in os.listdir():
        #         with ZipFile("submissions.zip", 'r') as zipObj:
        #             # zipObj.extractall(path = "Assignment-" + cmd[1][0])
        #             zipObj.extractall(path = "Assignment-" + cmd[1])
        #         os.remove("submissions.zip")
        #         # os.chdir("Assignment-" + cmd[1][0])
        #         os.chdir("Assignment-" + cmd[1])
        #         top = os.getcwd()
        #         unzipper()
        #         generate(cmd[1])
        #         os.chdir("..")
        #     else:
        #         output.append("submissions.zip not found")
        elif cmd[0] == "assignment":
            if len(cmd) == 1:
                output.append("The syntax of the command is incorrect.")
                return
            web("https://csc215.ducta.net/Assignments/Assignment-" + cmd[1] + "/" + "Assignment-" + cmd[1] + ".pdf")
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
        elif cmd[0] == "canvas":
            canvas()
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

green = "\033[32m"
blue = "\033[34m"
reset = "\033[0m"

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