import os
import shutil
from zipfile import ZipFile

cmd = ""

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
        raise Exception("[WinError 2] The system cannot find the file specified: '" + path + "'")
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
            return "."

def command(cmd):
    try:
        cmd = cmd.split(" ", 1)
        cmd[0] = cmd[0].lower()
        if cmd[0] == "cd":
            if len(cmd) == 1:
                os.system(cmd[0])
                return

            if cmd[1].replace("/", "") == "." or cmd[1].replace("/", "") == "..":
                os.chdir(cmd[1])
            else:
                os.chdir(fuzzy(cmd[1]))
            header()
        elif cmd[0] == "del":
            path = fuzzy(cmd[1])
            if path == ".":
                header()
                return
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            header()
        elif cmd[0] == "copy":
            parm = cmd[1].split(" ")
            shutil.copy2(parm[0], parm[1])
            header()
        elif cmd[0] == "start":
            os.system("start \"" + fuzzy(cmd[1]) + "\"")
            header()
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

header("\n")
while cmd.lower() != "exit":
    if cmd != "":
        print()
    cmd = " ".join(input("Console> ").split())
    header("\n")
    command(cmd)

os.system("cls")