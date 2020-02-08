'''
Useful functions to retrieve and load config information
'''
import json
import configparser
from utils import logger

# read ini
def read(filename: str):
    try:
        config = configparser.ConfigParser()
        config.read(filename)
        return config
    except Exception as e:
        logger.errorRun("config.py read ini")
        logger.errorRun(e)

# dump ini
def dump(filename: str, write):
    try:
        config = configparser.ConfigParser()
        config.write(write)
    except Exception as e:
        logger.errorRun("config.py dump ini")
        logger.errorRun(e)

# read json
def readJSON(filename: str):
    try:
        with open(filename, 'r') as jsondata:
            data = json.load(jsondata)
        return data
    except Exception as e:
        logger.errorRun("config.py read json")
        logger.errorRun(e)

# dump json
def dumpJSON(filename: str, data):
    try:
        with open(filename, 'w') as jsondata:
            json.dump(data, jsondata, indent=4)
    except Exception as e:
        logger.errorRun("config.py dump json")
        logger.errorRun(e)