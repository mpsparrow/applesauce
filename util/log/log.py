'''
Main log functions.
'''
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