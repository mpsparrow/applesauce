'''
Basic logging functions
'''
import datetime

# writes message to log file
def logWrite(filename, message, tag="", start=""):
    outputLog = open(f'logs/{filename}','a+')
    outputLog.write(f"{start}[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]{tag.upper()} {message}\n")
    outputLog.close()

# wipes log file
def logWipe(filename):
    outputLog = open(f'logs/{filename}','w+')
    outputLog.close()

# returns log file contents
def logReturn(filename):
    with open(f'logs/{filename}') as f:
        return f.read()

def errorLog(message):
    logWrite('output-log.txt', message, tag="[error]")

def warningLog(message):
    logWrite('output-log.txt', message, tag="[warning]")

def passedLog(message):
    logWrite('output-log.txt', message, tag="[passed]")

def infoLog(message):
    logWrite('output-log.txt', message, tag="[info]")

def normalLog(message):
    logWrite('output-log.txt', message, tag="")