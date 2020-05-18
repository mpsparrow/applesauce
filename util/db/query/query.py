"""
Database querying
"""
from util.db import connect
from util.log import runLog
from util import exceptions

def query(query: str):
    """
    Commits a query to the database
    :param str query: mySQL query
    :return: query data using fetchall()
    :raises dbQueryFail: if query fails to return result
    """
    try:
        cnx = connect.connect()
    except dbConnectionFail:
        raise dbQueryFail
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(query)
            dbData = cursor.fetchall()
        except Exception as e:
            runLog.error("Query failed. (commit.query)")
            runLog.error(e)
            raise dbQueryFail
            cursor.close()
            cnx.close()
        else:
            cursor.close()
            cnx.close()
            return dbData

def queryV(query: str, values: tuple):
    """
    Commits a query to the database
    :param str query: mySQL query
    :param tuple values: query values
    :return: query data using fetchall()
    :raises dbQueryFail: if query fails to return result
    """
    try:
        cnx = connect.connect()
    except dbConnectionFail:
        raise dbQueryFail
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(query, values)
            dbData = cursor.fetchall()
        except Exception as e:
            runLog.error("Query failed. (query.queryV)")
            runLog.error(e)
            raise dbQueryFail
            cursor.close()
            cnx.close()
        else:
            cursor.close()
            cnx.close()
            return dbData