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
    """
    config = configparser.ConfigParser()
    config.read(filename)
    return config

def dumpINI(filename: str, write):
    """
    Write to ini file
    :param str filename: ini file name
    :param write: contents to write to ini file
    """
    config = configparser.ConfigParser()
    config.write(write)

def readJSON(filename: str):
    """
    Read json file
    :param str filename: json file name
    :return: parsable json
    """
    with open(filename, 'r') as jsondata:
        data = json.load(jsondata)
    return data

def dumpJSON(filename: str, data):
    """
    Write to json file
    :param str filename: json file name
    :param write: contents to write to json file
    """
    with open(filename, 'w') as jsondata:
        json.dump(data, jsondata, indent=4)