"""
Start log quick functions.
"""
import log
from util import config

def getFile():
    """
    Get name of log file from mainConfig.ini.
    """
    conf = config.readINI("mainConfig.ini")
    return str(conf[logs][start])

def log(msg: str):
    """
    No tag log function.
    :param str msg: Message to log
    """
    log.write(getFile(), msg, tag="")

def error(msg: str):
    """
    [ERROR] tag log function.
    :param str msg: Message to log
    """
    log.write(getFile(), msg, tag="[ERROR]")

def warn(msg: str):
    """
    [WARN] tag log function.
    :param str msg: Message to log
    """
    log.write(getFile(), msg, tag="[WARN]")

def info(msg: str):
    """
    [INFO] tag log function.
    :param str msg: Message to log
    """
    log.write(getFile(), msg, tag="[INFO]")

def proceed(msg: str):
    """
    [PASS] tag log function.
    :param str msg: Message to log
    """
    log.write(getFile(), msg, tag="[PASS]")

def skip(msg: str):
    """
    [SKIP] tag log function.
    :param str msg: Message to log
    """
    log.write(getFile(), msg, tag="[SKIP]")

def custom(msg: str, tag: str):
    """
    Custom tag log function.
    :param str msg: Message to log
    :param str tag: Tag name (i.e tag="foo" produces [FOO])
    """
    log.write(getFile(), msg, tag=f"[{tag}]")