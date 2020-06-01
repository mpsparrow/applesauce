'''
Main log functions.
'''
import datetime
from util import config
from termcolor import colored

def write(filename: str, msg: str, tag="", start="", showdate=True, console=False, tagcolor=""):
    """
    Write to selected log file.
    :param str filename: txt file name
    :param str msg: Message to log
    :param tag: Tag name (i.e tag="foo" produces [FOO])
    :type tag: str or None
    :param start: Add str to the start of str being written to log
    :type start: str or None
    :param showdate: Show date in front of log msg (default True)
    :type showdate: bool or None
    :param console: log in console
    :type console: bool or None
    :param tagcolor: color for tag
    :type tagcolor: str or None
    """
    conf = config.readINI("mainConfig.ini")
    enableConsole = conf["logs"].getboolean("consoleLog")
    log = open(f'logs/{filename}','a+')
    if showdate:
        log.write(f"{start}[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]{tag.upper()} {msg}\n")
        if console and enableConsole:
            if len(tagcolor) == 0:
                print(f"{start}[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]{tag.upper()} {msg}")
            else:
                print(f"{start}[{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}]{colored(tag.upper(), tagcolor)} {msg}")
    else:
        log.write(f"{start}{tag.upper()} {msg}\n")
        if console and enableConsole:
            if len(tagcolor) == 0:
                print(f"{start}{tag.upper()} {msg}")
            else:
                print(f"{start}{colored(tag.upper(), tagcolor)} {msg}")
    log.close()

def wipe(filename: str):
    """
    Wipe selected log file.
    :param str filename: txt file name
    """
    log = open(f'logs/{filename}','w+')
    log.close()

def read(filename: str):
    """
    Returns contents of log file.
    :param str filename: txt file name
    :return: log file contents
    :rtype: str
    """
    with open(f'logs/{filename}') as log:
        return log.read()