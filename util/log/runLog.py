'''
Run log functions.
'''
import log
from util import config

# Gets run log file name from config.
def getFile():
    conf = config.readINI("mainConfig.ini")
    return str(conf[logs][run])

def log(msg: str):
    log.write(getFile(), msg, tag="")

def error(msg: str):
    log.write(getFile(), msg, tag="[error]")

def warn(msg: str):
    log.write(getFile(), msg, tag="[warn]")

def info(msg: str):
    log.write(getFile(), msg, tag="[info]")

def admin(msg: str):
    log.write(getFile(), msg, tag="[admin]")

def custom(msg: str, tag: str):
    log.write(getFile(), msg, tag=f"[{tag}]")