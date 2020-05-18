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
    return str(conf["logs"]["run"])

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
    l.write(getFile(), msg, tag="[ERROR]", console=console)

def warn(msg: str, console=False):
    """
    [WARN] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[WARN]", console=console)

def info(msg: str, console=False):
    """
    [INFO] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[INFO]", console=console)

def admin(msg: str, console=False):
    """
    [ADMIN] tag log function.
    :param str msg: Message to log
    :param console: log in console
    """
    l.write(getFile(), msg, tag="[ADMIN]", console=console)

def custom(msg: str, tag: str, console=False):
    """
    Custom tag log function.
    :param str msg: Message to log
    :param str tag: Tag name (i.e tag="foo" produces [FOO])
    :param console: log in console
    """
    l.write(getFile(), msg, tag=f"[{tag}]", console=console)