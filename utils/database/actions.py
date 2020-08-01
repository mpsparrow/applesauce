from pymongo import MongoClient
from utils.config import readINI

def connect():
    """
    Connects to main database
    :return: client
    """
    conf = readINI("config.ini")["MongoDB"]
    client = MongoClient(f"mongodb://{conf['user']}:{conf['password']}@{conf['host']}?authSource={conf['database']}")
    return client

def connectC(user: str, password: str, host: str, database: str):
    """
    Connects to custom database
    :param str name: username
    :param str password: password
    :param str host: host URL/IP
    :param str database: database name
    :return: client
    """
    client = MongoClient(f"mongodb://{user}:{password}@{host}?authSource={database}")
    return client