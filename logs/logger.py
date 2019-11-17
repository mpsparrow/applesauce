# wiping and writing commands for log files
# writes message to output-log.txt
def outputWrite(message):
    outputLog = open(r'logs\output-log.txt','a+')
    outputLog.write(f'{message}\n')
    outputLog.close()

# wipes everything from output-log.txt
def outputWipe():
    outputLog = open(r'logs\output-log.txt','w+')
    outputLog.close()

# writes message to command-log.txt
def commandWrite(message):
    commandLog = open(r'logs\command-log.txt','a+')
    commandLog.write(f'{message}\n')
    commandLog.close()

# wipes everything from command-log.txt
def commandWipe():
    commandLog = open(r'logs\command-log.txt','w+')
    commandLog.close()

# writes message to message-log.txt
def messageWrite(message):
    messageLog = open(r'logs\message-log.txt','a+')
    messageLog.write(f'{message}\n')
    messageLog.close()

# wipes everything from message-log.txt
def messageWipe():
    messageLog = open(r'logs\message-log.txt','w+')
    messageLog.close()
