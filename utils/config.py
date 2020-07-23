"""
Config read/write functions for INI and JSON
"""
import json
import configparser
from utils.logger import log

class configError(FrameworkError):
    """
    Raised when there is an error accessing a config file
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            log.error(f"configError, {self.message}")
            return f"configError, {self.message}"
        log.error("configError has been raised")
        return "configError has been raised"

def readINI(filename: str):
    """
    Read ini file
    :param str filename: ini file name
    :return: parsable ini
    :raises configError: if it fails to read or access ini file
    """
    try:
        conf = configparser.ConfigParser()
        conf.read(filename)
    except:
        raise configError("failed to read (utils.config.readINI)")
    else:
        return conf

def dumpINI(write):
    """
    Write to ini file
    :param write: contents to write to ini file
    :raises configError: if it fails to write to ini file
    """
    try:
        conf = configparser.ConfigParser()
        conf.write(write)
    except:
        raise configError("failed to write (utils.config.dumpINI)")

def readJSON(filename: str):
    """
    Read json file
    :param str filename: json file name
    :return: parsable json
    :raises configError: if it fails to read or access json file
    """
    try:
        with open(filename, 'r') as jsondata:
            data = json.load(jsondata)
    except:
        raise configError("failed to read (utils.config.readJSON)")
    else:
        return data

def dumpJSON(filename: str, data):
    """
    Write to json file
    :param str filename: json file name
    :param write: contents to write to json file
    :raises configError: if it fails to write to json file
    """
    try:
        with open(filename, 'w') as jsondata:
            json.dump(data, jsondata, indent=4)
    except:
        raise configError("failed to write (utils.config.dumpJSON)")