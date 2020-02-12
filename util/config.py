# Useful functions to read and write to config files.
import json
import configparser
import logger

# Reads and returns .ini file
def readINI(filename: str):
    config = configparser.ConfigParser()
    config.read(filename)
    return config

# Writes to .ini file
def dumpINI(filename: str, write):
    config = configparser.ConfigParser()
    config.write(write)

# Reads and returns .json file
def readJSON(filename: str):
    with open(filename, 'r') as jsondata:
        data = json.load(jsondata)
    return data

# Writes to .json file
def dumpJSON(filename: str, data):
    with open(filename, 'w') as jsondata:
        json.dump(data, jsondata, indent=4)