"""
MongoDB connection and action functions
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.config import readINI

def connect():
    """
    Connects to main MongoDB database defined in config.ini
    :return: client
    """
    conf = readINI("config.ini")["MongoDB"]
    client = MongoClient(f"mongodb://{conf['user']}:{conf['password']}@{conf['host']}/?authSource={conf['database']}")
    return client

def connectC(user: str, password: str, host: str, database: str):
    """
    Connects to custom MongoDB database
    :param str name: username
    :param str password: password
    :param str host: host URL/IP
    :param str database: database name
    :return: client
    """
    client = MongoClient(f"mongodb://{user}:{password}@{host}/?authSource={database}")
    return client

def isConnected(client: MongoClient):
    """
    Checks MongoDB connection
    :param client: client from MongoClient
    :return: boolean value
    """
    try:
        client.admin.command('ismaster')
        return True
    except ConnectionFailure:
        return False
    else:
        return False