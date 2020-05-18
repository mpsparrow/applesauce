"""
Config read/write functions for INI and JSON
"""
import json
import configparser

def readINI(filename: str):
    """
    Read ini file
    :param str filename: ini file name
    :return: parsable ini
    :raises configReadError: if it fails to read or access ini file
    """
    try:
        conf = configparser.ConfigParser()
        conf.read(filename)
    except:
        raise configReadError
    else:
        return conf

def dumpINI(write):
    """
    Write to ini file
    :param write: contents to write to ini file
    :raises configWriteError: if it fails to write to ini file
    """
    try:
        conf = configparser.ConfigParser()
        conf.write(write)
    except:
        raise configWriteError

def readJSON(filename: str):
    """
    Read json file
    :param str filename: json file name
    :return: parsable json
    :raises configReadError: if it fails to read or access json file
    """
    try:
        with open(filename, 'r') as jsondata:
            data = json.load(jsondata)
    except:
        raise configReadError
    else:
        return data

def dumpJSON(filename: str, data):
    """
    Write to json file
    :param str filename: json file name
    :param write: contents to write to json file
    :raises configWriteError: if it fails to write to json file
    """
    try:
        with open(filename, 'w') as jsondata:
            json.dump(data, jsondata, indent=4)
    except:
        raise configWriteError