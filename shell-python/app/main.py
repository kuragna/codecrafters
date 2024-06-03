import sys
import os

builtins  = ["exit", "echo", "type", "pwd", "cd"]

def exit(status):
    sys.exit(int(status[0]))

def echo(words):
    print(*words)

def pwd(ignore):
    print(os.getcwd())

def cd(path):
    if len(path) == 0:
        os.chdir(os.getenv("HOME"))
    elif path[0] == "~":
        os.chdir(os.getenv("HOME"))
    else:
        if os.path.exists(path[0]):
            os.chdir(path[0])
        else:
            sys.stdout.write("cd: " + path[0] + ": No such file or directory\n")

def isBuitIn(cmd):
    for builtin in builtins:
        if cmd == builtin:
            return True
    return False

def getCmdPath(cmd):
    if cmd.find("/", 0, len(cmd)) != -1:
        return cmd
    paths = os.getenv("PATH").split(":")
    for path in paths:
        path = path + "/" + cmd
        if os.path.exists(path):
            return path
    return None

def _type(cmd):
    r = getCmdPath(cmd[0])
    if isBuitIn(cmd[0]):
        print(cmd[0] + " is a shell builtin")
    elif r:
        print(cmd[0] + " is " + r)
    else:
        sys.stdout.write(cmd[0] + " not found\n")

callbacks = {"exit": exit, "echo": echo, "type": _type, "pwd": pwd, "cd": cd}


def execBuiltIn(words):
    re = False
    cmd = words[0]
    for i in builtins:
        if i == cmd:
            re = True
            callbacks[cmd](words[1:])
    return re

def prompt():
    pid = None
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        line  = input()
        words = line.lstrip().split(" ") # trim space from the beginning
        cmd   = words[0] 
        if execBuiltIn(words):
            continue
        path = getCmdPath(cmd)
        if path == None:
            sys.stdout.write(cmd + ": command not found\n")
            continue
        pid = os.fork()
        if pid == -1:
            sys.stdout.write("failed to create child process\n")
        if pid == 0:
            os.execve(path, words, os.environ)
        else:
            os.wait()

def main():
    # Wait for user input
    prompt()


if __name__ == "__main__":
    main()
