"""
Database querying
"""
from util.db import connect
from util.log import runLog
from util import exceptions

def query(q: str):
    """
    Commits a query to the database
    :param str q: mySQL query
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
            cursor.execute(q)
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

def queryV(q: str, values: tuple):
    """
    Commits a query to the database
    :param str q: mySQL query
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
            cursor.execute(q, values)
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