'''
Start log functions.
'''
import log
from util import config

# Gets start log file name from config.
def getFile():
    conf = config.readINI("mainConfig.ini")
    return str(conf[logs][start])

def log(msg: str):
    log.write(getFile(), msg, tag="")

def error(msg: str):
    log.write(getFile(), msg, tag="[error]")

def warn(msg: str):
    log.write(getFile(), msg, tag="[warn]")

def info(msg: str):
    log.write(getFile(), msg, tag="[info]")

def pasS(msg: str):
    log.write(getFile(), msg, tag="[pass]")

def skip(msg: str):
    log.write(getFile(), msg, tag="[skip]")

def custom(msg: str, tag: str):
    log.write(getFile(), msg, tag=f"[{tag}]")