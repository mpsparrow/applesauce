import json
from . import configloader
import mysql.connector
from mysql.connector import errorcode
from logs import logger

def SQLquery(query):
    try:
        config = configloader.configLoad('config.json')
        connection = mysql.connector.connect(
            host=config['mysql']['host'], 
            database=config['mysql']['database'], 
            user=config['mysql']['user'], 
            password=config['mysql']['password'])

        mySql_Create_Table_Query = f"""{query}"""

        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)
        print("Laptop Table created successfully ")

    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")