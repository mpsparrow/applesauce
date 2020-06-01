"""
Start log quick functions.
"""
from util.log import log as l
from util import config

def getFile():
    """
    Get name of log file from mainConfig.ini.
    """
    conf = config.readINI("mainConfig.ini")
    return str(conf["logs"]["start"])

def log(msg: str, console=False):
    """
    No tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="", console=console)

def error(msg: str, console=False):
    """
    [ERROR] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[ERROR]", console=console, tagcolor="red")

def warn(msg: str, console=False):
    """
    [WARN] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[WARN]", console=console, tagcolor="yellow")

def info(msg: str, console=False):
    """
    [INFO] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[INFO]", console=console)

def proceed(msg: str, console=False):
    """
    [PASS] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[PASS]", console=console, tagcolor="green")

def skip(msg: str, console=False):
    """
    [SKIP] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[SKIP]", console=console)

def debug(msg: str, console=False):
    """
    [DEBUG] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[DEBUG]", console=console)

def custom(msg: str, thistag="", thisstart="", console=False):
    """
    Custom tag log function.
    :param str msg: Message to log
    :param str tag: Tag name (i.e tag="[foo]" produces [FOO])
    :param console: log in console
    """
    l.write(getFile(), msg, tag=thistag, start=thisstart, console=console)