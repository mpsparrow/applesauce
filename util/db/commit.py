"""
Database committing
"""
from util.db import connect
from util.log import runLog
from util import exceptions

def commit(query: str, values: tuple):
    """
    Commits a query to the database
    :param str query: mySQL query
    :param tuple values: values for query
    :raises dbCommitFail: if query fails to commit
    """
    try:
        cnx = connect.connect()
    except exceptions.dbConnectionFail:
        raise exceptions.dbCommitFail
    else:
        try:
            cursor = cnx.cursor()
            cursor.execute(query, values)
            cnx.commit()
        except Exception as e:
            runLog.error("Query failed to commit. (commit.commit)")
            runLog.error(e)
            raise exceptions.dbCommitFail
        finally:
            cursor.close()
            cnx.close()