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

def log(msg: str):
    """
    No tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="")
    print(msg)

def error(msg: str):
    """
    [ERROR] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[ERROR]")
    print(msg)

def warn(msg: str):
    """
    [WARN] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[WARN]")
    print(msg)

def info(msg: str):
    """
    [INFO] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[INFO]")
    print(msg)

def proceed(msg: str):
    """
    [PASS] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[PASS]")
    print(msg)

def skip(msg: str):
    """
    [SKIP] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[SKIP]")
    print(msg)

def custom(msg: str, thistag="", thisstart=""):
    """
    Custom tag log function.
    :param str msg: Message to log
    :param str tag: Tag name (i.e tag="[foo]" produces [FOO])
    """
    l.write(getFile(), msg, tag=thistag, start=thisstart)
    print(msg)