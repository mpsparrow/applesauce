# writes message to log file
def logWrite(file, message):
    outputLog = open(f'logs/{file}','a+')
    outputLog.write(f'{message}\n')
    outputLog.close()

# wipes clean log file
def logWipe(file):
    outputLog = open(f'logs/{file}','w+')
    outputLog.close()

# returns log file contents
def logReturn(file):
    with open(f'logs/{file}') as f:
        return f.read()