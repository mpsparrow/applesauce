# writes message to log file
def logWrite(filename, message):
    outputLog = open(f'logs/{filename}','a+')
    outputLog.write(f'{message}\n')
    outputLog.close()

# wipes log file
def logWipe(filename):
    outputLog = open(f'logs/{filename}','w+')
    outputLog.close()

# returns log file contents
def logReturn(filename):
    with open(f'logs/{filename}') as f:
        return f.read()