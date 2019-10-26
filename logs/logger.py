# writes message to output-log.txt
def outputWrite(message):
    outputLog = open(r'logs\output-log.txt','a+')
    outputLog.write(f'{message}\n')
    outputLog.close()

# wipes everything from output-log.txt
def outputWipe():
    outputLog = open(r'logs\output-log.txt','w+')
    outputLog.close()
