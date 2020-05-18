"""
Run log quick functions.
"""
from util.log import log as l
from util import config

def getFile():
    """
    Get name of log file from mainConfig.ini.
    """
    conf = config.readINI("mainConfig.ini")
    return str(conf[logs][run])

def log(msg: str):
    """
    No tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="")

def error(msg: str):
    """
    [ERROR] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[ERROR]")

def warn(msg: str):
    """
    [WARN] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[WARN]")

def info(msg: str):
    """
    [INFO] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[INFO]")

def admin(msg: str):
    """
    [ADMIN] tag log function.
    :param str msg: Message to log
    """
    l.write(getFile(), msg, tag="[ADMIN]")

def custom(msg: str, tag: str):
    """
    Custom tag log function.
    :param str msg: Message to log
    :param str tag: Tag name (i.e tag="foo" produces [FOO])
    """
    l.write(getFile(), msg, tag=f"[{tag}]")