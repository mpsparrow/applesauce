"""
Database committing
"""
from util.db import connect
from util.log import runLog
from util import exceptions

def commit(query: str):
    """
    Commits a query to the database
    :param str query: mySQL query
    :raises dbCommitFail: if query fails to commit in any way
    """
    try:
        cnx = connect.connect()
    except exceptions.dbConnectionFail:
        raise exceptions.dbCommitFail("raised due to dbConnectionFail (util.db.commit.commit)")
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
        except Exception as e:
            raise exceptions.dbCommitFail(f"query failed to commit (util.db.commit.commit): {e}")
        finally:
            cursor.close()
            cnx.close()

def commitV(query: str, values: tuple):
    """
    Commits a query to the database with separate tuple for values
    :param str query: mySQL query
    :param tuple values: values for query
    :raises dbCommitFail: if query fails to commit in any way
    """
    try:
        cnx = connect.connect()
    except exceptions.dbConnectionFail:
        raise exceptions.dbCommitFail("raised due to dbConnectionFail (util.db.commit.commitV)")
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
        except Exception as e:
            raise exceptions.dbCommitFail(f"query failed to commit (util.db.commit.commitV): {e}")
        finally:
            cursor.close()
            cnx.close()