'''
mySql connection module
This isn't functioning yet
'''
import json
from utils import config, logger
import mysql.connector
from mysql.connector import errorcode

def SQLquery(query):
    try:
        config = config.configLoad('config.json')
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