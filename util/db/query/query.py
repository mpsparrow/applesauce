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
    :raises dbQueryFail: if query fails to return result in any way
    """
    try:
        cnx = connect.connect()
    except exceptions.dbConnectionFail:
        raise exceptions.dbQueryFail("raised due to dbConnectionFail (util.db.query.query.query)")
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(q)
            dbData = cursor.fetchall()
        except Exception as e:
            raise exceptions.dbQueryFail(f"query failed (util.db.query.query.query): {e}")
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
    :raises dbQueryFail: if query fails to return result in any way
    """
    try:
        cnx = connect.connect()
    except exceptions.dbConnectionFail:
        raise exceptions.dbQueryFail("raised due to dbConnectionFail (util.db.query.query.queryV)")
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(q, values)
            dbData = cursor.fetchall()
        except Exception as e:
            raise exceptions.dbQueryFail(f"query failed (util.db.query.query.queryV): {e}")
        else:
            cursor.close()
            cnx.close()
            return dbData