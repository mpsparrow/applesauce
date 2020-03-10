# Quick logging functions
import datetime


# writes to log
def write(filename: str, msg: str, tag="", start=""):
    log = open(f'logs/{filename}','a+')
    log.write(f"{start}[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]{tag.upper()} {msg}\n")
    log.close()

# wipes log
def wipe(filename: str):
    log = open(f'logs/{filename}','w+')
    log.close()

# returns log
def output(filename: str):
    with open(f'logs/{filename}') as log:
        return log.read()

# startup log logging commands    
startFilename = "startup-log.txt"
def errorStart(msg: str):
    write(startFilename, msg, tag="[error]")

def warnStart(msg: str):
    write(startFilename, msg, tag="[warn]")

def passStart(msg: str):
    write(startFilename, msg, tag="[pass]")

def skipStart(msg: str):
    write(startFilename, msg, tag="[skip]")

def infoStart(msg: str):
    write(startFilename, msg, tag="[info]")

def normStart(msg: str):
    write(startFilename, msg, tag="")

# runtime log logging commands
runFilename = "runtime-log.txt"
def errorRun(msg: str):
    write(runFilename, msg, tag="[error]")

def warnRun(msg: str):
    write(runFilename, msg, tag="[warn]")

def infoRun(msg: str):
    write(runFilename, msg, tag="[info]")

def adminRun(msg: str):
    write(runFilename, msg, tag="[admin]")

def normRun(msg: str):
    write(runFilename, msg, tag="")